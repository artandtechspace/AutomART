'''
Control the Brightness of LED using PWM on Raspberry Pi
http://www.electronicwings.com
'''

import RPi.GPIO as GPIO
from time import sleep

# Vorbereiten
ledpin = 32
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)		#set pin numbering system
GPIO.setup(ledpin,GPIO.OUT)
pi_pwm = GPIO.PWM(ledpin,1000)		#create PWM instance with frequency
pi_pwm.start(0)				#start PWM of required Duty Cycle

ledpin2 = 37
GPIO.setup(ledpin2,GPIO.OUT)





# Was soll er machen
GPIO.output(ledpin2,GPIO.LOW)
for duty in range(0,101,1):
    pi_pwm.ChangeDutyCycle(duty) #provide duty cycle in the range 0-100
    sleep(0.1)
    print(duty)
sleep(2)

for duty in range(100,-1,-1):
    pi_pwm.ChangeDutyCycle(duty)
    sleep(0.1)
    print(duty)
sleep(2)
GPIO.output(ledpin2,GPIO.HIGH)

for duty in range(0,101,1):
    pi_pwm.ChangeDutyCycle(duty) #provide duty cycle in the range 0-100
    sleep(0.1)
    print(duty)
sleep(2)

for duty in range(100,-1,-1):
    pi_pwm.ChangeDutyCycle(duty)
    sleep(0.1)
    print(duty)
sleep(2)
GPIO.output(ledpin2,GPIO.HIGH)

