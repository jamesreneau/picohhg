""" buttonConfigure - Determine if a pull up or down is needed and save the result in a configuration file.

Version 00
James M. Reneau Ph.D.
http://www.picohhg.com

This work is licensed under the Creative Commons Attribution-ShareAlike 2.0 Generic License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/2.0/ or send
a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

V
00		2023-05-09	jmr		original coding
"""

VERSION = "00"
GPIO = 26		# defult button for the PicoHHG project

import os
from ssd1306 import SSD1306_I2C
from machine import Pin
from machine import I2C
from button import Button
import time

i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
button = Pin(GPIO, Pin.IN)	## let GPIO FLOAT

for t in range(10,-1,-1):
    oled.fill(0)
    oled.text("buttonConigure",0,0)
    oled.text("V " + VERSION + " GPIO " + str(GPIO), 0, 10)
    oled.text("Press button",0,30)
    oled.text("and hold.",0,40)
    oled.text(str(t),0,50)
    oled.show()
    time.sleep(1)
    
# get the result - if true we need a pull down if false we need a pull up
pin = Pin(GPIO, Pin.IN)
v = pin.value()

# tell user we are working evn though we are finished
oled.fill(0)
oled.text("buttonConigure",0,0)
oled.text("Reading",0,30)
oled.show()
time.sleep(1)   
    
filename = "pulldown"+str(GPIO)+".cfg"
if v:
    ## need a pull down resistor (create empty file to flag this)
    with open(filename,'w') as f:
        f.write("")
else:
    ## pull up is default - delete config file
    try:
        os.remove(filename)
    except:
        pass

# tell user we are working evn though we are finished
oled.fill(0)
oled.text("buttonConigure",0,0)
oled.text("Release button",0,30)
oled.show()
time.sleep(1)

# test configure
oled.fill(0)
oled.text("buttonConfigure",0,0)
oled.text("Press button to",0,20)
oled.text("test.",0,30)
oled.show()

button = Button(GPIO)
while True:
    if button.pressed():
        break
    time.sleep(.1)
    
    
# test configure
oled.fill(0)
oled.text("buttonConfigure",0,0)
oled.text("Test complete.",0,20)
oled.show()   