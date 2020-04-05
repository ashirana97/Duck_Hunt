# File Name:  Duck_Hunt.py 
# File Path:  /home/ranaashish/Python/FinalProject/Duck_Hunt.py

# Ashish Rana
# Date (12/12/19)
# Duck_Hunt.py
# Implementation of a similar version of a game Duck Hunt.This is a python based program that
# uses many libraries such as graphic, adafruit, time and GPIO.This program is integrated with
# a joystick and a button for the user to shoot duck objects displayed on the screen.

import busio
import digitalio
import board
import time
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
from graphics import *
import math
import random
import RPi.GPIO as GPIO
import os
import sys

#Length and Width of the game display
WIN_WIDTH = 800
WIN_HEIGHT = 800

#Radius for the crosshair
RADIUS = 5

#Creating a graphics window
win = GraphWin("Game Window",WIN_WIDTH,WIN_HEIGHT)
win.setBackground("light blue")

global STATE
global DRAW1
global DRAW2

DRAW1 = True
DRAW2 = True

STATE = False

#This function records the input of the shooting button
def button(channel):
    global STATE
    print("Button One Falling Edge")
    STATE = True

#Intializing GPIO pins
GPIO.setwarnings(False) # Ignore warnings
GPIO.setmode(GPIO.BCM) # Use BCM Pin numbering
GPIO.setup(21, GPIO.IN)

print("Inital State is ",STATE)
GPIO.add_event_detect(21,GPIO.FALLING,callback=button, bouncetime=300)

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)

# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 1
chan0 = AnalogIn(mcp, MCP.P1)

# create an analog input channel on pin 2
chan1 = AnalogIn(mcp, MCP.P2)


#flap down for duck1 and duck2 going forward 
Duckdownf1 = Image(Point(100,500), "finaldownf.png")
Duckdownf2 = Image(Point(100,300),"finaldownf.png")

#flap up for duck1 and 2 going forward
Duckupf1 = Image(Point(100,500),"finalupf.png")
Duckupf2 = Image(Point(100,300),"finalupf.png")

#flap down for duck1 and duck2 going backwards
Duckdownb1 = Image(Point(700,500), "finaldownb")
Duckdownb2 = Image(Point(700,300),"finaldownb")

#flap up for duck1 and duck2 going backwards
Duckupb1 = Image(Point(700,500),"finalupb")
Duckupb2 = Image(Point(700,300),"finalupb")

#image of grass
Grass = Image(Point(0,700),"grass.png")
Grass1 = Image(Point(300,700),"grass.png")

#draw grass on the window
Grass.draw(win)
Grass1.draw(win)

# creating crosshair
circle01 = Circle(Point(100,100),RADIUS)
circle01.setFill("red")
circle01.draw(win)

count = 0
count1 = 0
xdir = 1
ydir  = 1

target = 0
while(1):
    
    #Getting the width of the ducks image going forward
    duckwidth1 = Duckupf1.getWidth()
    duckwidth2 = Duckupf2.getWidth()
    
    #Getting the width of the ducks image going backward
    duckwidth3 = Duckupb1.getWidth()
    duckwidth4 = Duckupb2.getWidth()

    #Getting the height of the ducks image
    duckheight1 = Duckupf1.getHeight()
    duckheight2 = Duckupf2.getHeight()
    
    #Storing the position of the Ducks forwards and backwards
    duckx1 = Duckupf1.getAnchor().getX() +(duckwidth1/2)
    duckx2 = Duckupf2.getAnchor().getX() +(duckwidth2/2)
    
    duckx3 = Duckupb1.getAnchor().getX() +(duckwidth3/2)
    duckx4 = Duckupb2.getAnchor().getX() +(duckwidth4/2)

    
    ducky1 = Duckupf1.getAnchor().getY() +(duckheight1/2)
    ducky2 = Duckupf2.getAnchor().getY() +(duckheight2/2)
  
    #motion of the duck while it not at the end of the diplay yet
    if(((duckx1 or duckx2) < WIN_WIDTH)):
        xdir = 1  #Direction multiplyer
        print("drawing 1")
        
        #if/else acts like a switch, it gets executed every other time to switch between
        #images smoothly without any delay. I used move method to displace the images and
        #make it animated so it looks like flapping wings
        if(count % 2 == 0):
            if(DRAW1 == True):
                Duckupf1.undraw()
                Duckdownf1.draw(win)
                Duckdownf1.move(20*xdir,5*ydir)
            if(DRAW2 == True):
                Duckupf2.undraw()
                Duckdownf2.draw(win)
                Duckdownf2.move(20*xdir,-5*ydir)
            
            count +=1
        else:
            if(DRAW1 ==True):
                Duckdownf1.undraw()
                Duckupf1.draw(win)
                Duckupf1.move(20*xdir,5*ydir)
            if(DRAW2 == True):
                Duckdownf2.undraw()
                Duckupf2.draw(win)
                Duckupf2.move(20*xdir,-5*ydir)
                
            count +=1
    
    if(count > 10):
        count = 1

    #bounce back of the duck when it reaches the end of the display
    if((duckx1 or duckx2) > WIN_WIDTH ):
        print("drawing 2")
        Duckupf1.undraw()
        Duckupf2.undraw()
        Duckdownf1.undraw()
        Duckdownf2.undraw()
        
        xdir = -1 #direction switch
        if(count1 % 2 == 0):
            if(DRAW1 == True):
                Duckupb1.undraw()
                Duckdownb1.draw(win) 
                Duckdownb1.move(30*xdir,-5*ydir) 
            if(DRAW2 == True):
                Duckupb2.undraw()
                Duckdownb2.draw(win)
                Duckdownb2.move(20*xdir,5*ydir)
            
            count1 +=1
            
        else:
            if(DRAW1 == True):
                Duckdownb1.undraw()
                Duckupb1.undraw()
                Duckupb1.draw(win)
                Duckupb1.move(30*xdir,-5*ydir)
            
            if(DRAW2 == True): 
                Duckdownb2.undraw()
                Duckupb2.undraw()
                Duckupb2.draw(win)
                Duckupb2.move(20*xdir,5*ydir)
            
            
            count1 += 1
            
    #condition counter for switching the images for flapping the wings
    if (count1 >10):
        count1 = 1
        
    #after one round of going back and forth if the user hasn't shot the ducks it will end.
    #and asks the user if they want to play again.
    if((duckx3 and duckx4) <10):
        Duckupf1.undraw()
        Duckupf2.undraw()
        Duckdownf1.undraw()
        Duckdownf2.undraw()
        stop = Text(Point(400,400),"You missed your targets")
        stop.draw(win)
        time.sleep(4)
        win.close()
        
        
        inputs = input("Do you want to play again[Y/N]")
        
        if(inputs == "Y"):
            os.system('sudo python3 /home/ranaashish/Python/FinalProject/project')
        else:
            print("The game will be closed..")
            break 
    
    time.sleep(2/30)
    update(30)
    
    #The crosshair integrated with joystick    
    xjoy = int((chan0.voltage/3.3)*800) 
    yjoy = int((1 - (chan1.voltage/3.3))*800)

    #x and y coordinate of the crosshair
    moveX = xjoy - circle01.getCenter().getX()
    moveY = yjoy - circle01.getCenter().getY()
    
    
    circle01.move(moveX,moveY)
    
    #center of images stored in a variable to check the over lap with crosshair
    
    destinationx1 =  circle01.getCenter().getX()- Duckdownf1.getAnchor().getX()
    
    destinationy1 =  circle01.getCenter().getY()- Duckdownf1.getAnchor().getY() 
    
    destinationx2 = circle01.getCenter().getX() - Duckdownf2.getAnchor().getX()
    
    destinationy2 = circle01.getCenter().getY() - Duckdownf2.getAnchor().getY()
    
    destinationx3 = circle01.getCenter().getX() - Duckdownb1.getAnchor().getX()
    
    destinationy3 = circle01.getCenter().getY() - Duckdownb1.getAnchor().getY()
    
    destinationx4 = circle01.getCenter().getX() - Duckdownb2.getAnchor().getX()
    
    destinationy4 = circle01.getCenter().getY() - Duckdownb2.getAnchor().getY()
    
    #stores the distance between crosshair and the ducks to kill them later on
    
    distance1 = math.sqrt((destinationx1)**2 + (destinationy1)**2)
    
    distance2 = math.sqrt((destinationx2)**2 + (destinationy2)**2)    
    
    distance3 = math.sqrt((destinationx3)**2 + (destinationy3)**2)
  
    distance4 = math.sqrt((destinationx4)**2 + (destinationy4)**2)


    #f1 is the lower bird. f2 is the higher bird
    #if any of the if statements is true the duck will be killed and removed from the display.
    if(STATE == True and (distance1 < 20)):
        STATE = False
        DRAW1 = False
        print("1shot")
        Duckdownf1.undraw()
        Duckupf1.undraw()
        target += 1
        
    if(STATE == True and (distance2 < 20)):
        STATE = False
        DRAW2 = False
        print("2 shot")
        Duckdownf2.undraw()
        Duckupf2.undraw()
        target +=1
    
    if(STATE == True and distance3 < 20):
        STATE = False
        DRAW1 = False
        Duckdownb1.undraw()
        Duckupb1.undraw()
        target += 1
    
    if(STATE == True and distance4 < 20):
        STATE = False
        DRAW2 = False
        Duckdownb2.undraw()
        Duckupb2.undraw()
        target += 1    
    #if both of the duck are killed it prints out a message
    #and score and asks the user to play again
    if((DRAW1 or DRAW2) == False):
        start = Text(Point(400,100),"Scores: " + str(target))
        end = Text(Point(400,200),"Congratulations! You won!")
        start.setSize(20)
        end.setSize(30)
        end.draw(win)
        start.draw(win)
        time.sleep(4)
        win.close()
        
        inputs = input("Do you want to play again[y/n]")
        if(inputs == "Y"):
            os.system('sudo python3 /home/ranaashish/Python/FinalProject/project')
        else:
            print("The game will be closed..")
            break      
    
            
            
