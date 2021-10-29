"""A Raspberry Pi based thermocouple that logs datapoints to a csv file."""

import csv
import os
import sys
from datetime import date, datetime
from time import sleep

import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import adafruit_max31855
import board
import busio
import digitalio
import RPi.GPIO as IO

# Setup thermocouple interface
# Ref https://learn.adafruit.com/thermocouple/python-circuitpython
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.D5)
max31855 = adafruit_max31855.MAX31855(spi, cs)

# Setup LCD screen
# Ref https://learn.adafruit.com/rgb-lcd-shield/circuitpython
lcd_columns = 16
lcd_rows = 2

# Initialise I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialise the LCD class
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
lcd.clear()

# Define log file location. Default to user home folder, but allow overriding via:
# - Command line argument provided to script
# - VER_THERM_LOG environment variable
folder = os.path.expanduser("~")
if len(sys.argv) >= 2:
    folder = sys.argv[1]
elif "VER_THERM_LOG" in os.environ:
    folder = os.environ["VER_THERM_LOG"]

filename = str((datetime.now().isoformat(timespec='seconds')))+".csv"
file = folder + filename

# Create header row
with open(file,'a',newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['Date', 'Time', 'Temp_c'])

# Count number of thermocouple read attempts
try_count = 0

# GPIO17 as an input pin, watching for reset button being pressed
# If reset button closed (pressed) then returns False
# Set up GPIO pins
# Do not show any GPIO warnings
IO.setwarnings(False)
# Programming the GPIO by BCM pin numbers (PIN11 as ‘GPIO17’)
IO.setmode(IO.BCM)
IO.setup(17, IO.IN, pull_up_down=IO.PUD_UP)

# Main datalogging loop
while True:
    # Variable to report reset button status
    button_open = IO.input(17)
    if button_open == False:
        break

    # Get temp, monitor error in reading sensor (~1.3% failure rate)
    try:
        tempC = max31855.temperature
        # Append temp to file with timestamp
        with open(file,'a',newline='') as f:
            writer = csv.writer(f, delimiter=',')
            date_str = str(date.today())
            time_str = datetime.now().strftime('%H:%M:%S')
            writer.writerow([date_str, time_str, tempC])
        try_count = 0
        lcd.clear()
        lcd.message = "Temp: {}".format(tempC)
        print(tempC)
    except RuntimeError:
        try_count = try_count+1
        print(try_count)
        # If 3 consecutive fails, probably a real error
        if try_count < 3:
            pass
        else:
            raise
    else:
        # Wait for next timepoint (15s)
        sleep(15)
