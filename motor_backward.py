import RPi.GPIO as GPIO
import time

# --- CONFIGURATION ---
IN1 = 17
IN2 = 27
ENA = 18

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# Set speed to HIGH
GPIO.output(ENA, GPIO.HIGH)

def motor_backward():
    print("Motor is running BACKWARD... (Press Ctrl+C to stop)")
    # Flip the signals from the forward script
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

try:
    motor_backward()
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping Motor and Cleaning up...")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.cleanup()
