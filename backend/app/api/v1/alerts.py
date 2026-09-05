from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.repositories.alert_repository import list_alerts
from app.schemas.alert import Alert

router = APIRouter()

@router.get("/", response_model=List[Alert])
def get_alerts(
    shipment_id: Optional[int] = None,
    acknowledged: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    return list_alerts(db, shipment_id=shipment_id, acknowledged=acknowledged)

@router.post("/{alert_id}/acknowledge", response_model=Alert)
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    from app.models.alert import Alert as AlertModel
    alert = db.query(AlertModel).filter(AlertModel.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.acknowledged = True
    db.commit()
    db.refresh(alert)
    return alert