import os
import tempfile
import unittest
from storage import EventStore

class StorageTests(unittest.TestCase):
    def setUp(self):
        handle, self.path = tempfile.mkstemp(suffix=".sqlite3")
        os.close(handle)
        self.store = EventStore(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_queue_and_delivery_flag(self):
        event_id = self.store.add({"feedback_type": "UNDERSTOOD", "session_id": "test"})
        pending = self.store.pending()
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0][0], event_id)
        self.store.mark_sent(event_id)
        self.assertEqual(self.store.pending(), [])
        self.assertEqual(self.store.count_pending(), 0)

if __name__ == "__main__":
    unittest.main()
