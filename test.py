# GPIO-Bibliothek laden
import RPi.GPIO as GPIO
import time

# BCM-Nummerierung verwenden
GPIO.setmode(GPIO.BCM)

pin = 23

GPIO.setup(pin, GPIO.OUT)

GPIO.output(pin, True)
time.sleep(1)

GPIO.output(pin, False)
time.sleep(1)

# Benutzte GPIOs freigeben
GPIO.cleanup()