from sqlalchemy.orm import Session
from app.models.shipment import Shipment
from app.models.road import RoadSegment
from app.models.route_recommendation import RouteRecommendation
from app.services.routing.graph_builder import build_risk_graph
from app.services.routing.geocoding import find_nearest_node


def recommend_route_for_shipment(db: Session, shipment_id: int):
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        return None

    # Determine risk penalty based on shipment priority
    priority_penalty_map = {
        'critical': 10.0,
        'high': 5.0,
        'normal': 1.0
    }
    risk_penalty = priority_penalty_map.get(shipment.priority, 1.0)

    # Set origin/destination nodes from coordinates if not already present
    if shipment.origin_node is None:
        if shipment.origin_lat is None or shipment.origin_lon is None:
            return None
        shipment.origin_node = find_nearest_node(db, shipment.origin_lat, shipment.origin_lon)

    if shipment.destination_node is None:
        if shipment.destination_lat is None or shipment.destination_lon is None:
            return None
        shipment.destination_node = find_nearest_node(db, shipment.destination_lat, shipment.destination_lon)

    db.commit()

    # Build the risk-aware graph
    graph = build_risk_graph(db)
    if not graph.adj:   # empty graph, no roads
        return None

    # Find shortest path using risk-adjusted weights
    path_nodes, path_segments, total_weight = graph.shortest_path(
        shipment.origin_node,
        shipment.destination_node,
        risk_penalty=risk_penalty
    )

    if path_nodes is None or path_segments is None or len(path_segments) == 0:
        return None

    # Fetch road segment details
    segments = db.query(RoadSegment).filter(RoadSegment.id.in_(path_segments)).all()
    seg_map = {s.id: s for s in segments}
    total_distance = sum(s.length_m for s in segments)

    # Calculate average risk and confidence
    avg_risk = sum(graph.segment_info[sid]['risk_score'] for sid in path_segments) / len(path_segments)
    avg_confidence = sum(graph.segment_info[sid]['confidence'] for sid in path_segments) / len(path_segments)

    # Generate explanation
    high_risk_segments = [sid for sid in path_segments if graph.segment_info[sid]['risk_score'] > 0.6]
    reason = f"Route uses {len(path_segments)} segments. "
    if high_risk_segments:
        reason += f"Avoided {len(high_risk_segments)} high-risk segments (risk>0.6)."
    else:
        reason += "No high-risk segments on route."

    # Deactivate any previous active recommendations for this shipment
    db.query(RouteRecommendation).filter(
        RouteRecommendation.shipment_id == shipment.id,
        RouteRecommendation.is_active == 1
    ).update({"is_active": 0})

    # Create and store the new recommendation
    new_rec = RouteRecommendation(
        shipment_id=shipment.id,
        path_nodes=path_nodes,
        path_segments=path_segments,
        total_distance_km=total_distance / 1000,
        estimated_time_minutes=total_weight / 60,
        average_risk_score=avg_risk,
        average_confidence=avg_confidence,
        risk_penalty_used=risk_penalty,
        reason=reason
    )
    db.add(new_rec)
    shipment.status = 'route_generated'
    db.commit()
    db.refresh(new_rec)
    return new_rec