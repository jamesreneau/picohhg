""" Clockywoky - Tribute to tommy

Version 00
James M. Reneau Ph.D.
http://www.picohhg.com

This work is licensed under the Creative Commons Attribution-ShareAlike 2.0 Generic License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/2.0/ or send
a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

V
00		2023-04-30	jmr		original coding
"""

## set displaydevice = ["OLED","LCD"]
displaydevice = "OLED"
showTH = False

if displaydevice=="OLED":
    from machine import SoftI2C
    from machine import Pin
    from ssd1306 import SSD1306_I2C

if displaydevice == "LCD":
    from Pico_LCD_114_V2 import LCD_1inch14
    from machine import Pin,SPI,PWM

if showTH:
    from sht31 import SHT31

import time
import math

def j2(n):
    return ("00" + str(n))[-2:]


if displaydevice == "OLED":
    i2c_oled = SoftI2C(scl=Pin(17), sda=Pin(16))
    display = SSD1306_I2C(128, 64, i2c_oled)
    black = 0
    white = 1
    
if displaydevice == "LCD":
    display = LCD_1inch14()
    black = 0x0000
    white = 0xffff
    
xc = display.height//2
yc = display.height//2
    
if showTH:
    i2c_thsens = SoftI2C(scl=Pin(15), sda=Pin(14))
    thsens = SHT31(i2c_thsens)

def hand(t, u, l):
    pct = t/u-.25
    x = math.cos(pct*math.pi*2)*xc*l+xc
    y = math.sin(pct*math.pi*2)*yc*l+yc
    display.line(xc,yc,int(x),int(y),white)

def face():
    for t in range(12):
        pct = t/12-.25
        x = math.cos(pct*math.pi*2)*xc+xc
        y = math.sin(pct*math.pi*2)*yc+yc
        x2 = math.cos(pct*math.pi*2)*xc+xc
        y2 = math.sin(pct*math.pi*2)*yc+yc
        display.line(int(x2),int(y2),int(x),int(y),white)

while True:
    time.sleep(.5)
    
    lt = time.localtime()
    display.fill(black)
    face()
    hand(lt[3], 12, .6)
    hand(lt[4], 60, .75)
    hand(lt[5], 60, 1)
    
    display.text(j2(lt[3])+':'+j2(lt[4])+':'+j2(lt[5]), display.width-8*8, 0, white)
   
    if showTH:
        th = thsens.get_temp_humi()
        s = str(int(th[0])) + "c"
        display.text(s, 128-len(s)*8, 10, white)
        s = str(int(th[0]*9/5+32)) + "f"
        display.text(s, 128-len(s)*8, 20, white)
        s = str(int(th[1])) + "%rh"
        display.text(s, 128-len(s)*8, 30, white)

    display.show()
