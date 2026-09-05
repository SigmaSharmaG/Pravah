from fastapi import FastAPI
from app.api.v1.router import api_router
from app.db.database import engine, Base
from app.models import road, incident, shipment, route_recommendation, alert  # import all models
from app.services.alerts.scheduler import start_alert_monitor

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pravah Logistics Intelligence")

app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    start_alert_monitor(interval_seconds=30)

@app.get("/health/live")
def live():
    return {"status": "alive"}

@app.get("/health/ready")
def ready():
    try:
        engine.connect()
        return {"status": "ready"}
    except Exception:
        return {"status": "not_ready"}, 503