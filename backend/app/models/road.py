from sqlalchemy import Column, Integer, BigInteger, String, Float
from geoalchemy2 import Geometry
from app.db.database import Base

class RoadSegment(Base):
    __tablename__ = "road_segments"

    id = Column(Integer, primary_key=True, index=True)
    osm_id = Column(String, index=True)
    name = Column(String, nullable=True)
    road_type = Column(String)  # e.g., 'primary', 'secondary', 'residential'
    length_m = Column(Float)
    slope = Column(Float, default=0.0)
    elevation = Column(Float, default=0.0)
    from_node = Column(BigInteger, nullable=False)   # OSM node ID of start point
    to_node = Column(BigInteger, nullable=False)     # OSM node ID of end point
    geometry = Column(Geometry("LINESTRING", srid=4326))