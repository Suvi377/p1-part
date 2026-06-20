import sqlite3
import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'smartcity.db')

def init_db():
    """Creates the database and tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create the Incident Logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incident_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            incident_type TEXT NOT NULL,
            license_plate TEXT,
            alert_sent BOOLEAN NOT NULL CHECK (alert_sent IN (0, 1))
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")

def log_incident(incident_type, license_plate="UNKNOWN"):
    """Logs a detected incident into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute('''
        INSERT INTO incident_logs (timestamp, incident_type, license_plate, alert_sent)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, incident_type, license_plate, True))
    
    conn.commit()
    conn.close()
    print(f"💾 Logged to DB: {incident_type} | Plate: {license_plate}")

# Run this once when the module is imported to ensure the table exists
init_db()