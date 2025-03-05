import unittest
from unittest.mock import patch, MagicMock
from iot.alerts import AlertSystem
from iot.cloud import CloudManager
from utils.words import WordBuilder
from datetime import datetime, time
import time

class SystemTests(unittest.TestCase):
    # Existing alert tests
    @patch('twilio.rest.api.v2010.account.message.MessageList.create')
    def test_emergency_alert(self, mock_sms):
        AlertSystem().send_emergency_alert("TEST")
        self.assertTrue(mock_sms.called)
        self.assertIn("EMERGENCY", mock_sms.call_args[1]['body'])

    @patch('twilio.rest.api.v2010.account.message.MessageList.create')
    def test_connection_alert(self, mock_sms):
        AlertSystem().send_connection_alert()
        self.assertIn("disconnected", mock_sms.call_args[1]['body'])

    @patch('twilio.rest.api.v2010.account.message.MessageList.create')
    def test_gesture_alert(self, mock_sms):
        AlertSystem().send_gesture_alert()
        self.assertIn("unrecognized", mock_sms.call_args[1]['body'])

    # New word formation tests
    def test_word_formation(self):
        """Test letter combination into words"""
        builder = WordBuilder()
        
        # Test basic word formation
        builder.add_gesture("H")
        builder.add_gesture("E")
        self.assertEqual(builder.add_gesture("L"), "HEL")
        
        # Test timeout reset
        builder.word_timeout = 0.1  # 100ms for testing
        time.sleep(0.2)
        self.assertEqual(builder.add_gesture("O"), "O")

    def test_undo_function(self):
        """Test letter-level undo functionality"""
        builder = WordBuilder()
        
        builder.add_gesture("H")
        builder.add_gesture("E")
        builder.add_gesture("L")
        self.assertEqual(builder.add_gesture("UNDO"), "HE")
        
        # Test undo on empty word
        builder = WordBuilder()
        self.assertEqual(builder.add_gesture("UNDO"), "")

    # Firebase logging test
    @patch('firebase_admin.db.reference')
    def test_firebase_logging(self, mock_firebase):
        """Test translation logging to Firebase"""
        mock_ref = MagicMock()
        mock_firebase.return_value = mock_ref
        
        cloud = CloudManager()
        test_data = {
            "letters": ["H", "E", "L", "P"],
            "word": "HELP",
            "timestamp": datetime.now().isoformat()
        }
        
        cloud.log_translation(test_data)
        
        # Verify Firebase push called with correct data
        mock_ref.push.assert_called_once_with({
            'letters': ["H", "E", "L", "P"],
            'word': "HELP",
            'timestamp': test_data['timestamp']
        })

if __name__ == "__main__":
    unittest.main()