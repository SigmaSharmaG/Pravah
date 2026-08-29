from sqlalchemy.orm import Session
from app.models.road import RoadSegment
from app.models.incident import Incident
from app.integrations.ml.mock_predictor import mock_predictor
from app.services.risk.risk_engine import assess_risk

def compute_risk_for_all_segments(db: Session):
    segments = db.query(RoadSegment).all()
    results = []
    for seg in segments:
        # Fetch active incidents for this segment (all, regardless of verified)
        incidents = db.query(Incident).filter(Incident.road_segment_id == seg.id).all()
        # Convert ORM objects to dicts for the risk engine
        incident_dicts = [
            {
                "type": inc.type,
                "severity": inc.severity,
                "source": inc.source,
                "verified": inc.verified
            }
            for inc in incidents
        ]

        prediction = mock_predictor.predict(seg.id, seg.slope, seg.elevation)
        assessment = assess_risk(seg.id, prediction, incident_dicts)
        results.append(assessment)
    return results