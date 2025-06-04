# main_user_controlled.py
# User-controlled robot with obstacle detection and PWM headlights

import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor
import lcd  # Custom LCD module

# Pin configuration
PINS = {
    "status_led": 19,
    "buzzer": 16,
    "servo": 21,
    "motor1_fwd": 5,
    "motor1_bwd": 0,
    "motor2_fwd": 7,
    "motor2_bwd": 6,
    "ultrasonic_trigger": 23,
    "ultrasonic_echo": 24,
    "headlight_left": 12,
    "headlight_right": 26
}

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for pin in PINS.values():
    GPIO.setup(pin, GPIO.OUT if pin != PINS["ultrasonic_echo"] else GPIO.IN)

# PWM setup
led_pwm = GPIO.PWM(PINS["status_led"], 500)
buzzer_pwm = GPIO.PWM(PINS["buzzer"], 1000)
servo_pwm = GPIO.PWM(PINS["servo"], 50)
headlight_pwm_left = GPIO.PWM(PINS["headlight_left"], 100)
headlight_pwm_right = GPIO.PWM(PINS["headlight_right"], 100)

led_pwm.start(0)
servo_pwm.start(7.5)
headlight_pwm_left.start(0)
headlight_pwm_right.start(0)

# Ultrasonic sensor setup
ultrasonic = DistanceSensor(echo=PINS["ultrasonic_echo"], trigger=PINS["ultrasonic_trigger"])
lcd.lcd_init()

def display_message(line1, line2=""):
    lcd.printer(line1, line2)

def set_headlights(intensity):
    headlight_pwm_left.ChangeDutyCycle(intensity)
    headlight_pwm_right.ChangeDutyCycle(intensity)

def measure_distance():
    distance = round(ultrasonic.distance * 100, 1)
    display_message("Distance:", f"{distance} cm" if 0.5 < distance < 400 else "Out of Range")
    return distance

def forward(seconds):
    set_headlights(100)
    GPIO.output(PINS["motor1_fwd"], GPIO.HIGH)
    GPIO.output(PINS["motor2_fwd"], GPIO.HIGH)
    display_message("Moving Forward")
    time.sleep(seconds)
    GPIO.output(PINS["motor1_fwd"], GPIO.LOW)
    GPIO.output(PINS["motor2_fwd"], GPIO.LOW)

def backward(seconds):
    GPIO.output(PINS["motor1_bwd"], GPIO.HIGH)
    GPIO.output(PINS["motor2_bwd"], GPIO.HIGH)
    display_message("Moving Backward")
    time.sleep(seconds)
    GPIO.output(PINS["motor1_bwd"], GPIO.LOW)
    GPIO.output(PINS["motor2_bwd"], GPIO.LOW)

def turn_left(seconds):
    GPIO.output(PINS["motor1_bwd"], GPIO.HIGH)
    GPIO.output(PINS["motor2_fwd"], GPIO.HIGH)
    display_message("Turning Left")
    time.sleep(seconds)
    GPIO.output(PINS["motor1_bwd"], GPIO.LOW)
    GPIO.output(PINS["motor2_fwd"], GPIO.LOW)

def turn_right(seconds):
    GPIO.output(PINS["motor1_fwd"], GPIO.HIGH)
    GPIO.output(PINS["motor2_bwd"], GPIO.HIGH)
    display_message("Turning Right")
    time.sleep(seconds)
    GPIO.output(PINS["motor1_fwd"], GPIO.LOW)
    GPIO.output(PINS["motor2_bwd"], GPIO.LOW)

try:
    # Initialization
    led_pwm.ChangeDutyCycle(40)
    display_message("Hello")
    time.sleep(2)
    lcd.printer("", "")

    # User input
    direction = input("Enter direction (forward, backward, left, right): ").strip().lower()
    intensity = int(input("Enter headlight intensity (0–100): ").strip())
    set_headlights(intensity)

    # Movement based on user input
    if direction == "forward":
        forward(2)
    elif direction == "backward":
        backward(2)
    elif direction == "left":
        turn_left(2)
    elif direction == "right":
        turn_right(2)
    else:
        display_message("Invalid Input", "Try Again")
        time.sleep(2)

    # Obstacle detection loop
    while True:
        distance = measure_distance()
        if distance < 10:
            display_message("Obstacle!", "Stopping...")
            buzzer_pwm.start(50)
            time.sleep(1)
            buzzer_pwm.stop()
            backward(1)
            turn_right(1)
        time.sleep(0.5)

except KeyboardInterrupt:
    display_message("Interrupted", "by user")

finally:
    headlight_pwm_left.stop()
    headlight_pwm_right.stop()
    display_message("Cleaning up...")
    time.sleep(2)
    lcd.printer("", "")
    lcd.cleanup()
    GPIO.cleanup()
