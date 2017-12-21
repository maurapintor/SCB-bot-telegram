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
sensitivities. Depending on the logic input placed on pin GSEL,
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

For GPS setup and testing we used [this tutorial](http://www.ayomaonline.com/iot/gy-gps6mv2-neo6mv2-neo-6m-gps-module-with-arduino-usb-ttl/). This just reads the GPS output data. Those data are very hard to read, so we used the parsing library [Tiny GPS](https://github.com/mikalhart/TinyGPS). From this library we took the example sketch "test_with_gps_device" and modified the behavior in order to obtain the time-stamp and the coordinates. Finally, we are ready to send the coordinates to the Google Cloud Datastore.

### Setup WiFi connectivity (hotspot)



### Sending coordinates to cloud

USIAMO SERVIZI CLOUD

#### Google cloud platform
Now we have to create a project in the [Google Cloud Platform](https://cloud.google.com). You can create a Google account or use your own. First step is to create a project, following this [link](https://console.cloud.google.com). 

Inline-style: 
![alt text](https://drive.google.com/open?id=1XpMfyL-WS0ciBbPdfrY-XnO1eNiyMnmC "Logo Title Text 1")
IMAGE





### Telegram bot setup

### Adding Telegram bot functionalities in the Arduino Sketch
