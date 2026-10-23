# IIoT Real-Time Class Feedback System

Python starter implementation based on the uploaded report.

## Hardware pin map (BCM)
- Buttons: UNDERSTOOD GPIO 17, CONFUSED GPIO 22, SLOW_DOWN GPIO 27, NEED_EXAMPLE GPIO 23
- LEDs: green GPIO 24, red GPIO 25, yellow GPIO 12, blue GPIO 15
- Active buzzer: GPIO 18
- RFID reader: SPI (depends on exact reader module)
- LCD: I2C (verify address and library for your module)

Each button connects between its GPIO pin and GND; internal pull-ups are enabled. Use a 330-ohm series resistor for each LED. Raspberry Pi GPIO is 3.3 V only. Do not connect 5 V signals directly to GPIO; use a suitable driver for a buzzer if needed.

## Run
1. Copy `.env.example` to `.env` and add your Power BI HTTPS push URL.
2. On a laptop: `pip install -r requirements.txt` then `python main.py --simulate`
3. On Raspberry Pi OS: install the supported GPIO package, install requirements, then `python main.py`
4. Tests: `python -m unittest discover -s tests -v`

Power BI endpoint schema and APIs can vary. Configure the streaming/push dataset in your own tenant. Keep `.env` secret and never commit it.

RFID and LCD driver integrations are separated because the report does not identify exact modules. The attendance helper counts unique scans during the running session and does not store UIDs in the database or attach identities to feedback.

Performance numbers in the report should be independently measured on the actual prototype; this starter code does not establish those reported results.
