from twilio.rest import Client
from config.settings import settings

class AlertSystem:
    def __init__(self):
        self.client = Client(settings.twilio_sid, settings.twilio_token)
    
    def send_emergency_alert(self, message):
        self._send_sms(f"🚨 EMERGENCY: {message}")
    
    def send_connection_alert(self):
        self._send_sms("🔌 Connection Alert: Camera feed disconnected")

    def send_gesture_alert(self):
        self._send_sms("❌ Recognition Alert: Multiple unrecognized gestures")

    def _send_sms(self, body):
        try:
            self.client.messages.create(
                body=body,
                from_=settings.twilio_number,
                to=settings.user_number
            )
        except Exception as e:
            print(f"Alert failed: {str(e)}")