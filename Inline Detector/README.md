# Raspberry Pi / Adafruit AS7341 Based Inline Detector

*Add DOI shield here on publication* [![License: MIT](https://img.shields.io/badge/License-MIT-green)](../LICENSE)

## Overview
A Raspberry Pi based inline detector, using an Adafruit AS7341 sensor. Allowing detection of slugs within a flow chemistry system, through differing visible light absorbance. 

|![Pi_Detector][overview_img]|![Graph_Output][graph_img]|
| --- | ---| 
|The completed device - Raspberry Pi and detector shown|Graphical output from the detector|


[overview_img]: Completed_Detector.jpg
[graph_img]: Validation_Test_Result.png


## Publication
Details about the design and development of the device can be found in the accompanying paper. A step-by-step guide to building your own is given in the supplementary information. 

[Paper][Paper] | [Supplementary Information][si]

If you have used this project as a resource in your research, please cite:

>Citation to be added here on publication

[paper]: 2023%20Maddox%20Inline%20Detector%20Paper.pdf
[si]: 2023%20Maddox%20Inline%20Detector%20Supplementary%20Information.pdf

## Bill of Materials
The following components are required to construct our design. The supplier we used is provided, however parts should be available from alternative suppliers too. 

| Name | Catalogue Number | Supplier | Quantity | Total Price (£) |
| ------ | ------ | ------ | ------ | ------ |
|Raspberry Pi 4 Model B	| SC0192 | Thepihut.com | 1 | 40.00 |
|32 Gb MicroSD Card | SD-32GB | Thepihut.com | 1 | 8.00 |
|Adafruit AS7341 10-Channel Light / Color Sensor Breakout (STEMMA QT / Qwiic) | ADA4698 | Thepihut.com | 1 |15.60
|5mm White LED (forward voltage 3.4V, forward current 30mA) | Components within ELEGOO Upgraded Electronics Fun Kit (ASIN: B01LZRV539) | Amazon.co.uk | 1 |16.99 |
|NPN Transistor (PN2222)			|Components within ELEGOO Upgraded Electronics Fun Kit (ASIN: B01LZRV539)| Amazon.co.uk | 1 |N/A|	
|10 kΩ Resistor			|Components within ELEGOO Upgraded Electronics Fun Kit (ASIN: B01LZRV539)| Amazon.co.uk |2|N/A|	
|1 kΩ Resistor			|Components within ELEGOO Upgraded Electronics Fun Kit (ASIN: B01LZRV539)| Amazon.co.uk |1|N/A|	
|Sparkfun RJ45 8-Pin Connector | PRT-00643 | Pimoroni.com | 2 | 3.00 |
|Sparkfun RJ45 Breakout | BOB-00716 | Pimoroni.com | 2 | 2.40 |
|2x20 pin Female GPIO Header for Raspberry Pi| COM0001 |Pimoroni.com | 1 | 1.50 |
|Custom PCB for detector module (price for minimum order of 3 boards shown) | HRKGEPJB (https://aisler.net/p/HRKGEPJB) | Aisler.net | 1 | 6.17 |
|Custom PCB for Raspberry Pi HAT (price for minimum order of 3 boards shown) | QVZTMZVR (https://aisler.net/p/QVZTMZVR) | Aisler.net |1 | 7.55|
| PLA Filament for detector module | 832-0264 | uk.rs-online.com/web | 2.7 p/g (prorated price), 37 g used | 1.00 |
| PP Filament for Raspberry Pi case feet | 174-0057 | uk.rs-online.com/web | 5.6 p/g (prorated price), 1 g used | 0.06 |
| PETG Filament for Raspberry Pi case | 190-1962 | uk.rs-online.com/web | 3.5 p/g (prorated price), 53 g used | 1.86 |
| Low profile (flat) LAN cable, 1m | Widely available, e.g. ASIN: B0B6WC6MRB | Amazon.co.uk | 1	| 2.00 |
| 1/16th inch o/d PTFE tubing, with ¼-28” connection at either end | Various suppliers | Various suppliers | Approx. 15cm required | Cost negligible |
||||Combined Total | £106.13 |

## Repository Contents
This repository contains the following assets to enable reproduction of the device:
* Original publication - full documentation for the device is provided within the paper and supplementary information
* 3D Printer .stl Files - files for both the detector and Raspberry Pi housing
* PCB Gerber Files - to allow manufacture of custom PCBs with alternative suppliers
* Python code used to operate the device (inline_detector.py)

### 3D Printer .stl Files
Files are separated into two folders - components for the Raspberry Pi case, and components for the detector housing.

The Raspberry Pi case is a modified version of [a publicly available Raspberry Pi 4 case](https://www.thingiverse.com/thing:3723561), modified to accommodate the custom HAT designed for this project.  

All Pi case components were printed in PETG due to the higher thermal tolerance, apart from the legs - which were printed in PP due to the higher solvent resistance.

The detector housing parts were all printed in PLA. Take care to print interlocking parts in the same orientation on the print bed to ensure a good fit. 

See Supplementary Information section S4 for further details, such as printer settings. 

### PCB Gerber Files
Zipped Gerber files are provided to allow manufacture of the custom PCBs at a supplier of your choice. 

Alternatively, for convenience, use the following links to use the same supplier as we did. After registration, simply import the designs into your sandbox and order. A minimum order quantity of 3 is required, however the price is minimal. 

[HAT PCB](https://aisler.net/p/QVZTMZVR)

[Detector PCB](https://aisler.net/p/HRKGEPJB)

See Supplementary Information section S3 for further details on circuit design. See Supplementary Information section S5 for PCB assembly.

**Note:** The HAT PCB available at publication has undergone a minor revision to the board shown in the publication. This revision decreases the board size by ~1.5mm, allowing compatibility with the Raspberry Pi Zero platform. 

### Raspberry Pi Configuration and Operation

A Raspberry Pi running Raspberry Pi OS Bullseye was used. VNC and I2C interfaces were enabled. 

The following python libraries were installed:
* CircuitPython (Blinka) by Adafruit for interfacing with their products
* adafruit-circuitpython-as7341 for the sensor device itself
* matplotlib for graphical representation of the sensor data
* pandas for data processing

Once configured, operating the Raspberry Pi through VNC to allow a graphical interface, inline_detector.py can be run. After 3 initial baseline readings a graphical output of the sensor data is shown. This then updates every 2.5s with the next datapoint. Data is saved in a .csv file at each update. 

At the end of the experiment, closing the window will terminate the code, saving a .png of the graph to the same folder as the .csv files.

See Supplementary Information section S6 for full details. 