""" Pico Pong

Version 4
James M. Reneau Ph.D.
http://www.picohhg.com

This work is licensed under the Creative Commons Attribution-ShareAlike 2.0 Generic License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/2.0/ or send
a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

V
03		2023-05-08	jmr		changed button to use new button object
04      2023-05-08  jmr     removed main loop for better menuing
"""

VERSION = "04"

import math
import random
import time
from machine import I2C
from machine import Pin
from rotaryIRQ import RotaryIRQ
from ssd1306 import SSD1306_I2C
from button import Button

class Paddle():
    def __init__(self, oled, rotary):
        self.oled = oled ## OLED Object
        self.rotary = rotary ## RotaryIRQ object
        self.x = 0
        self.w = 2
        self.h = 20
        self.y = (self.oled.height - self.h) // 2
        self.ry = self.rotary.value() - self.y ## to zero rotary
        self.speed = 3
    
    def draw(self, force=False):
        v = self.rotary.value() * self.speed
        ny = v - self.ry
        if ny != self.y or force:
            if ny < 0:
                ny = 0
            if ny > self.oled.height - self.h - 1:
                ny = self.oled.height - self.h - 1
            self.oled.rect(self.x, self.y, self.w, self.h, 0)
            self.oled.rect(self.x, ny, self.w, self.h, 1)
            ###self.oled.show()
            self.y = ny
        return
    
class Ball():
    def __init__(self, oled):
        self.oled = oled
        self.x = 20
        self.y = 20
        self.oldx = 0
        self.oldy = 0
        self.dx = 3
        self.dy = 1
        self.score = 0
        
    def move(self):
        ## return False if missed paddle
        self.oldx = self.x
        self.oldy = self.y
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        if self.x >= self.oled.width or self.x <= 0:
            self.dx = self.dx * -1
        if self.y >= self.oled.height or self.y <= 0:
            self.dy = self.dy * -1
        return
    
    def missed(self, paddle):
        if self.x <= paddle.x + paddle.w:
            if self.y < paddle.y or self.y > paddle.y+paddle.h:
                return True
            # spin
            self.dx += random.random()
            self.dy += random.random()
            self.score += 1
            self.showScore()
        return False
    
    def showScore(self):
        oled.fill_rect(50, 0 , 16, 10, 0)
        self.oled.text(str(self.score),50,0)
        
    def draw(self):
        self.oled.rect(int(self.oldx), int(self.oldy), 3, 3, 0)
        self.oled.rect(int(self.x), int(self.y), 3, 3, 1)
        ### self.oled.show()

i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
rotary = RotaryIRQ(7, 6)
button = Button(26)
    

paddle = Paddle(oled, rotary)
ball = Ball(oled)

oled.fill(0)
oled.text("Raspberry Pi", 0, 0)
oled.text("PICO Pong  V" + VERSION, 0, 10)
oled.text("J.M.Reneau '23", 0, 20)
oled.text("Press button", 0, 30)
oled.show()
while not button.pressed():
    time.sleep(.05)        

oled.fill(0)
paddle.draw(True)	## initial draw
ball.showScore()
oled.show()
while True:
    paddle.draw()
    ball.move()
    if ball.missed(paddle):
        break;
    ball.draw()
    oled.show()
    #print(paddle.y)
    time.sleep(.05)

## show Game Over and count down
oled.text("Game Over", 30,30)
oled.text("Press Button", 30,40)
ball.showScore()
oled.show()

while not button.pressed():
    time.sleep(.05) 
    

