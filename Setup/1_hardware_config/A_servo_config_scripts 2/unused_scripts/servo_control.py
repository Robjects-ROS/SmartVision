#!/usr/bin/env python3
#coding=utf-8
import time
from Arm_Lib import Arm_Device

# Get DOFBOT object
Arm = Arm_Device()
time.sleep(.1)

# Separately control a servo to move to a certain angle
id = 1

Arm.Arm_serial_servo_write(id, 90, 500)
time.sleep(1)