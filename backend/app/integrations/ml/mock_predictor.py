import random
from datetime import datetime, timezone

class MockPredictor:
    def __init__(self):
        self.model_version = "mock-v0"

    def predict(self, road_segment_id: int, slope: float, elevation: float):
        # Use slope to influence landslide probability
        if slope > 10:
            landslide_prob = random.uniform(0.5, 0.95)
        elif slope > 5:
            landslide_prob = random.uniform(0.2, 0.5)
        else:
            landslide_prob = random.uniform(0.0, 0.2)

        # Elevation (low areas near rivers) can increase flood probability
        if elevation < 200:
            flood_prob = random.uniform(0.3, 0.9)
        else:
            flood_prob = random.uniform(0.0, 0.3)

        # General blockage probability depends on both
        blockage_prob = max(landslide_prob * 0.7, flood_prob * 0.5) + random.uniform(0.0, 0.1)
        blockage_prob = min(blockage_prob, 0.99)

        # Confidence is random but mostly high
        confidence = round(random.uniform(0.75, 0.98), 2)

        return {
            "road_segment_id": road_segment_id,
            "blockage_probability": round(blockage_prob, 2),
            "flood_probability": round(flood_prob, 2),
            "landslide_probability": round(landslide_prob, 2),
            "confidence": confidence,
            "prediction_horizon_hours": 6,
            "model_version": self.model_version,
            "predicted_at": datetime.now(timezone.utc).isoformat()
        }

# Singleton instance to use elsewhere
mock_predictor = MockPredictor()