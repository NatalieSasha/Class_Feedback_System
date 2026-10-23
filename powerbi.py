import logging
import requests
from config import POWERBI_PUSH_URL, REQUEST_TIMEOUT_SECONDS

log = logging.getLogger(__name__)

class PowerBIClient:
    def __init__(self, push_url: str = POWERBI_PUSH_URL):
        self.push_url = push_url

    def send(self, event: dict) -> bool:
        if not self.push_url:
            log.warning("POWERBI_PUSH_URL is not configured; event remains queued.")
            return False
        try:
            # Common streaming push format: JSON array containing one event row.
            response = requests.post(
                self.push_url,
                json=[event],
                headers={"Content-Type": "application/json"},
                timeout=REQUEST_TIMEOUT_SECONDS,
            )
            if 200 <= response.status_code < 300:
                return True
            log.error("Power BI rejected event: HTTP %s; response=%s",
                      response.status_code, response.text[:300])
            return False
        except requests.RequestException as exc:
            log.warning("Power BI transmission failed: %s", exc)
            return False
