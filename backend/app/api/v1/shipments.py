from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.shipment import Shipment as ShipmentModel   # SQLAlchemy model
from app.schemas.shipment import ShipmentCreate, Shipment    # Pydantic schemas
from app.services.routing.routing_service import recommend_route_for_shipment
from app.schemas.route_recommendation import RouteRecommendation

router = APIRouter()

@router.post("/", response_model=Shipment, status_code=201)
def create_shipment(shipment: ShipmentCreate, db: Session = Depends(get_db)):
    # Basic validation: either lat/lon or node IDs required
    has_coords = shipment.origin_lat is not None and shipment.origin_lon is not None and \
                 shipment.destination_lat is not None and shipment.destination_lon is not None
    has_nodes = shipment.origin_node is not None and shipment.destination_node is not None
    if not has_coords and not has_nodes:
        raise HTTPException(
            status_code=400,
            detail="Provide either origin/destination coordinates (lat/lon) or node IDs"
        )

    data = shipment.dict()
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