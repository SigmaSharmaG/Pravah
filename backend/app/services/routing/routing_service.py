from sqlalchemy.orm import Session
from app.services.routing.graph_builder import build_risk_graph
from app.models.road import RoadSegment

def recommend_route(db: Session, from_node: int, to_node: int, risk_penalty: float = 1.0):
    graph = build_risk_graph(db)
    if not graph.adj:  # empty graph
        return None

    path_nodes, path_segments, total_weight = graph.shortest_path(
        from_node, to_node, risk_penalty=risk_penalty
    )
    if path_nodes is None:
        return None

    # Get segment details
    segments = db.query(RoadSegment).filter(RoadSegment.id.in_(path_segments)).all()
    seg_map = {s.id: s for s in segments}
    route_segments = [seg_map[sid] for sid in path_segments if sid in seg_map]

    total_distance = sum(s.length_m for s in route_segments)
    avg_risk = sum(graph.segment_info[sid]['risk_score'] for sid in path_segments) / len(path_segments)
    avg_confidence = sum(graph.segment_info[sid]['confidence'] for sid in path_segments) / len(path_segments)

    return {
        "path_nodes": path_nodes,
        "path_segments": path_segments,
        "total_weight": total_weight,
        "total_distance_km": total_distance / 1000,
        "estimated_time_minutes": total_weight / 60,
        "average_risk_score": avg_risk,
        "average_confidence": avg_confidence,
        "risk_penalty_used": risk_penalty
    }