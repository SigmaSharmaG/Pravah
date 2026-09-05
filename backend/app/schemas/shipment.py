from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.core.enums import CargoType, ShipmentPriority, ShipmentStatus

class ShipmentBase(BaseModel):
    origin_name: Optional[str] = None
    destination_name: Optional[str] = None
    origin_lat: Optional[float] = None
    origin_lon: Optional[float] = None
    destination_lat: Optional[float] = None
    destination_lon: Optional[float] = None
    origin_node: Optional[int] = None
    destination_node: Optional[int] = None
    cargo_type: CargoType
    priority: ShipmentPriority

class ShipmentCreate(ShipmentBase):
    pass

class Shipment(ShipmentBase):
    id: int
    status: ShipmentStatus
    created_at: datetime

    class Config:
        from_attributes = True