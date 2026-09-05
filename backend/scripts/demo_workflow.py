import sys
import os
import time
import requests

BASE_URL = "http://localhost:8000/api/v1"

def main():
    # 1. Create shipment from Guwahati to Shillong
    print("Creating shipment...")
    shipment_data = {
        "origin_name": "Guwahati",
        "destination_name": "Shillong",
        "cargo_type": "medicine",
        "priority": "critical"
    }
    resp = requests.post(f"{BASE_URL}/shipments/", json=shipment_data)
    if resp.status_code != 201:
        print("Shipment creation failed:", resp.text)
        return
    shipment = resp.json()
    shipment_id = shipment["id"]
    print(f"Shipment created with ID {shipment_id}")

    # 2. Get route recommendation
    print("Requesting route...")
    resp = requests.post(f"{BASE_URL}/routes/recommend?shipment_id={shipment_id}")
    if resp.status_code != 200:
        print("Route recommendation failed:", resp.text)
        return
    route = resp.json()
    print(f"Route generated: {route['total_distance_km']:.2f} km, risk {route['average_risk_score']:.2f}")
    first_segment = route["path_segments"][0]
    print(f"First segment ID: {first_segment}")

    # 3. Simulate incident on first segment
    print("Adding blocked incident...")
    incident_data = {
        "road_segment_id": first_segment,
        "type": "blocked",
        "severity": "critical",
        "source": "manual",
        "description": "Landslide blocking road",
        "verified": True
    }
    resp = requests.post(f"{BASE_URL}/incidents/", json=incident_data)
    if resp.status_code != 201:
        print("Incident creation failed:", resp.text)
        return
    print("Incident created.")

    # 4. Wait for alert monitor to pick up (30 sec interval)
    print("Waiting for alert (30 seconds)...")
    time.sleep(35)

    # 5. Check alerts
    resp = requests.get(f"{BASE_URL}/alerts?shipment_id={shipment_id}")
    alerts = resp.json()
    if alerts:
        print(f"Alert received: {alerts[-1]['message']}")
    else:
        print("No alert received. Check alert monitor logs.")

    # 6. Reroute
    print("Rerouting shipment...")
    resp = requests.post(f"{BASE_URL}/shipments/{shipment_id}/reroute")
    if resp.status_code == 200:
        new_route = resp.json()
        print(f"New route: {new_route['total_distance_km']:.2f} km, risk {new_route['average_risk_score']:.2f}")
    else:
        print("Reroute failed (expected if no alternative):", resp.text)

if __name__ == "__main__":
    main()