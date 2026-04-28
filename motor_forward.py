import RPi.GPIO as GPIO
import time

# --- CONFIGURATION ---
# Ensure these match your actual jumper wires on the T-Cobbler
IN1 = 17
IN2 = 27
ENA = 18

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

# Enable the motor (High = On)
GPIO.output(ENA, GPIO.HIGH)

def motor_forward():
    print("Motor is running FORWARD... (Press Ctrl+C to stop)")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

try:
    motor_forward()
    while True:
        # Keeping the script alive
        time.sleep(1)

except KeyboardInterrupt:
    print("\nStopping Motor and Cleaning up...")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.cleanup()
