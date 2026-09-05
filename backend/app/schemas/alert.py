from pydantic import BaseModel
from datetime import datetime

class AlertBase(BaseModel):
    route_recommendation_id: int
    shipment_id: int
    type: str
    message: str

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    acknowledged: bool
    created_at: datetime

    class Config:
        from_attributes = True