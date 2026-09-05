from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.route_recommendation import RouteRecommendation as RouteModel
from app.schemas.route_recommendation import RouteRecommendation
from app.services.routing.routing_service import recommend_route_for_shipment

router = APIRouter()

@router.post("/recommend", response_model=RouteRecommendation)
def recommend_route(shipment_id: int, db: Session = Depends(get_db)):
    route = recommend_route_for_shipment(db, shipment_id)
    if not route:
        raise HTTPException(status_code=404, detail="No route found")
    return route

@router.get("/{route_id}", response_model=RouteRecommendation)
def get_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(RouteModel).filter(RouteModel.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route recommendation not found")
    return route

@router.delete("/{route_id}", status_code=204)
def delete_route(route_id: int, db: Session = Depends(get_db)):
    route = db.query(RouteModel).filter(RouteModel.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route recommendation not found")
    # Soft deactivate
    route.is_active = 0
    db.commit()
    return None