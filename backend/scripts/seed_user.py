import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def seed_user():
    db = SessionLocal()
    try:
        # Check if user exists
        existing = db.query(User).filter(User.username == "demo").first()
        if existing:
            print("Demo user already exists.")
            return
        user = User(
            username="demo",
            email="demo@pravah.in",
            hashed_password=get_password_hash("demo123"),
            role="dispatcher",
            is_active=True
        )
        db.add(user)
        db.commit()
        print("Demo user created (username: demo, password: demo123)")
    finally:
        db.close()

if __name__ == "__main__":
    seed_user()