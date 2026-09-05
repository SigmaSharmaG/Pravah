from sqlalchemy.orm import Session
from app.models.alert import Alert

def create_alert(db: Session, alert_data: dict):
    alert = Alert(**alert_data)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

def list_alerts(db: Session, shipment_id: int = None, acknowledged: bool = None):
    query = db.query(Alert)
    if shipment_id is not None:
        query = query.filter(Alert.shipment_id == shipment_id)
    if acknowledged is not None:
        query = query.filter(Alert.acknowledged == acknowledged)
    return query.all()