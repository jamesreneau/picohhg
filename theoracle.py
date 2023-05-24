""" theoracle - real world problem solver

Version 00
James M. Reneau Ph.D.
http://www.picohhg.com

This work is licensed under the Creative Commons Attribution-ShareAlike 2.0 Generic License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/2.0/ or send
a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

V
00		2023-05-23	jmr		original coding
"""

VERSION = "00"

import random
import time
from machine import I2C
from machine import Pin
from rotaryIRQ import RotaryIRQ
from ssd1306 import SSD1306_I2C
from button import Button
    
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
rotary = RotaryIRQ(7, 6)
button = Button(26)

faces = [
["It is certain."],
["It is decidedly", "so."],
["Without a doubt."],
["Yes definitely."],
["You may rely", "on it."],
["As I see it,", "yes."],
["Most likely."],
["Outlook good."],
["Yes."],
["Signs point", "to yes."],
["Reply hazy,", "try again."],
["Ask again later."],
["Better not tell", "you now."],
["Cannot", "predict now."],
["Concentrate", "and ask again."],
["Don't count on", "it."],
["My reply is no."],
["My sources say", "no."],
["Outlook not so", "good."],
["Very doubtful."],
["42"]]

oled.fill(0)
oled.text("The Oracle",0,0)
oled.text("Spin to commune",0,15)
oled.text("with the Oracle.",0,25)
oled.text("Press rotary to",0,40)
oled.text("find the answer.",0,50)
oled.show()

f = 0

# wait for initial spin
rval = rotary.value()
while True:
    if rotary.value() != rval:
        break
    time.sleep(.1)
    
rval = rotary.value()
newrval = rval

mainloop = True

while mainloop:
    f = f + 11
    f = f % len(faces)
    
    oled.fill(0)
    oled.text("The Oracle",0,0)
    for i in range(len(faces[f])):
        oled.text(faces[f][i],0,15 + 10 * i)
    oled.text("Press to receive",0,54)
    oled.show()
    
    while True:
        newrval = rotary.value()
        if button.pressed():
            mainloop = False
            break
        elif newrval != rval:
            rval = newrval
            break
        elif random.random() < .2:
            break
        time.sleep(.2 * random.random())

button.waitRelease()

f = f + int(random.random()*10)
f = f % len(faces)

oled.fill(0)
oled.text("The Oracle Spoke",0,0)
for i in range(len(faces[f])):
    oled.text(faces[f][i],0,22 + 10 * i)
oled.text("Press to exit.",0,54)
oled.show()

button.wait()