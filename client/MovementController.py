import math
from GPIOAPi import GPIO

# Config
PIN_RIGHT_SPEED = 32
PIN_LEFT_SPEED = 33

PIN_RIGHT_DIRECTION = 37
PIN_LEFT_DIRECTION = 36


SPEED_MODIFIER = 10 # 0 - 100




# PWM-API's
rightPWMAPI = None
leftPWMAPI = None

def setupMovement():
    global rightPWMAPI, leftPWMAPI
    print("GPIO", GPIO)
    # Setup board
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    # Configures the PWM-Pins
    GPIO.setup(PIN_RIGHT_SPEED, GPIO.OUT)
    rightPWMAPI = GPIO.PWM(PIN_RIGHT_SPEED, 1000)
    rightPWMAPI.start(0)

    GPIO.setup(PIN_LEFT_SPEED, GPIO.OUT)
    leftPWMAPI = GPIO.PWM(PIN_LEFT_SPEED, 1000)
    leftPWMAPI.start(0)

    # Configures direction Pins
    GPIO.setup(PIN_LEFT_DIRECTION, GPIO.OUT)
    GPIO.setup(PIN_RIGHT_DIRECTION, GPIO.OUT)


def calculate_x_y_from_angle_and_speed(angle, speed):
    nY = speed * math.sin(angle)

    if nY < 0:
        angle = -angle

    nX = speed * math.cos(angle)
    

    left = nX - nY
    right = nX + nY

    left /= 1.415
    right /= 1.415
    
    l_rev = left < 0
    r_rev = right < 0

    left = int(abs(left) * 50)
    right = int(abs(right) * 50)

    return left, right, l_rev, r_rev

# -100 to 100 to
def setMovement(angle: int, speed: int):
    global rightPWMAPI, leftPWMAPI
    

    if -math.pi/8 < angle < math.pi/8:
        angle = 0

    left, right, l_rev, r_rev = calculate_x_y_from_angle_and_speed(angle, speed)

    GPIO.output(PIN_LEFT_DIRECTION, GPIO.HIGH if r_rev == 1 else GPIO.LOW)
    GPIO.output(PIN_RIGHT_DIRECTION, GPIO.HIGH if l_rev == 0 else GPIO.LOW)

    rightPWMAPI.ChangeDutyCycle(int(left))
    leftPWMAPI.ChangeDutyCycle(int(right))

    pass



def loopMovement():
    pass
