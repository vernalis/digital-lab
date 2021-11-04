# Raspberry Pi Based Logging Thermocouple

[![DOI:10.33774/chemrxiv-2021-cxs25](https://img.shields.io/badge/DOI-10.33774%2Fchemrxiv--2021--cxs25-blue)][paper]
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](../LICENSE)

## Publication

Detailed information about the design and testing of these files is available in the accompanying paper:

[Paper][paper] | [Supplementary Information][si]

If you have used this project as a resource in your research, please cite:

> David Lee Walmsley, Stephen Hilton, Emilie Sellier, Matthew Penny, Daniel Maddox (2021) “Control and Monitoring of Temperature in 3D-Printed Circular Disk Reactors for Continuous Flow Photochemistry using Raspberry Pi Based Software” ChemRxiv. DOI: [10.33774/chemrxiv-2021-cxs25][paper]

[paper]: https://doi.org/10.33774/chemrxiv-2021-cxs25
[si]: https://chemrxiv.org/engage/api-gateway/chemrxiv/assets/orp/resource/item/617fc58581c4fc77f2e8b692/original/control-and-monitoring-of-temperature-in-3d-printed-circular-disk-reactors-for-continuous-flow-photochemistry-using-raspberry-pi-based-software.pdf

## Assembly Instructions

### Bill Of Materials

| Description | Product Number | Source | Price (£) |
| ------ | ------ | ------ | ------ |
| Raspberry Pi 4 Model B 2Gb | SC0193 | thepihut.com | 33.90 |
| Official UK Raspberry Pi 4 Power Supply (5.1V 3A) | SC0212 | thepihut.com | 7.50 |
| Raspbian Preinstalled 16GB Micro SD Card [Discontinued] | SC0267 | thepihut.com | 8.00 |
| Thermocouple Amplifier MAX31855 breakout board | ADA269 | thepihut.com | 13.00 |
| Thermocouple Type-K Glass Braid Insulated Stainless Steel Tip | ADA3245 | thepihut.com | 8.70 |
| RGB LCD Shield Kit w/ 16x2 Character Display | ADA716 | thepihut.com | 20.80 |
| 3D Printing Filament Made in Germany 1.75 mm 2.85 mm PLA PETG HIPS 15 Colours 1 kg Spool or Refill | 8719689844059 | amazon.co.uk | (24.88/ kg, 71 g used) 1.77 |
| **Total** |  |  | **(116.78) 93.67** |

A modified version of [a publicly available Raspberry Pi 4 case](https://www.thingiverse.com/thing:3723561) was designed to accommodate RGB LCD shield (ADA716) – allowing headless operation of the device and containment of all components. STL files and further instructions for this modified case are available in the [Vernalis 3D-printing Files Repository][case]. This was printed in PETG filament to provide good temperature resilience during operation even during high CPU usage.

[case]: https://github.com/vernalis/3Dprint_files

### Assembly

Raspberry Pi 4 containing 16Gb SD card (with operating system pre-installed) was fitted into the base of the case.

Thermocouple amplifier (ADA269) interfaces using SPI and was connected to 3V (Vin), Ground (Gnd), GPIO 9 (Do/MISO), GPIO 11 (Clk) and GPIO 5 (CS). Type-K class thermocouple (ADA3245) was connected to positive and negative terminals, noting correct polarity [ref][ADA269]. Thermocouple threaded through side port included in upper portion of case.

RGB LCD Shield (ADA716) was constructed according to supplier instructions [[ref][ADA716]]. The screen and buttons primarily interface using I2C, with the reset button operating as an independent switch monitored on a separate GPIO pin. Shield was connected to 5V, Ground, GPIO 2 (Data/SDA), GPIO 3 (Clock/SCL) and GPIO 17 (Reset, configured pin to be ‘pull up’). Screen was then mounted into upper portion of case using 4 screws (M2.5 nuts printed into the casing). Case could then be snapped together closed.

Fritzing and circuit diagrams follow below:

![Fritzing_Diagram][fritzing]

![Circuit_Diagram][circuit]

[circuit]: Circuit.png
[fritzing]: Fritzing.png
[ADA269]: https://learn.adafruit.com/thermocouple/overview
[ADA716]: https://learn.adafruit.com/rgb-lcd-shield/overview
## Code & Usage

Datalogging code written and tested in Python 3.7.3 using Thonny IDE. Thermocouple interface code based on that supplied by manufacturer [[ref][ADA269]]. Screen I2C interface code based on that supplied by manufacturer [[ref][ADA716]].

By default the script will output a CSV to the user folder, however can also be configured to output to a defined location by either of two methods. First, by providing the path as a command line argument:

```
python logging_thermocouple.py /path/to/output/folder/
```

Or secondly by setting an environment variable:

```
export VER_THERM_LOG=/path/to/output/folder
python logging_thermocouple.py
```

Once started, the code will log a temperature every 15 seconds to a csv file in a pre-defined file location and update the LCD screen accordingly.
To prevent log file corruption, press and hold the reset button to ‘break’ and stop the code loop.
