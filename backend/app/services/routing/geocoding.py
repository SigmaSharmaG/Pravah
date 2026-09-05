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


# Local mapping for pilot region: place name -> (lat, lon, node_id)
PLACE_INFO = {
    "guwahati": (26.1445, 91.7362, 113),
    "shillong": (25.5788, 91.8933, 178),
    "nongpoh": (25.9022, 91.8811, 1538),   # example, adjust as needed
    "jowai": (25.3000, 92.1500, None),      # if no node known, set None
    # Add more places and node IDs from your valid nodes list
}

def geocode_place_name(name: str):
    """Return (lat, lon, node_id) for a given place name, or None if not found."""
    if not name:
        return None
    key = name.strip().lower()
    return PLACE_INFO.get(key)