import RPi.GPIO as GPIO
import time

# --- PINS ---
IN1, IN2, ENA = 17, 27, 18
DT, SCK = 5, 6

GPIO.setmode(GPIO.BCM)
GPIO.setup([IN1, IN2, ENA], GPIO.OUT)
# Initialize PWM on the Enable pin at 100Hz
pwm = GPIO.PWM(ENA, 100)
pwm.start(0)

# --- SPEED SETTINGS ---
CRAWL_SPEED = 25   # % speed
LAUNCH_SPEED = 100 # % speed
GENTLE_SPEED = 35  # % speed

def set_motor(speed, forward=True):
    pwm.ChangeDutyCycle(speed)
    GPIO.output(IN1, GPIO.HIGH if forward else GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW if forward else GPIO.HIGH)

def get_weight_sim():
    # Replace this with your actual hx.get_weight() later
    # For now, let's pretend it's heavy
    return 150

try:
    print("Step 1: Crawling to scale...")
    set_motor(CRAWL_SPEED)
    time.sleep(3) # Time it takes to reach the center

    print("Step 2: Stopping for measurement...")
    set_motor(0)
    time.sleep(1)
    weight = get_weight_sim()
    print(f"Weight detected: {weight}g")

    if weight < 50:
        print("Step 3: LIGHT OBJECT - LAUNCHING!")
        set_motor(LAUNCH_SPEED)
        time.sleep(1.5) # High speed burst
    else:
        print("Step 3: HEAVY OBJECT - GENTLE DROP")
        set_motor(GENTLE_SPEED)
        time.sleep(3.0) # Slow roll

    set_motor(0)
    print("Cycle Complete.")

except KeyboardInterrupt:
    pwm.stop()
    GPIO.cleanup()
