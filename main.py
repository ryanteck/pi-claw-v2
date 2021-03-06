from time import sleep
from gpiozero import Motor, Button, PWMLED, LED
import pygame
import random

#Setup audio
pygame.mixer.pre_init(44100, -8, 2, 512)
pygame.mixer.init()
moveMusic = ["music/movement-1.ogg","music/movement-2.ogg","music/movement-3.ogg"]
clawMusic = "music/clawLonger-m.ogg"

#Define motors
fbM = Motor(17,27)
lrM = Motor(23,22)
udM = Motor(24,25)
#Define stops
lrStop = Button(20)
fbStop = Button(19)
uStop = Button(26)
dStop = Button(21)
#Define FP Buttons
fBut = Button(13)
rBut = Button(12)
#Define FP Button Lights
fBl = LED(6)
rBl = LED(5)
#Define Coin Mech
#coinI = Button()
#Define Magnet
clawMagnet = PWMLED(18,frequency=200)

#Rigging Calculations

#averageCostPerPrize = 1 #In GBP
#costPerGo = 0.2 #In GBP
#currentWins = 0 #Start at 0 and add
#currentPlays = 0 # Start at 0 and add one per each play
#profitRequired = 1 #Percentage/100 required, usually 2 (double) is fine
#winRatio = (averageCostPerPrize*profitRequired)/costPerGo
#
#def calculateStrength():
#    global currentPlays
#    winPercentage = (currentPlays*winRatio)/100
#    print(winPercentage)
#    percentage = random.uniform(0.4,winPercentage)
#    print(percentage)
#    currentPlays +=1
#return 0.8
def calculateStrength():
    return random.uniform(0.4,0.8)

def returnToHome():
    lrStop.when_pressed = lrM.stop
    fbStop.when_pressed = fbM.stop
    lrM.backward()
    fbM.backward()
    sleep(0.3)
    while(lrStop.value==False or fbStop.value==False):
        pass
    lrM.stop() #Sometimes even though this should have been run it doesn't.
    fbM.stop()
    lrStop.when_pressed = None
    fbStop.when_pressed = None
    clawMagnet.off()

def grabProcedure(strength):
    pygame.mixer.music.load(clawMusic)
    pygame.mixer.music.play(-1)
    #Procedure for grabbing the item.
    udM.backward()
    cT = 0
    while(cT<16 and dStop.value==False):
        print(cT)
        sleep(1)
        cT = cT+1
    udM.stop()
    #grab
    #pygame.mixer.music.rewind()
    clawMagnet.value = strength
    udM.forward()
    sleep(5)
    clawMagnet.value = random.uniform(strength-0.05,strength)
    uStop.wait_for_press()
    udM.stop()

def initProcedure():
    #First move the motor one second forward and right & Drop claw 2 secs
    fbM.forward()
    lrM.forward()
    udM.backward()
    sleep(1)
    fbM.stop()

    sleep(1)
    lrM.stop()
    udM.stop()
    #Blink claw
    i = 0
    while(i<2):
        clawMagnet.toggle()
        sleep(0.3)
        i = i +1
    clawMagnet.off()
    #Home Claw
    udM.forward()
    uStop.wait_for_press()
    udM.stop()
    #Home LR
    returnToHome()


initProcedure()
musicNo = 0
while True:
    pygame.mixer.music.load(moveMusic[musicNo])
    fBl.on()
    rBl.on()
    fBut.wait_for_press()
    pygame.mixer.music.play()
    fbM.forward()
    sleep(0.2)
    while(fBut.is_pressed) and (fbStop.is_pressed==False):
        sleep(0.01)
    fbM.stop()
    fBl.off()
    rBut.wait_for_press()
    lrM.forward()
    sleep(0.2)
    while(rBut.is_pressed) and (lrStop.is_pressed==False):
        sleep(0.01)
    lrM.stop()
    rBl.off()
    strength = calculateStrength()
    grabProcedure(strength)
    pygame.mixer.music.load(moveMusic[musicNo])
    pygame.mixer.music.play()
    returnToHome()
    pygame.mixer.music.stop()
    musicNo+=1
    if(musicNo>2):
        musicNo=0
