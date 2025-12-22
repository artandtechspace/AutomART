try:
    from board import I2C
    from adafruit_motor.servo import Servo
    from adafruit_pca9685 import PCA9685
except:
    print("[WARNING] Using emulator for Adagruit_PCA9685 because the real library can't be found.")

    class I2C:
        pass

    class PCA9685:
        def __init__(self, i2d, address):
            self.frequency: int = 50
            self.channels = [i for i in range(16)]

    class Servo:
        def __init__(self, channel):
            self.angle: float = 0