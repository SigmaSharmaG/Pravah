from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ShipmentBase(BaseModel):
    origin_lat: Optional[float] = None
    origin_lon: Optional[float] = None
    destination_lat: Optional[float] = None
    destination_lon: Optional[float] = None
    origin_node: Optional[int] = None
    destination_node: Optional[int] = None
    cargo_type: str
    priority: str

class ShipmentCreate(ShipmentBase):
    pass

class Shipment(ShipmentBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True