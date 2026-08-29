from fastapi import FastAPI
from app.api.v1.router import api_router
from app.db.database import engine
from app.models import road, incident #, shipment  # import models so Base can create tables

# Create tables (for dev; we'll use Alembic later)
road.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pravah Logistics Intelligence")

app.include_router(api_router, prefix="/api/v1")

@app.get("/health/live")
def live():
    return {"status": "alive"}

@app.get("/health/ready")
def ready():
    # check database connection
    try:
        engine.connect()
        return {"status": "ready"}
    except Exception:
        return {"status": "not_ready"}, 503