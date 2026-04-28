import RPi.GPIO as GPIO
import time
import sys

# --- CONFIGURATION ---
DT_PIN = 5
SCK_PIN = 6

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SCK_PIN, GPIO.OUT)
GPIO.setup(DT_PIN, GPIO.IN)

def read_hx711():
    # Wait for DT to go LOW (indicates data is ready)
    timeout = 0
    while GPIO.input(DT_PIN) == 1:
        timeout += 1
        if timeout > 10000: return None # Chip not responding

    data = 0
    # Read 24 bits of data
    for i in range(24):
        GPIO.output(SCK_PIN, True)
        data = (data << 1) | GPIO.input(DT_PIN)
        GPIO.output(SCK_PIN, False)

    # 25th pulse sets the gain for next time (128 gain)
    GPIO.output(SCK_PIN, True)
    GPIO.output(SCK_PIN, False)

    # Handle 2's complement (negative numbers)
    if data & 0x800000:
        data -= 0x1000000
    return data

def main():
    print("Reading RAW data directly from pins... (No Library)")
    # Get a baseline offset
    print("Taring...")
    samples = []
    for _ in range(10):
        val = read_hx711()
        if val is not None: samples.append(val)
        time.sleep(0.1)

    offset = sum(samples) / len(samples) if samples else 0
    print(f"Offset: {offset}")

    try:
        while True:
            raw = read_hx711()
            if raw is not None:
                print(f"Raw: {raw} | Adjusted: {raw - offset}")
            else:
                print("Error: HX711 not responding. Check wiring!")
            time.sleep(0.2)
    except KeyboardInterrupt:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
