from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    route_recommendation_id = Column(Integer, ForeignKey("route_recommendations.id"), nullable=False)
    shipment_id = Column(Integer, ForeignKey("shipments.id"), nullable=False)
    type = Column(String, nullable=False)          # e.g., "risk_increase"
    message = Column(String, nullable=False)
    acknowledged = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())