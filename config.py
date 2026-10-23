import os
from dotenv import load_dotenv

load_dotenv()
SESSION_ID = os.getenv("SESSION_ID", "IIOT-CLASS-01")
POWERBI_PUSH_URL = os.getenv("POWERBI_PUSH_URL", "").strip()
DATABASE_PATH = os.getenv("DATABASE_PATH", "feedback_queue.sqlite3")
REQUEST_TIMEOUT_SECONDS = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "4"))
RETRY_INTERVAL_SECONDS = float(os.getenv("RETRY_INTERVAL_SECONDS", "5"))

# BCM GPIO: button pin -> (feedback category, LED pin)
BUTTONS = {
    17: ("UNDERSTOOD", 24),
    22: ("CONFUSED", 25),
    27: ("SLOW_DOWN", 12),
    23: ("NEED_EXAMPLE", 15),
}
BUZZER_PIN = 18
DEBOUNCE_MS = 50
BUZZER_DURATION_SECONDS = 0.15
LED_DURATION_SECONDS = 0.25
