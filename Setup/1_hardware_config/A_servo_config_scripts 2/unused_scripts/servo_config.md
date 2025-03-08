# Working with a Three-Pin Servo using Raspberry Pi and Python

To work with a three-pin servo using a Raspberry Pi and Python, follow these steps:

## Hardware Setup

1. Connect the servo's ground wire (usually brown or black) to one of the Raspberry Pi's ground pins (e.g., pin 6).
2. Connect the servo's power wire (usually red) to a 5V pin on the Raspberry Pi if the servo is small and doesn't require much power. For larger servos or multiple servos, use an external power supply capable of providing the necessary current, and connect the power supply ground to the Raspberry Pi's ground.
3. Connect the servo's signal wire (usually orange or white) to a GPIO pin on the Raspberry Pi that is capable of PWM (e.g., GPIO17, pin 11).

Both configurations of the 9 g blue motor and the heavier Motor that requires external source are provided below. 

[PUT PHOTO HERE:]

## Software Setup

1. Install the RPi.GPIO Python library if it's not already installed:
    ```bash
    sudo apt-get update
    sudo apt-get install python3-rpi.gpio

