from sqlalchemy.orm import Session
from app.models.route_recommendation import RouteRecommendation
from app.models.shipment import Shipment
from app.services.routing.graph_builder import build_risk_graph
from app.repositories.alert_repository import create_alert

def check_routes_for_risk_increase(db: Session):
    # Get all active recommendations with their shipments
    active_recommendations = db.query(RouteRecommendation).filter(RouteRecommendation.is_active == 1).all()
    if not active_recommendations:
        return

    graph = build_risk_graph(db)  # fresh risk assessment

    for rec in active_recommendations:
        shipment = db.query(Shipment).filter(Shipment.id == rec.shipment_id).first()
        if not shipment:
            continue

        # Recompute current average risk for the route's segments
        if len(rec.path_segments) == 0:
            continue
        current_avg_risk = sum(
            graph.segment_info.get(sid, {}).get('risk_score', 0.5)
            for sid in rec.path_segments
        ) / len(rec.path_segments)

        # Threshold: if risk increased by more than 0.2 compared to original stored risk
        if current_avg_risk > rec.average_risk_score + 0.2:
            # Create alert
            message = (
                f"Risk on active route for shipment #{shipment.id} increased from "
                f"{rec.average_risk_score:.2f} to {current_avg_risk:.2f}. "
                f"Consider rerouting."
            )
            create_alert(db, {
                "route_recommendation_id": rec.id,
                "shipment_id": shipment.id,
                "type": "risk_increase",
                "message": message
            })
            # Optionally mark shipment status as 'needs_reroute'
            shipment.status = 'needs_reroute'
            rec.is_active = 0
            db.commit()

    return