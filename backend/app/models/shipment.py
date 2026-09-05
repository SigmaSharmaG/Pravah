from sqlalchemy import Column, Integer, String, Float, DateTime, BigInteger
from sqlalchemy.sql import func
from app.db.database import Base

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    origin_lat = Column(Float, nullable=False)
    origin_lon = Column(Float, nullable=False)
    destination_lat = Column(Float, nullable=False)
    destination_lon = Column(Float, nullable=False)
    origin_node = Column(BigInteger, nullable=True)   # set later by geocoding
    destination_node = Column(BigInteger, nullable=True)
    cargo_type = Column(String, nullable=False)       # e.g., 'medicine', 'food', 'commercial'
    priority = Column(String, nullable=False)          # 'critical', 'high', 'normal'
    status = Column(String, default='pending')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())