# main_autonomous.py
# Autonomous robot operation with forward, pause, and backward sequence

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
led_pwm.start(0)
servo_pwm.start(7.5)

# Ultrasonic sensor setup
ultrasonic = DistanceSensor(echo=PINS["ultrasonic_echo"], trigger=PINS["ultrasonic_trigger"])
lcd.lcd_init()

def display_message(line1, line2=""):
    lcd.printer(line1, line2)

def headlights(on=True):
    GPIO.output(PINS["headlight_left"], on)
    GPIO.output(PINS["headlight_right"], on)

def measure_distance():
    distance = round(ultrasonic.distance * 100, 1)
    display_message("Distance:", f"{distance} cm" if 0.5 < distance < 400 else "Out of Range")
    return distance

def forward(seconds):
    headlights(True)
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

try:
    # Initialization
    led_pwm.ChangeDutyCycle(40)
    display_message("Hello")
    time.sleep(2)
    lcd.printer("", "")

    # Moving Forward
    buzzer_pwm.start(50)
    time.sleep(2)
    buzzer_pwm.stop()
    led_pwm.ChangeDutyCycle(80)
    forward(4)

    # Measure distance and adjust servo
    for _ in range(4):
        measure_distance()
        time.sleep(1)
    servo_pwm.ChangeDutyCycle(5)
    time.sleep(1)

    # Pause
    headlights(False)
    led_pwm.ChangeDutyCycle(0)
    display_message("Pause")
    time.sleep(4)
    lcd.printer("", "")

    # Moving Backward
    buzzer_pwm.ChangeFrequency(500)
    buzzer_pwm.start(30)
    time.sleep(2)
    buzzer_pwm.stop()
    led_pwm.ChangeDutyCycle(60)
    backward(4)

    # Shutdown
    display_message("Goodbye")
    led_pwm.stop()
    time.sleep(2)
    lcd.printer("", "")

except KeyboardInterrupt:
    display_message("Interrupted", "by user")

finally:
    display_message("Cleaning up...")
    time.sleep(2)
    lcd.printer("", "")
    lcd.cleanup()
    headlights(False)
    GPIO.cleanup()
