from sqlalchemy.orm import Session
from app.models.route_recommendation import RouteRecommendation
from app.models.shipment import Shipment
from app.models.alert import Alert
from app.services.routing.graph_builder import build_risk_graph


def check_routes_for_risk_increase(db: Session):
    active_recommendations = db.query(RouteRecommendation).filter(RouteRecommendation.is_active == 1).all()
    if not active_recommendations:
        print("No active routes found.")
        return

    graph = build_risk_graph(db)

    for rec in active_recommendations:
        shipment = db.query(Shipment).filter(Shipment.id == rec.shipment_id).first()
        if not shipment:
            continue

        if len(rec.path_segments) == 0:
            continue

        current_risks = [graph.segment_info.get(sid, {}).get('risk_score', 0.5) for sid in rec.path_segments]
        current_avg = sum(current_risks) / len(current_risks) if current_risks else 0

        has_critical_segment = any(risk > 0.8 for risk in current_risks)
        avg_increased = current_avg > rec.average_risk_score + 0.1

        if has_critical_segment or avg_increased:
            message = (
                f"Risk on active route for shipment #{shipment.id} changed. "
                f"Average risk now {current_avg:.2f} (was {rec.average_risk_score:.2f}). "
                f"{'Critical segment detected.' if has_critical_segment else ''}"
            )
            # Create alert
            alert = Alert(
                route_recommendation_id=rec.id,
                shipment_id=shipment.id,
                type="risk_increase",
                message=message
            )
            db.add(alert)
            shipment.status = 'needs_reroute'
            rec.is_active = 0   # deactivate to avoid duplicate alerts
            db.commit()
            print(f"Alert created for shipment {shipment.id}: {message}")
        else:
            print(f"No significant risk change for shipment {shipment.id} (current avg {current_avg:.2f}, stored {rec.average_risk_score:.2f})")