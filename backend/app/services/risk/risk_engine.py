from enum import Enum
from dataclasses import dataclass
from typing import Optional

class RiskState(str, Enum):
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"

@dataclass
class RiskAssessment:
    road_segment_id: int
    state: RiskState
    score: float          # 0.0 (safe) to 1.0 (most dangerous)
    confidence: float     # 0.0 (no confidence) to 1.0 (full confidence)
    inputs_summary: dict  # for debugging/explanation

def assess_risk(segment_id: int, prediction: Optional[dict], active_incidents: list) -> RiskAssessment:
    """
    Combine ML prediction and active incidents to determine risk.

    - If any incident of type 'blocked' or 'landslide' -> CRITICAL (score 0.95)
    - Else if prediction exists:
        - blockage_probability > 0.8 -> HIGH (score = probability)
        - blockage_probability > 0.5 -> MODERATE (score = probability)
        - else LOW (score = probability)
    - If no prediction and no incidents -> UNKNOWN (score 0.5, confidence 0.3)
    - Confidence is derived from prediction confidence and incident source reliability.
    """
    if active_incidents:
        # Check for critical incident
        for inc in active_incidents:
            if inc.get('type') in ['blocked', 'landslide'] and inc.get('verified', False):
                return RiskAssessment(
                    road_segment_id=segment_id,
                    state=RiskState.CRITICAL,
                    score=0.95,
                    confidence=0.9,
                    inputs_summary={"incident": inc}
                )
        # Even unverified incidents can raise risk
        for inc in active_incidents:
            if inc.get('type') in ['blocked', 'landslide']:
                return RiskAssessment(
                    road_segment_id=segment_id,
                    state=RiskState.HIGH,
                    score=0.8,
                    confidence=0.5,
                    inputs_summary={"unverified_incident": inc}
                )

    if prediction:
        blockage = prediction.get('blockage_probability', 0.0)
        conf = prediction.get('confidence', 0.5)
        if blockage > 0.8:
            state = RiskState.HIGH
        elif blockage > 0.5:
            state = RiskState.MODERATE
        else:
            state = RiskState.LOW
        # Score can be directly the blockage probability
        score = blockage
        # Confidence from ML
        confidence = conf
        return RiskAssessment(
            road_segment_id=segment_id,
            state=state,
            score=score,
            confidence=confidence,
            inputs_summary={"prediction": prediction}
        )

    # No data
    return RiskAssessment(
        road_segment_id=segment_id,
        state=RiskState.UNKNOWN,
        score=0.5,
        confidence=0.3,
        inputs_summary={"no_data": True}
    )