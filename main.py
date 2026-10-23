import argparse
import logging
import threading

from config import DATABASE_PATH, RETRY_INTERVAL_SECONDS
from hardware import RaspberryPiHardware, SimulatedHardware
from powerbi import PowerBIClient
from storage import EventStore
from telemetry import make_feedback_event

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

class FeedbackApplication:
    def __init__(self):
        self.store = EventStore(DATABASE_PATH)
        self.powerbi = PowerBIClient()
        self._stop = threading.Event()
        self._sync_thread = threading.Thread(target=self._sync_loop, daemon=True)

    def start(self):
        self._sync_thread.start()

    def stop(self):
        self._stop.set()
        self._sync_thread.join(timeout=2)

    def record_feedback(self, feedback_type: str):
        event = make_feedback_event(feedback_type)
        event_id = self.store.add(event)
        log.info("Recorded event #%s: %s; pending=%s",
                 event_id, feedback_type, self.store.count_pending())
        if self.powerbi.send(event):
            self.store.mark_sent(event_id)
            log.info("Event #%s delivered to Power BI.", event_id)
        else:
            log.warning("Event #%s queued for retry.", event_id)

    def _sync_loop(self):
        while not self._stop.is_set():
            for event_id, event in self.store.pending(limit=100):
                if self._stop.is_set():
                    break
                if self.powerbi.send(event):
                    self.store.mark_sent(event_id)
                    log.info("Queued event #%s delivered.", event_id)
                else:
                    break
            self._stop.wait(RETRY_INTERVAL_SECONDS)

def main():
    parser = argparse.ArgumentParser(description="IIoT Class Feedback System")
    parser.add_argument("--simulate", action="store_true", help="run without Raspberry Pi GPIO")
    args = parser.parse_args()
    app = FeedbackApplication()
    app.start()
    hardware = None
    try:
        if args.simulate:
            hardware = SimulatedHardware(app.record_feedback)
            hardware.run()
        else:
            hardware = RaspberryPiHardware(app.record_feedback)
            log.info("Hardware ready. Press Ctrl+C to stop.")
            while True:
                threading.Event().wait(1)
    except KeyboardInterrupt:
        log.info("Stopping.")
    finally:
        app.stop()
        if isinstance(hardware, RaspberryPiHardware):
            hardware.close()

if __name__ == "__main__":
    main()
