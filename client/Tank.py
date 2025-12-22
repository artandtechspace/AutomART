from apis.GPIOAPi import GPIO

# Config
PIN_TANK = 13

# Variables
state: bool = False

# region: External access

def setupTank():
    GPIO.setup(PIN_TANK, GPIO.OUT)
    GPIO.output(PIN_TANK, GPIO.LOW)

def turn_tank(on: bool):
    global state
    GPIO.output(PIN_TANK, GPIO.HIGH if on else GPIO.LOW)
    state = on

def loopTank():
    pass


def collect_status():
    global state
    return state

# endregion