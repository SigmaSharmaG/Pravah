from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    road_segment_id = Column(Integer, ForeignKey("road_segments.id"), nullable=False)
    type = Column(String)          # e.g., 'blocked', 'landslide', 'flood', 'bridge_damage'
    severity = Column(String)      # 'low', 'medium', 'high', 'critical'
    source = Column(String)        # e.g., 'manual', 'weather_api', 'emergency_report'
    description = Column(String, nullable=True)
    reported_at = Column(DateTime(timezone=True), server_default=func.now())
    verified = Column(Boolean, default=False)