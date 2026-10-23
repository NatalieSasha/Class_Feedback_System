import unittest
from telemetry import make_feedback_event

class TelemetryTests(unittest.TestCase):
    def test_event_fields_and_privacy(self):
        event = make_feedback_event("CONFUSED")
        self.assertEqual(event["feedback_type"], "CONFUSED")
        self.assertIn("timestamp", event)
        self.assertIn("session_id", event)
        self.assertNotIn("uid", event)
        self.assertNotIn("student_id", event)

    def test_categories(self):
        for category in ("UNDERSTOOD", "CONFUSED", "SLOW_DOWN", "NEED_EXAMPLE"):
            self.assertEqual(make_feedback_event(category)["feedback_type"], category)

if __name__ == "__main__":
    unittest.main()
