from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.incident import Incident as IncidentModel
from app.schemas.incident import IncidentCreate, Incident
from app.schemas.update_schemas import IncidentUpdate

router = APIRouter()

@router.post("/", response_model=Incident, status_code=201)
def report_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    db_incident = IncidentModel(**incident.dict())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@router.get("/", response_model=List[Incident])
def list_incidents(
    road_segment_id: Optional[int] = None,
    verified: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(IncidentModel)
    if road_segment_id is not None:
        query = query.filter(IncidentModel.road_segment_id == road_segment_id)
    if verified is not None:
        query = query.filter(IncidentModel.verified == verified)
    return query.all()

@router.get("/{incident_id}", response_model=Incident)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(IncidentModel).filter(IncidentModel.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.patch("/{incident_id}", response_model=Incident)
def update_incident(incident_id: int, update_data: IncidentUpdate, db: Session = Depends(get_db)):
    incident = db.query(IncidentModel).filter(IncidentModel.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(incident, field, value)
    db.commit()
    db.refresh(incident)
    return incident

@router.delete("/{incident_id}", status_code=204)
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(IncidentModel).filter(IncidentModel.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    db.delete(incident)
    db.commit()
    return None