# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# # Replace with your actual email credentials (use an App Password for Gmail)
# SENDER_EMAIL = "your_email@gmail.com"
# SENDER_PASSWORD = "your_app_password"
# RECEIVER_EMAIL = "security_team@smartcity.com"

# def send_email_alert(incident_type, license_plate, location="Camera 01 - Main Gate"):
#     """Sends an automated email alert."""
#     try:
#         msg = MIMEMultipart()
#         msg['From'] = SENDER_EMAIL
#         msg['To'] = RECEIVER_EMAIL
#         msg['Subject'] = f"URGENT: OmniGuard AI Detection - {incident_type}"
        
#         body = (
#             f"OmniGuard System has detected an anomaly.\n\n"
#             f"Incident Details:\n"
#             f"- Type: {incident_type}\n"
#             f"- Associated Vehicle: {license_plate}\n"
#             f"- Location: {location}\n\n"
#             f"Please review the system dashboard immediately."
#         )
        
#         msg.attach(MIMEText(body, 'plain'))
        
#         # Connect to Gmail's SMTP server
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(SENDER_EMAIL, SENDER_PASSWORD)
#         text = msg.as_string()
#         server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
#         server.quit()
        
#         print("📧 Email Alert Sent!")
        
#     except Exception as e:
#         print(f"❌ Failed to send Email: {e}")

import smtplib
from email.mime.text import MIMEText

def send_email(incident_details):
    """
    Sends an email notification when an incident is detected.
    """
    print(f"📧 Attempting to send email alert for: {incident_details}")
    
    # Placeholder for your real email details
    sender_email = "your_email@gmail.com"
    receiver_email = "security_team@gmail.com"
    password = "your_app_password" 

    message = MIMEText(f"OmniGuard Security Alert!\n\nDetails: {incident_details}")
    message["Subject"] = "🚨 CRITICAL SMART CITY ALERT"
    message["From"] = sender_email
    message["To"] = receiver_email

    try:
        # If you haven't set up real credentials yet, this print acts as a safe backup
        if sender_email == "your_email@gmail.com":
            print("💡 (Simulated Email) Setup real credentials in alert/mail.py to send actual emails.")
            return True
            
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("✅ Email sent successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False