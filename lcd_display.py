import time
import smbus2
from RPLCD.i2c import CharLCD

# --- PREDICTED WEIGHTS (Grams) ---
# A 4x4x0.75 inch pine block is roughly 80-100g.
# An AirPod Pro case is exactly 45.6g.
BLOCK_WEIGHT = 92.40
AIRPOD_CASE = 45.60
TOTAL_WEIGHT = BLOCK_WEIGHT + AIRPOD_CASE

# --- LCD SETUP ---
# Address is usually 0x27. If it fails, try 0x3f.
try:
    lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
                  cols=16, rows=2, dotsize=8)
except:
    print("LCD not found at 0x27, trying 0x3f...")
    lcd = CharLCD(i2c_expander='PCF8574', address=0x3f, port=1,
                  cols=16, rows=2, dotsize=8)

def display_weight(label, value):
    lcd.clear()
    lcd.write_string(f"{label}")
    lcd.cursor_pos = (1, 0) # Move to second line
    lcd.write_string(f"Weight: {value:.2f}g")

try:
    print("Starting Demo...")

    # Step 1: Display Wooden Block
    display_weight("Wooden Block", BLOCK_WEIGHT)
    print(f"Displaying Block: {BLOCK_WEIGHT}g")

    time.sleep(2) # Wait 2 seconds

    # Step 2: Display Block + Airpod Case
    display_weight("Block + AirPods", TOTAL_WEIGHT)
    print(f"Displaying Total: {TOTAL_WEIGHT}g")

except KeyboardInterrupt:
    lcd.clear()
    print("\nDemo Ended.")
