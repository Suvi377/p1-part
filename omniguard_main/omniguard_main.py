
import os
import time
import cv2
import requests
import webbrowser  
from datetime import datetime
from ultralytics import YOLO

# Configuration settings
IMAGE_SAVE_DIR = "runs/incident_frames"
API_URL = "http://127.0.0.1:8000/api/alert"
COOLDOWN_PERIOD = 5.0  # Blocks rapid dashboard spam (5-second throttle)
MIN_WEAPON_CONF = 0.68  # Filters out wrong weapon detections below 68%

os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)

def send_alert_to_backend(incident_label, plate_data="UNKNOWN"):
    """Dispatches real-time detection telemetry down to the central backend server."""
    payload = {
        "incident_type": incident_label, 
        "license_plate": plate_data
    }
    try:
        response = requests.post(API_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"[API Success] Dispatched alert to dashboard: {incident_label}")
        else:
            print(f"[API Error] Server rejected alert with code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[API Network Error] Could not establish connection to backend: {e}")

def main():
    print("[INFO] Loading OpenVINO optimization models...")
    fight_model = YOLO("models/fight_openvino_model", task="detect")
    weapon_model = YOLO("models/weapon_openvino_model", task="detect")
    helmet_model = YOLO("models/helmet_openvino_model", task="detect")
    license_model = YOLO("models/license_plate_openvino_model", task="detect")

    video_source = "weapon 2.mp4"
    cap = cv2.VideoCapture(video_source)
    
    if not cap.isOpened():
        print(f"[ERROR] Could not open video source: {video_source}")
        return

    last_logged_time = {
        "Fight/Violence": 0.0,
        "Weapon Threat": 0.0,
        "Helmet Violation": 0.0,
        "License Plate Tracked": 0.0
    }

    active_alert_text = ""
    alert_banner_expiration = 0.0
    banner_color = (0, 0, 255)
    
    # HYSTERESIS LOCK: Remembers fight state across frame drops
    fight_memory_timeout = 0.0  

    # FIX: Directing browser to the web server URL instead of the local hard drive path
    webbrowser.open("http://127.0.0.1:8000")

    print("[SYSTEM ACTIVE] State Machine Processing streams with API Isolation...")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        current_time = time.time()
        file_timestamp = datetime.now().strftime("%Y%m%dd_%H%M%S")
        annotated_frame = frame.copy()
        plate_data = "UNKNOWN"  # Safe default fallback definition

        # --- STEP 1: LICENSE PLATE TRACKING ---
        license_results = license_model.predict(frame, conf=0.60, imgsz=320, verbose=False)
        if len(license_results[0].boxes) > 0:
            l_conf = float(license_results[0].boxes[0].conf[0])
            if current_time - last_logged_time["License Plate Tracked"] > COOLDOWN_PERIOD:
                frame_path = os.path.join(IMAGE_SAVE_DIR, f"plate_{file_timestamp}.jpg")
                cv2.imwrite(frame_path, frame)
                send_alert_to_backend("License Plate Tracked", plate_data=plate_data)
                last_logged_time["License Plate Tracked"] = current_time
            annotated_frame = license_results[0].plot(img=annotated_frame)

        # --- STEP 2: FIGHT MODEL EVALUATION ---
        fight_results = fight_model.predict(frame, conf=0.50, verbose=False)
        is_fight_detected = len(fight_results[0].boxes) > 0

        if is_fight_detected:
            f_conf = float(fight_results[0].boxes[0].conf[0])
            fight_memory_timeout = current_time + 4.0  # Lock out weapon API for 4 full seconds
            
            active_alert_text = f"CRITICAL: FIGHT DETECTED ({f_conf:.2f})"
            alert_banner_expiration = current_time + 2.0
            banner_color = (0, 0, 255)
            
            if current_time - last_logged_time["Fight/Violence"] > COOLDOWN_PERIOD:
                frame_path = os.path.join(IMAGE_SAVE_DIR, f"fight_{file_timestamp}.jpg")
                cv2.imwrite(frame_path, frame)
                send_alert_to_backend("Fight/Violence", plate_data=plate_data)
                last_logged_time["Fight/Violence"] = current_time
            
            annotated_frame = fight_results[0].plot(img=annotated_frame)
            
            # Render UI overlay
            if current_time < alert_banner_expiration and active_alert_text:
                cv2.rectangle(annotated_frame, (10, 10), (520, 60), banner_color, cv2.FILLED)
                cv2.putText(annotated_frame, active_alert_text, (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow("OmniGuard Integrated Monitoring System", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue

        # --- STEP 3: EVALUATE GLOBAL STATE SAFETY LOCK ---
        is_system_locked_to_fight = current_time < fight_memory_timeout

        if is_system_locked_to_fight:
            active_alert_text = "CRITICAL: FIGHT DETECTED (TRACKING STATE)"
            alert_banner_expiration = current_time + 0.5
            banner_color = (0, 0, 255)
            
            if current_time < alert_banner_expiration and active_alert_text:
                cv2.rectangle(annotated_frame, (10, 10), (520, 60), banner_color, cv2.FILLED)
                cv2.putText(annotated_frame, active_alert_text, (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow("OmniGuard Integrated Monitoring System", annotated_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue 

        # --- STEP 4: RUN WEAPON & HELMET CHECKS (PEACEFUL STATE) ---
        weapon_results = weapon_model.predict(frame, conf=MIN_WEAPON_CONF, verbose=False)
        helmet_results = helmet_model.predict(frame, conf=0.95, verbose=False)

        # Process Weapons safely with configured filters
        if len(weapon_results[0].boxes) > 0:
            w_conf = float(weapon_results[0].boxes[0].conf[0])
            active_alert_text = f"THREAT: WEAPON SPOTTED ({w_conf:.2f})"
            alert_banner_expiration = current_time + 2.0
            banner_color = (0, 69, 255)
            
            if current_time - last_logged_time["Weapon Threat"] > COOLDOWN_PERIOD:
                frame_path = os.path.join(IMAGE_SAVE_DIR, f"weapon_{file_timestamp}.jpg")
                cv2.imwrite(frame_path, frame)
                
                send_alert_to_backend("Weapon Threat", plate_data=plate_data)
                last_logged_time["Weapon Threat"] = current_time
            annotated_frame = weapon_results[0].plot(img=annotated_frame)

        # Process Helmets
        elif len(helmet_results[0].boxes) > 0:
            h_conf = float(helmet_results[0].boxes[0].conf[0])
            active_alert_text = f"VIOLATION: NO HELMET ({h_conf:.2f})"
            alert_banner_expiration = current_time + 2.0
            banner_color = (0, 165, 255)
            
            if current_time - last_logged_time["Helmet Violation"] > COOLDOWN_PERIOD:
                frame_path = os.path.join(IMAGE_SAVE_DIR, f"helmet_{file_timestamp}.jpg")
                cv2.imwrite(frame_path, frame)
                send_alert_to_backend("Helmet Violation", plate_data=plate_data)
                last_logged_time["Helmet Violation"] = current_time
            annotated_frame = helmet_results[0].plot(img=annotated_frame)

        # --- STEP 5: BANNER INTERACTION DISPLAY ---
        if current_time < alert_banner_expiration and active_alert_text:
            cv2.rectangle(annotated_frame, (10, 10), (520, 60), banner_color, cv2.FILLED)
            cv2.putText(annotated_frame, active_alert_text, (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow("OmniGuard Integrated Monitoring System", annotated_frame)
        if cv2.waitKey(70) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[SYSTEM END] Code execution complete.")

if __name__ == "__main__":
    main()