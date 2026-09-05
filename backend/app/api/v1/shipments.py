from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.shipment import Shipment as ShipmentModel   # SQLAlchemy model
from app.schemas.shipment import ShipmentCreate, Shipment    # Pydantic schemas
from app.services.routing.routing_service import recommend_route_for_shipment
from app.schemas.route_recommendation import RouteRecommendation
from app.services.routing.geocoding import geocode_place_name

router = APIRouter()

@router.post("/", response_model=Shipment, status_code=201)
def create_shipment(shipment: ShipmentCreate, db: Session = Depends(get_db)):
    data = shipment.dict()

    # Geocode origin if name provided
    if data.get('origin_name'):
        info = geocode_place_name(data['origin_name'])
        if info is None:
            raise HTTPException(status_code=400, detail=f"Unknown origin place: {data['origin_name']}")
        lat, lon, node_id = info
        data['origin_lat'] = lat
        data['origin_lon'] = lon
        if node_id is not None:
            data['origin_node'] = node_id   # override any provided value
        else:
            data['origin_node'] = None      # will be found later via coordinates

    # Geocode destination if name provided
    if data.get('destination_name'):
        info = geocode_place_name(data['destination_name'])
        if info is None:
            raise HTTPException(status_code=400, detail=f"Unknown destination place: {data['destination_name']}")
        lat, lon, node_id = info
        data['destination_lat'] = lat
        data['destination_lon'] = lon
        if node_id is not None:
            data['destination_node'] = node_id
        else:
            data['destination_node'] = None

    # Basic validation: either lat/lon or node IDs required
    has_coords = (data.get('origin_lat') is not None and data.get('origin_lon') is not None and
                  data.get('destination_lat') is not None and data.get('destination_lon') is not None)
    has_nodes = (data.get('origin_node') is not None and data.get('destination_node') is not None)

    if not has_coords and not has_nodes:
        raise HTTPException(
            status_code=400,
            detail="Provide either origin/destination coordinates (lat/lon), place names, or node IDs"
        )

    data['status'] = 'pending'
    db_shipment = ShipmentModel(**data)
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment


@router.get("/{shipment_id}", response_model=Shipment)
def get_shipment(shipment_id: int, db: Session = Depends(get_db)):
    shipment = db.query(ShipmentModel).filter(ShipmentModel.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment

@router.post("/{shipment_id}/reroute", response_model=RouteRecommendation)
def reroute_shipment(shipment_id: int, db: Session = Depends(get_db)):
    route = recommend_route_for_shipment(db, shipment_id)
    if not route:
        raise HTTPException(status_code=404, detail="No feasible route found")
    return route