# High-five-robot
A raspberry Pi 4 python powered robot arm which checks for a user presence to give a high five to and raises and lowers its arm accordingly. 

My capstone project from Seneca College which makes use of a Raspberry Pi 4, distasnce sensor, motion sensor, LEDs, 180 servo motor, and an external USB speaker.

Libraries used: RPi.GPIO, time, pygame, queue, threading

# Basic program loop

0. Arm is lowered and LED is off
1. Constantly checks for a presence using the motion sensor located at the front of the robot
2. If a presence is detected the arm is raised, LED is turned on, the distance sensor starts calculating distance for the high five detection, and it plays the audio file promtping the user for a high five
3. If the high five was made (distance sensor calculated distance low enough) the arm is lowered, the LED is turned off, plays the cheer audio file and waits for the presenece to leave
4. If the high five was never made it lowers the arm and turns off LED waiting for another presenece
5. Repeat


![image](https://user-images.githubusercontent.com/74801180/176693710-c0e3d57a-d9ac-4793-aae4-57445a398a99.png)
