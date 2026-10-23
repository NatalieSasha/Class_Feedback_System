import time
from config import BUTTONS, BUZZER_PIN, BUZZER_DURATION_SECONDS, LED_DURATION_SECONDS

class RaspberryPiHardware:
    def __init__(self, on_feedback):
        try:
            import RPi.GPIO as GPIO
        except ImportError as exc:
            raise RuntimeError("RPi.GPIO unavailable. Use --simulate on a laptop or install compatible GPIO support on Raspberry Pi OS.") from exc
        self.GPIO = GPIO
        self.on_feedback = on_feedback
        self._last_event = {}
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for button_pin, (_, led_pin) in BUTTONS.items():
            GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(BUZZER_PIN, GPIO.OUT, initial=GPIO.LOW)
        for button_pin in BUTTONS:
            GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=self._button_callback, bouncetime=50)

    def _button_callback(self, channel):
        feedback_type, led_pin = BUTTONS[channel]
        now = time.monotonic()
        if now - self._last_event.get(channel, 0) < 0.05:
            return
        self._last_event[channel] = now
        self.GPIO.output(led_pin, self.GPIO.HIGH)
        self.GPIO.output(BUZZER_PIN, self.GPIO.HIGH)
        try:
            self.on_feedback(feedback_type)
        finally:
            time.sleep(BUZZER_DURATION_SECONDS)
            self.GPIO.output(BUZZER_PIN, self.GPIO.LOW)
            time.sleep(max(0, LED_DURATION_SECONDS - BUZZER_DURATION_SECONDS))
            self.GPIO.output(led_pin, self.GPIO.LOW)

    def close(self):
        self.GPIO.cleanup()

class SimulatedHardware:
    def __init__(self, on_feedback):
        self.on_feedback = on_feedback

    def run(self):
        print("Simulation mode: enter 1-4 to submit feedback; q to quit.")
        for key, label in {"1": "UNDERSTOOD", "2": "CONFUSED", "3": "SLOW_DOWN", "4": "NEED_EXAMPLE"}.items():
            print(f"  {key}: {label}")
        while True:
            try:
                value = input("> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                break
            if value == "q":
                break
            options = {"1": "UNDERSTOOD", "2": "CONFUSED", "3": "SLOW_DOWN", "4": "NEED_EXAMPLE"}
            if value in options:
                self.on_feedback(options[value])
            else:
                print("Choose 1, 2, 3, 4, or q.")
