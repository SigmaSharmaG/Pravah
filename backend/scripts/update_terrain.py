import sys
import os
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.road import RoadSegment

def update_terrain():
    db = SessionLocal()
    try:
        segments = db.query(RoadSegment).all()
        print(f"Updating {len(segments)} road segments...")

        for seg in segments:
            # Random elevation between 50 and 2000 meters
            elevation = random.uniform(50, 2000)

            # Slope: most roads < 10 degrees, some steeper up to 20
            # Use a simple triangular distribution: low probability of very high slope
            slope = random.triangular(0, 20, 3)  # mode at 3°

            seg.elevation = round(elevation, 2)
            seg.slope = round(slope, 2)

        db.commit()
        print("Terrain data updated successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_terrain()