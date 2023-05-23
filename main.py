""" Menu (use as main.py)

Version 03
James M. Reneau Ph.D.
http://www.picohhg.com

This work is licensed under the Creative Commons Attribution-ShareAlike 2.0 Generic License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/2.0/ or send
a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

V
00		2023-05-08	jmr		original coding
01      2023-05-09  jmr     updated sst to sst02, added quit
02		2023-05-19	jmr		added jacks or better
03		2023-05-20	jmr		added one hand solitare

"""
import sys
import time
import math
import os

from choosers import ChooseList
from choosers import TextScroll

if sys.implementation.name == 'micropython':
    from machine import Pin
    from machine import I2C
    from rotaryIRQ import RotaryIRQ
    from ssd1306 import SSD1306_I2C
    from button import Button
    
    i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
    oled = SSD1306_I2C(128, 64, i2c)
    rotary = RotaryIRQ(7, 6)
    button = Button(26)
else:
    oled = False
    rotary = False
    rotarybutton = False

def find(l, s):
    try:
        return l.index(s)
    except:
        return -1

    
VERSION = "03"
menufiles = ["pong04.py", "sst.py", "jacksorbetter.py", "onehandedsolitare.py", "clockywocky.py", "", ""]
menunames = ["PicoPong", "Super Trekie", "Jacks or Better", "OneHand Solitare", "Clocky Woky", "About", "Quit"]

while True:
    files = os.listdir()
    installed = []
    for f in files:
        i = find(menufiles, f)
        if i >=0:
            installed.append(menunames[i])
    installed.append(menunames[-2])
    installed.append(menunames[-1])

    oled.fill(0)
    oled.text("PicoHHG Menu " + VERSION, 0, 0)
    s = ChooseList(oled, rotary, button, installed, 0, 20, "choose...").get()
    if s == menunames[-1]:
        break
    elif s == menunames[-2]:
        TextScroll(oled, rotary, button, [
            "PicoHHG Menu",
            "Version "+VERSION,
            "Program Menu by J.M.Reneau."
            ]).display()
    else:
        i = find(menunames, s)
        if i >= 0:
            exec(open(menufiles[i]).read())

oled.fill(0)
oled.text("PicoHHT Menu " + version, 0, 0)
oled.text("Exited.", 0, 10)
oled.show()
