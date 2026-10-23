from datetime import datetime, timezone
from config import SESSION_ID


def make_feedback_event(feedback_type: str) -> dict:
    # Anonymous by design: never include RFID UID or student identity.
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(
            timespec="milliseconds"
        ).replace("+00:00", "Z"),
        "session_id": SESSION_ID,
        "feedback_type": feedback_type,
        "feedback_count": 1,
    }