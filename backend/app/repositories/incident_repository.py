from sqlalchemy.orm import Session
from app.models.incident import Incident

def get_active_incidents(db: Session, road_segment_id: int = None):
    query = db.query(Incident)
    if road_segment_id is not None:
        query = query.filter(Incident.road_segment_id == road_segment_id)
    return query.all()

def create_incident(db: Session, incident_data: dict):
    incident = Incident(**incident_data)
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident