from sqlalchemy.orm import Session
from app.models.road import RoadSegment
from app.integrations.ml.mock_predictor import mock_predictor
from app.services.risk.risk_engine import assess_risk

def compute_risk_for_all_segments(db: Session):
    segments = db.query(RoadSegment).all()
    results = []
    for seg in segments:
        # For now, no incidents considered; we'll add incidents later
        prediction = mock_predictor.predict(seg.id, seg.slope, seg.elevation)
        assessment = assess_risk(seg.id, prediction, [])
        results.append(assessment)
    return results