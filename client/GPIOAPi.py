try:
    import RPi.GPIO as GPIO
except:
    class DummyPWM:

        def __init__(self, name = "unnamed"):
            self.name = name

        def ChangeDutyCycle(self, cycle):
            print(f"Cycle[{self.name}] = {cycle}")
            pass
        def start(self, cycle):
            pass

    # Creates a dummy GPIO for when the lib is not installed
    # bc. the script is not run on a pi
    class GPIO:

        LOW = 0
        HIGH = 1
        OUT = 2
        BOARD = 10

        @staticmethod
        def setwarnings(mode):
            pass

        @staticmethod
        def setmode(mode):
            pass

        @staticmethod
        def output(pin, mode):
            pass

        @staticmethod
        def setup(pin, mode):
            pass

        @staticmethod
        def PWM(pin, freq):
            return DummyPWM(pin)
    pass
