class AttendanceCounter:
    # Counts unique tag scans in memory only. Never persists UIDs or links them to feedback.
    def __init__(self):
        self.present_count = 0
        self._seen_in_session = set()

    def register_scan(self, uid: str) -> int:
        normalized = str(uid).replace(" ", "").upper()
        if normalized and normalized not in self._seen_in_session:
            self._seen_in_session.add(normalized)
            self.present_count += 1
        return self.present_count

class LCDDisplay:
    # Replace this method with the library call for your exact I2C LCD module.
    def show_message(self, line1: str, line2: str = ""):
        print(f"[LCD] {line1} {line2}".strip())
