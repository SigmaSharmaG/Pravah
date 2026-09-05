from pydantic import BaseModel
from typing import Optional
from app.core.enums import ShipmentStatus, IncidentType, IncidentSeverity

class ShipmentUpdate(BaseModel):
    status: Optional[ShipmentStatus] = None
    origin_name: Optional[str] = None
    destination_name: Optional[str] = None
    cargo_type: Optional[str] = None
    priority: Optional[str] = None

class IncidentUpdate(BaseModel):
    type: Optional[IncidentType] = None
    severity: Optional[IncidentSeverity] = None
    source: Optional[str] = None
    description: Optional[str] = None
    verified: Optional[bool] = None

class AlertUpdate(BaseModel):
    acknowledged: Optional[bool] = None