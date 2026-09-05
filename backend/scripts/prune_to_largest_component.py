import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import defaultdict, deque
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.road import RoadSegment

def get_largest_component_nodes(db: Session):
    # Build adjacency from road_segments
    adj = defaultdict(list)
    segments = db.query(RoadSegment).all()
    for seg in segments:
        adj[seg.from_node].append(seg.to_node)
        adj[seg.to_node].append(seg.from_node)

    # Find all connected components via BFS
    visited = set()
    largest_component = []
    for node in list(adj.keys()):
        if node not in visited:
            component = []
            q = deque([node])
            visited.add(node)
            while q:
                u = q.popleft()
                component.append(u)
                for v in adj[u]:
                    if v not in visited:
                        visited.add(v)
                        q.append(v)
            if len(component) > len(largest_component):
                largest_component = component
    return set(largest_component)

def main():
    db = SessionLocal()
    try:
        largest_nodes = get_largest_component_nodes(db)
        print(f"Largest component has {len(largest_nodes)} nodes.")

        # Fetch all segments and filter out those not in largest component
        all_segments = db.query(RoadSegment).all()
        to_delete = []
        for seg in all_segments:
            if seg.from_node not in largest_nodes or seg.to_node not in largest_nodes:
                to_delete.append(seg.id)

        print(f"Deleting {len(to_delete)} segments not in largest component...")
        db.query(RoadSegment).filter(RoadSegment.id.in_(to_delete)).delete(synchronize_session=False)
        db.commit()
        print("Pruning complete. Remaining segments are connected.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()