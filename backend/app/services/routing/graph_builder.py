from sqlalchemy.orm import Session
from app.models.road import RoadSegment
from app.integrations.ml.mock_predictor import mock_predictor
from app.services.risk.risk_engine import assess_risk
from app.models.incident import Incident
from app.services.routing.graph import RoadGraph

def build_risk_graph(db: Session) -> RoadGraph:
    graph = RoadGraph()
    segments = db.query(RoadSegment).all()
    if not segments:
        return graph

    # Precompute risk per segment ID
    risk_map = {}
    for seg in segments:
        incidents = db.query(Incident).filter(Incident.road_segment_id == seg.id).all()
        incident_dicts = [
            {"type": i.type, "severity": i.severity, "source": i.source, "verified": i.verified}
            for i in incidents
        ]
        prediction = mock_predictor.predict(seg.id, seg.slope, seg.elevation)
        assessment = assess_risk(seg.id, prediction, incident_dicts)
        risk_map[seg.id] = assessment

    # Build graph edges
    speed_map = {
        'motorway': 80, 'trunk': 60, 'primary': 50,
        'secondary': 40, 'tertiary': 30, 'residential': 20,
        'unclassified': 20
    }
    for seg in segments:
        speed = speed_map.get(seg.road_type, 30)  # km/h
        base_time_seconds = seg.length_m * 3.6 / speed
        graph.add_edge(seg.from_node, seg.to_node, seg.id, base_time_seconds)
        assessment = risk_map[seg.id]
        graph.set_risk(seg.id, assessment.score, assessment.confidence)

    return graph