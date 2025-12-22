from client.apis.ServoBoardAPI import I2C, PCA9685, Servo


# Config
PCA_FREQUENCY = 50
PCA_I2C_ADDRESS = 65

TANK_ON_ANGLE = 0
TANK_OFF_ANGLE = 180


# Values to access the Servo (API)
i2c: I2C = None
pca: PCA9685 = None
servo: Servo = None

status: bool = False

# region: External access

def setupTank():
    global i2c, pca, servo

    i2c = I2C()
    pca = PCA9685(i2c, address=PCA_I2C_ADDRESS)
    pca.frequency = PCA_FREQUENCY

    servo = Servo(pca.channels[0])
    servo.angle = 0

def turn_tank(on: bool):
    global servo, status
    servo.angle = TANK_ON_ANGLE if on else TANK_OFF_ANGLE
    status = on

def loopTank():
    pass

def collect_status():
    global status
    return status

# endregion