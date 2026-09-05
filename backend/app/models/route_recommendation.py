from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from app.db.database import Base

class RouteRecommendation(Base):
    __tablename__ = "route_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    path_nodes = Column(JSON, nullable=False)          # list of node IDs
    path_segments = Column(JSON, nullable=False)        # list of road segment IDs
    total_distance_km = Column(Float, nullable=False)
    estimated_time_minutes = Column(Float, nullable=False)
    average_risk_score = Column(Float, nullable=False)
    average_confidence = Column(Float, nullable=False)
    risk_penalty_used = Column(Float, nullable=False)
    reason = Column(String, nullable=True)              # explanation e.g., "avoided high-risk segments"
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Integer, default=1)              # 1 = active, 0 = superseded