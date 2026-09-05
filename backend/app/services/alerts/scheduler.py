import threading
import time
from app.db.database import SessionLocal

def start_alert_monitor(interval_seconds=30):
    def monitor_loop():
        while True:
            try:
                db = SessionLocal()
                from app.services.alerts.alert_service import check_routes_for_risk_increase
                check_routes_for_risk_increase(db)
                db.close()
            except Exception as e:
                print(f"Alert monitor error: {e}")
            time.sleep(interval_seconds)

    thread = threading.Thread(target=monitor_loop, daemon=True)
    thread.start()