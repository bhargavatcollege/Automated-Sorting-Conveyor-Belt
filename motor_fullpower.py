import RPi.GPIO as GPIO

IN1, IN2, ENA = 17, 27, 18

GPIO.setmode(GPIO.BCM)
GPIO.setup([IN1, IN2, ENA], GPIO.OUT)

# Setting speed to 100%
# (If you aren't using a PWM object, GPIO.HIGH is the same as 100%)
GPIO.output(ENA, GPIO.HIGH)

def max_speed_backwards():
    print("Running motor at MAX VOLTAGE backwards...")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

try:
    max_speed_backwards()
    input("Press Enter to Stop...") # Keeps it running until you hit Enter
finally:
    GPIO.cleanup()
