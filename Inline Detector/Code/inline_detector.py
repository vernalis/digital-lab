"""A Raspberry Pi / Adafruit AS7341 based inline detector.

- Outputs a live absorbance graph
- Stores a csv file
- Stores a png image

"""

import os
from datetime import datetime
from time import sleep

import board
from adafruit_as7341 import AS7341
from RPi import GPIO

import matplotlib.pyplot as plt
import pandas as pd


# See https://docs.circuitpython.org/projects/as7341/en/latest/index.html
# for AS7341 documentation
# Setup i2c sensor interface
i2c = board.I2C()
sensor = AS7341(i2c)


# Create a 1-row dataframe with all channel data and timestamp
def sensor_data():
    """Retrieve data from AS7341 and store in a dataframe against current timepoint."""
    # Get main channel data stream, plus additional manual channels
    sensor_channels = sensor.all_channels
    ir = sensor.channel_nir
    clear = sensor.channel_clear

    # Combine all channel data
    new_readings_list = list(sensor_channels)
    new_readings_list.append(ir)
    new_readings_list.append(clear)

    # Get data timepoint
    timepoint = datetime.now()

    # Store results in a dataframe
    new_readings_df = pd.DataFrame(
        [new_readings_list],
        columns=[415, 445, 480, 515, 555, 590, 630, 680, "IR", "Clear"],
        index=[timepoint],
    )
    return new_readings_df


# LED PWM setup
# Prevent warnings
GPIO.setwarnings(False)
# BCM pin labelling system
GPIO.setmode(GPIO.BCM)
# Pin 13 aka 33 (PWM)
GPIO.setup(13, GPIO.OUT)
# GPIO13 as PWM output, with 100Hz frequency
pwm_output = GPIO.PWM(13, 100)
# Generate PWM signal with a duty cycle
pwm_output.start(100)

# Define location for data to be stored
# Output raw and normalised data as csv file
# Output png image of graph at the end of the experiment
FOLDER = os.path.join(os.getcwd(), "data", "")
if not os.path.isdir(FOLDER):
    os.mkdir(FOLDER)
# Filename contains start datetime of experiment
START_TIME = str(datetime.now().isoformat(timespec="seconds"))
RUN_ID = START_TIME + ".csv"
NORM_RUN_ID = START_TIME + "_norm.csv"
IMG_ID = START_TIME + "_norm.png"
FILENAME = FOLDER + RUN_ID
NORM_FILENAME = FOLDER + NORM_RUN_ID
IMG_FILENAME = FOLDER + IMG_ID

# Create dataframe for sensor readings
readings = pd.DataFrame()

# Take 3 readings to generate a baseline value for each channel
# this baseline will then be subtracted from the raw sensor data
# normalising all wavelengths, making absorbance changes easier to spot
print("Getting baseline readings...")

# Get 3 readings
for n in range(3):
    # Get new sensor data and append to the data table
    new_data = sensor_data()
    readings = pd.concat([readings, new_data])
    print("Reading " + str(n + 1) + " of 3 taken")
    if n < 2:
        sleep(2.5)

# Caculate mean value at each wavelength - the baseline
baseline = readings.mean()
print("Baseline calculated")

# Calculate normalised readings (i.e. reading minus the mean baseline)
norm_readings = readings.sub(baseline)

# Create interactive plot for data to fall into as acquired
# noqa: Ref https://stackoverflow.com/questions/66943917/is-there-a-way-to-update-the-matplotlib-plot-without-closing-the-window
fig = plt.figure(num=1, figsize=[10, 10])
plt.ion()

# Set colours for each wavelegnth (same order as columns)
plt.gca().set_prop_cycle(
    color=[
        "purple",
        "blue",
        "aqua",
        "green",
        "lime",
        "yellow",
        "goldenrod",
        "red",
        "black",
        "silver",
    ]
)

# Plot initial data
plt.plot(norm_readings.index, norm_readings, label=norm_readings.columns)
plt.legend(bbox_to_anchor=(0.0, 1.0, 1.0, 0.0), loc="lower left", ncol=5, mode="expand")
plt.tick_params(axis="x", labelrotation=45)
plt.show()


# Create a function to handle exit and shutdown of the process
def on_close(event):
    """Triggered when figure window is closed, causing shutdown procedure to begin."""
    global loop
    print("Shutdown initiated")
    loop = False


# Watch for closure of the graph - indicating end requested
fig.canvas.mpl_connect("close_event", on_close)

# Variable to flag when shutdown activated and to stop the loop
loop = True

# Get regular sensor readings
while True:
    # Get new sensor data, normalise and append to the data table
    new_data = sensor_data()
    norm_new_data = new_data.sub(baseline)
    readings = pd.concat([readings, new_data])
    norm_readings = pd.concat([norm_readings, norm_new_data])
    # Store raw and normalised data as csv
    readings.to_csv(FILENAME)
    norm_readings.to_csv(NORM_FILENAME)

    # Refresh data in chart
    plt.plot(norm_readings.index, norm_readings, label=norm_readings.columns)

    # Check if shutdown procedure has been activated
    # If activated, ouput final chart as a png image
    if loop is False:
        # Prepare output plot - need to reapply settings for png generation
        plt.gca().set_prop_cycle(
            color=[
                "purple",
                "blue",
                "aqua",
                "green",
                "lime",
                "yellow",
                "goldenrod",
                "red",
                "black",
                "silver",
            ]
        )
        plt.plot(norm_readings.index, norm_readings, label=norm_readings.columns)
        plt.legend(
            bbox_to_anchor=(0.0, 1.0, 1.0, 0.0), loc="lower left", ncol=5, mode="expand"
        )
        plt.tick_params(axis="x", labelrotation=45)
        # Generate png image of the final graph
        plt.savefig(IMG_FILENAME)
        # Turn off LED
        pwm_output.stop()
        GPIO.cleanup()
        # Exit the while loop
        break

    # Draw chart, wait before next datapoint
    plt.pause(2.5)

# Confirm while loop exited, and png image generated
print("Shutdown complete")
