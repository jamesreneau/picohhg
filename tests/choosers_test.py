import sys

import time
import math

from choosers import ChooseList
from choosers import ChooseRoundNumber
from choosers import ChooseFaceNumber
from choosers import TextScroll
from choosers import ChooseString

    
if sys.implementation.name == 'micropython':
    from machine import Pin
    from machine import I2C
    from rotaryIRQ import RotaryIRQ
    from ssd1306 import SSD1306_I2C
    from button import Button
    
    i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
    oled = SSD1306_I2C(128, 64, i2c)
    rotary = RotaryIRQ(7, 6)
    rotarybutton = Button(26)
else:
    oled = False
    rotary = False
    rotarybutton = False

if True:
    s = ChooseString(oled, rotary, rotarybutton, 8, 0, 10, "#", False).get()
    print(s)
    
if True:
    text = ["a - the first letter of the alphabet if you are an american.","uy yfhfjhgf jhgf hjgfjhgf jhgf jhgf jhgf uytf yutfjhgfjhgfjh.","z - The last letter in the same alphabet and one of the least used."]
    n = TextScroll(oled, rotary, rotarybutton, text).display()

if True:
    n =  ChooseRoundNumber(oled, rotary, rotarybutton, "Heading", 0, 360, 5)
    print(n.get())
    
if True:
    n =  ChooseFaceNumber(oled, rotary, rotarybutton, "Power", 0, 100, 5)
    print(n.get())
