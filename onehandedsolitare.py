""" OneHandedSolitare - Soltare you play in one hand

Version 00
James M. Reneau Ph.D.
http://www.picohhg.com

This work is licensed under the Creative Commons Attribution-ShareAlike 2.0 Generic License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/2.0/ or send
a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

V
00		2023-05-20	jmr		original coding
"""

VERSION = "00"

import random
import math
import time
import sys
from machine import I2C
from machine import Pin
from rotaryIRQ import RotaryIRQ
from ssd1306 import SSD1306_I2C
from button import Button
from choosers import *
from playingcards import *

    
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
rotary = RotaryIRQ(7, 6)
button = Button(26)
        
uiWidgets = [PlayingCardButton(oled, 92, 10, None),
      PlayingCardButton(oled, 68, 10, None),
      PlayingCardButton(oled, 44, 10, None),
      PlayingCardButton(oled, 20, 10, None),
      ]

hand = [] 

TextScroll(oled, rotary, button, [
    "One Handed Solitare.",
    "Version "+VERSION,
    "Foo"
    ]).display()

# deal initialhand
deck = PlayingCardDeck()
deck.shuffle()
for i in range(4):
    hand.append(deck.deal())
        
   
def draw():
    oled.fill(0)
    oled.text("One Hand",0,0)
    oled.text(str(len(hand)),0,10)
    oled.text(str(len(deck)),0,20)
    for i in range(4):
        uiWidgets[i].card = hand[-1-i]
        uiWidgets[i].draw()
        
while True:
    ## show cards
    draw()
    oled.show()

    can4 = hand[-1].card == hand[-4].card
    can2 = hand[-1].suite == hand[-4].suite
    
    list = []
    list.append("next card")
    if can4:
        list.append("discard 4")
    if can2:
        list.append("discard 2")
    list.append("quit")
        
    cmd = ChooseList(oled, rotary, button,
        list
        , x=0, y=50, prompt="").get()
 
    if cmd == "next card":
            if len(deck)!=0:
                hand.append(deck.deal())
            
    if cmd == "discard 4":
        ## need test
        for i in range(4):
            hand.pop()
        
    if cmd == "discard 2":
        ## need test
        hand.pop(-2)
        hand.pop(-2)

    while len(hand) < 4 and len(deck) > 0:
        hand.append(deck.deal())
            
    if cmd == "quit" or len(hand) < 4:
        draw()
        oled.text("game over.",0,40)
        oled.text("press button",0,50)
        oled.show()
        button.wait()
        break
