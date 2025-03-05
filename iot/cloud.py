import firebase_admin
from firebase_admin import credentials, db
from config.settings import settings

class CloudManager:
    def __init__(self):
        cred = credentials.Certificate(settings.firebase_key_path)
        firebase_admin.initialize_app(cred, {
            'databaseURL': settings.firebase_db_url
        })
        self.ref = db.reference('/translations')
    
    def log_translation(self, data):
        self.ref.push({
            'letters': data.get('letters', []),
            'word': data.get('word', ''),
            'timestamp': data.get('timestamp', '')
        })