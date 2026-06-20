from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import datetime
import os

app = FastAPI()

# FORCE OPEN CORS PERMISSIONS FOR PORT 8000 LOOPBACKS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

global_metrics = {
    "Fight/Violence": 0,
    "Weapon Threat": 0,
    "Helmet Violation": 0,
    "License Plate Tracked": 0
}
recent_logs = []

class AlertPayload(BaseModel):
    incident_type: str
    license_plate: str = "UNKNOWN"

@app.get("/")
def read_root():
    return FileResponse("dashboard.html")

@app.post("/api/alert")
def receive_alert(payload: AlertPayload):
    try:
        label = payload.incident_type.strip().lower()
        matched_key = None

        if "weapon" in label:
            matched_key = "Weapon Threat"
        elif "fight" in label or "violence" in label:
            matched_key = "Fight/Violence"
        elif "helmet" in label:
            matched_key = "Helmet Violation"
        elif "plate" in label or "license" in label:
            matched_key = "License Plate Tracked"

        if matched_key and matched_key in global_metrics:
            global_metrics[matched_key] += 1
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            recent_logs.insert(0, {"timestamp": timestamp, "type": matched_key})
            if len(recent_logs) > 10:
                recent_logs.pop()
            print(f"🔥 Live Alert Processed: {matched_key}")
        return {"status": "success"}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"status": "error"}

@app.get("/api/metrics")
def get_metrics():
    return {"counts": global_metrics, "recent_logs": recent_logs}