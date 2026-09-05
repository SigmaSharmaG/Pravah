from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.models.alert import Alert as AlertModel
from app.schemas.alert import Alert
from app.schemas.update_schemas import AlertUpdate

router = APIRouter()

@router.get("/", response_model=List[Alert])
def list_alerts(
    shipment_id: Optional[int] = None,
    acknowledged: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(AlertModel)
    if shipment_id is not None:
        query = query.filter(AlertModel.shipment_id == shipment_id)
    if acknowledged is not None:
        query = query.filter(AlertModel.acknowledged == acknowledged)
    return query.all()

@router.get("/{alert_id}", response_model=Alert)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert

@router.patch("/{alert_id}", response_model=Alert)
def update_alert(alert_id: int, update_data: AlertUpdate, db: Session = Depends(get_db)):
    alert = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(alert, field, value)
    db.commit()
    db.refresh(alert)
    return alert

@router.post("/{alert_id}/acknowledge", response_model=Alert)
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.acknowledged = True
    db.commit()
    db.refresh(alert)
    return alert

@router.delete("/{alert_id}", status_code=204)
def delete_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(alert)
    db.commit()
    return None