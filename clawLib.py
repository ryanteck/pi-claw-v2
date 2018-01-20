from time import sleep
from gpiozero import Motor, Button, PWMLED

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
fBut = Button(12)
rBut = Button(13)
#Define Coin Mech
#coinI = Button()
#Define Magnet
clawMagnet = PWMLED(18,frequency=100)
def returnToHome():
        lrStop.when_pressed = lrM.stop
        fbStop.when_pressed = fbM.stop
        lrM.backward()
        fbM.backward()
        while(lrStop.value==False or fbStop.value==False):
            pass
        lrStop.when_pressed = None
        fbStop.when_pressed = None

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
    while(i<10):
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

    print("True") #Both switches are hit by now and the when_pressed function should have ran but doesn't seem to trigger for 5 seconds.



initProcedure()
