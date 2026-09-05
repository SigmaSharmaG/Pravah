from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class RouteRecommendationBase(BaseModel):
    shipment_id: int
    path_nodes: List[int]
    path_segments: List[int]
    total_distance_km: float
    estimated_time_minutes: float
    average_risk_score: float
    average_confidence: float
    risk_penalty_used: float
    reason: Optional[str] = None

class RouteRecommendationCreate(RouteRecommendationBase):
    pass

class RouteRecommendation(RouteRecommendationBase):
    id: int
    generated_at: datetime
    is_active: int

    class Config:
        from_attributes = True