
#Description: The code used for the high five robot. It uses a background thread to detect and use the input of the motion sensor and a foreground loop
#which checks if the high five was made and act accordingly

#!/usr/bin/python3

#libraries used
#raspberry PI was updated to latest version for program to function correctly
import RPi.GPIO as GPIO
import time
import pygame
import queue
import threading

pygame.init()

#the tts audio files used
highfive = pygame.mixer.Sound("/home/pi/Documents/highfive.ogg")
cheer = pygame.mixer.Sound("/home/pi/Documents/cheer.ogg")

#global value to check if the high five was made to stop/start if statements
global highFiveMade
highFiveMade = False

#Setting up the GPIO pins to be used
#the number used as the pin = pin postion on the Raspberry Pi not GPIO + number
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(11,GPIO.IN)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.setup(29,GPIO.IN)

#Setting the motor pulse width, start position
p = GPIO.PWM(13,50)
p.start(5)

#power LED always on
GPIO.output(7,1)

#the distance sensor loop
#will consider a high five made if distance < 6 cm
def sensor():
        global highFiveMade
        #sensor needs time to warm up before calculating
        GPIO.output(15,GPIO.LOW)
        time.sleep(1) # this time.sleep() affects the speed of the calculations
        #triggers/ starts the distance sensor calculation
        GPIO.output(15,GPIO.HIGH)
        time.sleep(0.001)
        GPIO.output(15,GPIO.LOW)
        
        #the distance calculation loop
        while GPIO.input(29)== 0:
            startTime = time.time()
        while GPIO.input(29)==1:
            endTime = time.time()
        duration = endTime - startTime
        distance = round(duration * 17150, 2)

        #the high five was made
        if distance <= 5 and highFiveMade == False:
            cheer.play()
            
            highFiveMade = True

 
#the motion sensor background thread
#constantly checks for the presenece and adjusts led and motor accordingly
#detected i = 1 nothing i = 0
def PIR(q):
    detected = False
    global highFiveMade
    while True:
        i = GPIO.input(11)
        #the high five was made
        if highFiveMade == True:
            
            p.ChangeDutyCycle(5)
            GPIO.output(3,0)
            time.sleep(0.1)
            highFiveMade = False
        #not detected code/ idle state
        elif i == 0 and detected == False and highFiveMade == False:
            p.ChangeDutyCycle(5)
            detected = True
            GPIO.output(3,0)
            time.sleep(0.1)
        #detected code    
        elif i == 1 and detected == True and highFiveMade == False:
            detected = False
            highfive.play()
            p.ChangeDutyCycle(10)
            GPIO.output(3,1)
            time.sleep(0.1)
        
        q.put(i)    
        p.ChangeDutyCycle(0)
        

#the code used the create the PIR() background thread
q = queue.Queue()
d = threading.Thread(target=PIR,args=[q])
d.daemon = True
d.start()
time.sleep(0.01)

while True:
    
    sensor()
