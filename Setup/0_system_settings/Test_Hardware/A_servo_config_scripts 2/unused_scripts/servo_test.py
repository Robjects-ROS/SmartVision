import RPi.GPIO as GPIO
import time

# Set the pin for the servo
servo_pin = 17

# Set up the GPIO library
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Set up the servo and start it
servo = GPIO.PWM(servo_pin, 50)  # 50 Hz frequency
servo.start(0)  # Initial duty cycle of 0
