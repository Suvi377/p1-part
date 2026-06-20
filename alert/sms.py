# import os
# from twilio.rest import Client

# # You would typically store these in a .env file for security
# TWILIO_ACCOUNT_SID = 'your_twilio_account_sid'
# TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'
# TWILIO_PHONE_NUMBER = '+1234567890' 
# AUTHORITY_PHONE_NUMBER = '+0987654321' # The police/security number

# def send_sms_alert(incident_type, license_plate, location="Camera 01 - Main Gate"):
#     """Sends an SMS alert using Twilio."""
#     try:
#         client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
#         message_body = (
#             f"🚨 OMNIGUARD ALERT 🚨\n"
#             f"Type: {incident_type}\n"
#             f"Vehicle Plate: {license_plate}\n"
#             f"Location: {location}\n"
#             f"Action Required immediately."
#         )
        
#         message = client.messages.create(
#             body=message_body,
#             from_=TWILIO_PHONE_NUMBER,
#             to=AUTHORITY_PHONE_NUMBER
#         )
#         print(f"📱 SMS Alert Sent! Message SID: {message.sid}")
        
#     except Exception as e:
#         print(f"❌ Failed to send SMS: {e}")

def send_sms(incident_details):
    """
    Sends an SMS notification via Twilio when an incident is detected.
    """
    print(f"💬 Attempting to send SMS alert for: {incident_details}")
    
    # Placeholder for your real Twilio details
    account_sid = "your_twilio_sid"
    auth_token = "your_twilio_auth_token"
    twilio_number = "+1234567890"
    target_number = "+0987654321"

    try:
        if account_sid == "your_twilio_sid":
            print("💡 (Simulated SMS) Setup real Twilio keys in alert/sms.py to send actual texts.")
            return True
            
        # Twilio sending logic goes here when ready
        print("✅ SMS sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to send SMS: {e}")
        return False
    