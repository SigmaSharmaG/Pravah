from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.road import RoadSegment
from geoalchemy2.shape import to_shape

def find_nearest_node(db: Session, lat: float, lon: float) -> int:
    # Query all segments, compute distance to endpoints in Python
    segments = db.query(RoadSegment).all()
    min_dist = float('inf')
    nearest_node = None
    for seg in segments:
        geom = to_shape(seg.geometry)
        # Check both endpoints
        for coord in [geom.coords[0], geom.coords[-1]]:
            dx = lon - coord[0]
            dy = lat - coord[1]
            dist = (dx*dx + dy*dy) ** 0.5
            if dist < min_dist:
                min_dist = dist
                # Determine which endpoint (from_node or to_node)
                if coord == geom.coords[0]:
                    nearest_node = seg.from_node
                else:
                    nearest_node = seg.to_node
    if nearest_node is None:
        raise ValueError("No road segments found")
    return nearest_node