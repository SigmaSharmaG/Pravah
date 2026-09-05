from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.core.enums import IncidentType, IncidentSeverity

class IncidentBase(BaseModel):
    road_segment_id: int
    type: IncidentType
    severity: IncidentSeverity
    source: str
    description: Optional[str] = None
    verified: bool = False

class IncidentCreate(IncidentBase):
    pass

class Incident(IncidentBase):
    id: int
    reported_at: datetime

    class Config:
        from_attributes = True