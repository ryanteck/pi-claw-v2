from time import sleep
from gpiozero import Motor, Button, PWMLED

clawMagnet = PWMLED(18,frequency=10000)

while True:
    input()
    clawMagnet.value = 0.9
    input()
    clawMagnet.value = 0
