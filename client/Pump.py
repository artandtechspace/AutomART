from client.apis.GPIOAPi import GPIO

# Config
PIN_PUMP = 27

# Variables
state: bool = False

# region: External access

def setupPump():
    GPIO.setup(PIN_PUMP, GPIO.OUT)
    GPIO.output(PIN_PUMP, GPIO.LOW)

def turn_pump(on: bool):
    global state
    GPIO.output(PIN_PUMP, GPIO.HIGH if on else GPIO.LOW)
    state = on

def loopPump():
    pass


def collect_status():
    global state
    return state

# endregion

