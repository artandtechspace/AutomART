from apis.ServoBoardAPI import I2C, PCA9685, Servo


# Config
PCA_FREQUENCY = 50
PCA_I2C_ADDRESS = 65

PUMP_ON_ANGLE = 0
PUMP_OFF_ANGLE = 180


# Values to access the Servo (API)
i2c: I2C = None
pca: PCA9685 = None
servo: Servo = None


# region: External access

def setupPump():
    global i2c, pca, servo

    i2c = I2C()
    pca = PCA9685(i2c, address=PCA_I2C_ADDRESS)
    pca.frequency = PCA_FREQUENCY

    servo = Servo(pca.channels[0])
    servo.angle = 0

def turn_pump(on: bool):
    global servo
    servo.angle = PUMP_ON_ANGLE if on else PUMP_OFF_ANGLE

def loopPump():
    pass

def collect_status():
    return servo.angle == PUMP_ON_ANGLE

# endregion