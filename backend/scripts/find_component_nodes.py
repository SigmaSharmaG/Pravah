import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collections import defaultdict, deque
from app.db.database import SessionLocal
from app.models.road import RoadSegment

def largest_component_nodes(db):
    adj = defaultdict(list)
    for from_node, to_node in db.query(RoadSegment.from_node, RoadSegment.to_node).all():
        adj[from_node].append(to_node)
        adj[to_node].append(from_node)

    visited = set()
    largest = []
    for node in adj:
        if node not in visited:
            comp = []
            q = deque([node])
            visited.add(node)
            while q:
                u = q.popleft()
                comp.append(u)
                for v in adj[u]:
                    if v not in visited:
                        visited.add(v)
                        q.append(v)
            if len(comp) > len(largest):
                largest = comp
    return largest

if __name__ == "__main__":
    db = SessionLocal()
    nodes = largest_component_nodes(db)
    print(f"Largest component has {len(nodes)} nodes.")
    print("Sample node IDs:", nodes[:50])  # choose any two from this list
    db.close()