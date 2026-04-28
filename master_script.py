import RPi.GPIO as GPIO
import time
from RPLCD.i2c import CharLCD

# --- PINS ---
IN1, IN2, ENA = 17, 27, 18
DT_PIN, SCK_PIN = 5, 6
LCD_ADDR = 0x27

# --- MOTOR SETTINGS ---
CRAWL_SPEED = 30
LAUNCH_SPEED = 100
GENTLE_SPEED = 40

# --- INITIALIZATION ---
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup([IN1, IN2, ENA, SCK_PIN], GPIO.OUT)
GPIO.setup(DT_PIN, GPIO.IN)

pwm = GPIO.PWM(ENA, 100)
pwm.start(0)

try:
    lcd = CharLCD('PCF8574', LCD_ADDR)
except:
    lcd = None
    print("LCD not found. Continuing in terminal mode.")

def read_hx711():
    """Manual 24-bit read from HX711"""
    timeout = 0
    while GPIO.input(DT_PIN) == 1:
        timeout += 1
        if timeout > 20000: return None 

    data = 0
    for i in range(24):
        GPIO.output(SCK_PIN, True)
        data = (data << 1) | GPIO.input(DT_PIN)
        GPIO.output(SCK_PIN, False)

    # 25th pulse for 128 gain
    GPIO.output(SCK_PIN, True)
    GPIO.output(SCK_PIN, False)

    if data & 0x800000:
        data -= 0x1000000
    return data

def set_motor(speed, forward=True):
    pwm.ChangeDutyCycle(speed)
    if forward:
        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
    else:
        GPIO.output(IN1, GPIO.HIGH)
        GPIO.output(IN2, GPIO.LOW)

def get_stable_weight(offset, samples=5):
    """Averages multiple readings for a clean result"""
    vals = []
    for _ in range(samples):
        raw = read_hx711()
        if raw is not None:
            vals.append(raw - offset)
        time.sleep(0.05)
    return sum(vals) / len(vals) if vals else 0

def update_display(line1, line2=""):
    print(f"{line1} | {line2}")
    if lcd:
        lcd.clear()
        lcd.write_string(f"{line1}\n{line2}")

def main():
    update_display("System Booting", "Taring...")
    
    # Tare: Get baseline
    readings = []
    for _ in range(20):
        val = read_hx711()
        if val is not None: readings.append(val)
        time.sleep(0.05)
    
    offset = sum(readings) / len(readings) if readings else 0
    update_display("Ready", "Place Object")

    try:
        while True:
            # 1. Start moving object to scale
            set_motor(CRAWL_SPEED)
            update_display("Moving to Scale")
            time.sleep(2.5) # Adjust based on your belt length

            # 2. Stop and Measure
            set_motor(0)
            update_display("Measuring...")
            time.sleep(1.0)
            
            # Use raw units for thresholding initially
            weight_units = get_stable_weight(offset)
            
            # THRESHOLD: Adjust '5000' based on your actual raw readings
            # (Check terminal while running to see what your objects weigh)
            is_light = weight_units < 5000 
            
            status = "LIGHT" if is_light else "HEAVY"
            update_display(f"Detected: {status}", f"Val: {int(weight_units)}")
            time.sleep(1)

            # 3. Action
            if is_light:
                update_display("LAUNCHING!")
                set_motor(LAUNCH_SPEED)
                time.sleep(1.5)
            else:
                update_display("GENTLE DROP")
                set_motor(GENTLE_SPEED)
                time.sleep(3.0)

            set_motor(0)
            update_display("Cycle Done", "Waiting...")
            time.sleep(3)

    except KeyboardInterrupt:
        pwm.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
