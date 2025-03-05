import cv2
import time
from datetime import datetime
from config.settings import settings
from utils.gestures import GestureRecognizer
from utils.words import WordBuilder
from iot.cloud import CloudManager
from iot.alerts import AlertSystem
import pyttsx3

def main():
    recognizer = GestureRecognizer()
    word_builder = WordBuilder()
    cloud = CloudManager()
    alerts = AlertSystem()
    tts = pyttsx3.init()
    
    unrecognized_count = 0
    
    cap = cv2.VideoCapture(settings.camera_url)
    
    try:
        while True:
            if not cap.isOpened():
                alerts.send_connection_alert()
                cap = cv2.VideoCapture(settings.camera_url)
                time.sleep(5)
                continue

            ret, frame = cap.read()
            if not ret:
                alerts.send_connection_alert()
                continue
            
            gesture = recognizer.process_frame(frame)
            
            if gesture:
                unrecognized_count = 0
                current_word = word_builder.add_gesture(gesture)
                
                tts.say("Undo successful" if gesture == "UNDO" else gesture)
                tts.runAndWait()
                
                cloud.log_translation({
                    "letters": list(current_word),
                    "word": current_word,
                    "timestamp": datetime.now().isoformat()
                })
                
                if "HELP" in current_word.upper():
                    alerts.send_emergency_alert(current_word)
            else:
                unrecognized_count += 1
                if unrecognized_count >= settings.max_unrecognized:
                    alerts.send_gesture_alert()
                    unrecognized_count = 0

    finally:
        cap.release()

if __name__ == "__main__":
    main()