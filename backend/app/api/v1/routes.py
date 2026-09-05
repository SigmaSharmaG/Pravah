from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.routing.routing_service import recommend_route_for_shipment
from app.schemas.route_recommendation import RouteRecommendation

router = APIRouter()

@router.post("/recommend", response_model=RouteRecommendation)
def recommend_route(shipment_id: int, db: Session = Depends(get_db)):
    route = recommend_route_for_shipment(db, shipment_id)
    if not route:
        raise HTTPException(status_code=404, detail="No route found")
    return route