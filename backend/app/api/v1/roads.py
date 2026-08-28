from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.road import RoadSegment as RoadSegmentModel
from app.schemas.road import RoadSegment as RoadSegmentSchema

router = APIRouter()

@router.get("/", response_model=List[RoadSegmentSchema])
def list_roads(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    roads = db.query(RoadSegmentModel).offset(skip).limit(limit).all()
    return roads