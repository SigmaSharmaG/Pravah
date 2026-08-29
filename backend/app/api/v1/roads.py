from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.road import RoadSegment as RoadSegmentModel
from app.schemas.road import RoadSegment as RoadSegmentSchema
from app.services.risk.risk_service import compute_risk_for_all_segments

router = APIRouter()

@router.get("/", response_model=List[RoadSegmentSchema])
def list_roads(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    roads = db.query(RoadSegmentModel).offset(skip).limit(limit).all()
    return roads

@router.get("/risk")
def get_road_risks(db: Session = Depends(get_db)):
    assessments = compute_risk_for_all_segments(db)
    # Convert dataclasses to dict
    return [a.__dict__ for a in assessments]


