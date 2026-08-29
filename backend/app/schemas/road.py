from pydantic import BaseModel
from typing import Optional

class RoadSegmentBase(BaseModel):
    osm_id: str
    name: Optional[str] = None
    road_type: str
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