# SCB-bot-telegram
Smart Car Box (SCB) repository. Made by pizza-team, a group of students from University of Cagliari.

## Introduction

### Functionalities

### Architecture

### State-diagram

## Let's start!

### Software requirements

### Hardware list

### Hardware setup

### Arduino sketch for accelerometer
First of all connect the accelemeter (MMA7361) as showed following:

immagine connectionship

For more information on MMA7361 click [here](https://www.nxp.com/docs/en/data-sheet/MMA7361L.pdf).

Summarizing the principal functionalities:

#### g-Select
The g-Select feature allows for the selection between two
sensitivities. Depending on the logic input placed on pin 10,
the device internal gain will be changed allowing it to function
with a 1.5g or 6g sensitivity.

| g-Select        | g-Range           | Sensitivity  |
| ----------------|:-----------------:| ------------:|
|       0         |       1.5g        | 800 mV/g     |
|       1         |        6g         | 206 mV/g     |

#### Sleep Mode
The 3 axis accelerometer provides a Sleep Mode that is
ideal for battery operated products. When Sleep Mode is
active, the device outputs are turned off, providing significant
reduction of operating current

### Arduino sketch for GPS

### Setup WiFi connectivity (hotspot)

### Sending coordinates to cloud

### Telegram bot setup

### Adding Telegram bot functionalities in the Arduino Sketch
