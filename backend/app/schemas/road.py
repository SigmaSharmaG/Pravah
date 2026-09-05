from pydantic import BaseModel
from typing import Optional
from app.core.enums import RoadType

class RoadSegmentBase(BaseModel):
    osm_id: str
    name: Optional[str] = None
    road_type: RoadType
    length_m: float
    slope: float = 0.0
    elevation: float = 0.0
    from_node: int
    to_node: int

class RoadSegmentCreate(RoadSegmentBase):
    pass

class RoadSegment(RoadSegmentBase):
    id: int

    class Config:
        from_attributes = True