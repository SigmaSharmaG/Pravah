import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.models.incident import Incident
from app.models.shipment import Shipment
from app.models.route_recommendation import RouteRecommendation
from app.models.alert import Alert
from app.core.security import get_password_hash
from app.models.user import User

def reset_all():
    db = SessionLocal()
    try:
        # Delete in order to respect foreign keys
        alerts = db.query(Alert).delete()
        routes = db.query(RouteRecommendation).delete()
        shipments = db.query(Shipment).delete()
        incidents = db.query(Incident).delete()
        db.commit()
        print(f"Cleared {alerts} alerts, {routes} routes, {shipments} shipments, {incidents} incidents.")
    except Exception as e:
        db.rollback()
        print(f"Error during reset: {e}")
        return  # Stop if reset fails
    finally:
        # Ensure db is closed if we return early
        # But careful: if we return, the finally still runs, but we close db only at end
        pass

    # Seed demo user in a separate try block
    try:
        existing = db.query(User).filter(User.username == "demo").first()
        if not existing:
            db.add(User(
                username="demo",
                email="demo@pravah.in",
                hashed_password=get_password_hash("demo123"),
                role="dispatcher"
            ))
            db.commit()
            print("Demo user seeded.")
        else:
            print("Demo user already exists.")
    except Exception as e:
        db.rollback()
        print(f"Error during seeding: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_all()