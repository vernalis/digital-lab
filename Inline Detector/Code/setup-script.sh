#!/bin/bash

sudo apt-get update \
 && sudo apt-get install python3-pip libatlas3-base -y \
 && sudo pip3 install --upgrade --no-input \
  adafruit-python-shell \
  adafruit-circuitpython-as7341 \
  matplotlib \
  numpy \
  pandas \
 && wget https://raw.githubusercontent.com/vernalis/digital-lab/main/Inline%20Detector/Code/inline_detector.py \
 && wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py \
 && sudo python3 raspi-blinka.py \
