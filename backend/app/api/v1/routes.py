from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.routing.routing_service import recommend_route

router = APIRouter()

@router.post("/recommend")
def get_route_recommendation(
    from_node: int,
    to_node: int,
    risk_penalty: float = 1.0,
    db: Session = Depends(get_db)
):
    route = recommend_route(db, from_node, to_node, risk_penalty)
    if not route:
        raise HTTPException(status_code=404, detail="No route found between the given nodes")
    return route