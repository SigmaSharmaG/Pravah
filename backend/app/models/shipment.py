from sqlalchemy import Column, Integer, String, Float, DateTime, BigInteger
from sqlalchemy.sql import func
from app.db.database import Base

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    origin_name = Column(String, nullable=True)
    destination_name = Column(String, nullable=True)
    origin_lat = Column(Float, nullable=True)
    origin_lon = Column(Float, nullable=True)
    destination_lat = Column(Float, nullable=True)
    destination_lon = Column(Float, nullable=True)
    origin_node = Column(BigInteger, nullable=True)
    destination_node = Column(BigInteger, nullable=True)
    cargo_type = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    status = Column(String, default='pending')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())