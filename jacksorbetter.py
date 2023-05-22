""" JacksOrBetter - Simple Poker Game

Version 00
James M. Reneau Ph.D.
http://www.picohhg.com

This work is licensed under the Creative Commons Attribution-ShareAlike 2.0 Generic License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/2.0/ or send
a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

V
00		2023-05-19	jmr		original coding
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

def jacksOrBetterScore(hand):
    ## return type and card
    # pair 1
    # 2pair 2
    # 3ok = 3
    # str = 4
    # flu = 6
    # fullh = 9
    # 4ok = 25
    # sflu = 50
    # rflu = 250
    hand = sorted(hand, key = lambda c: c.card)
    flush = hand[0].suite == hand[1].suite and hand[0].suite == hand[2].suite and hand[0].suite == hand[3].suite and hand[0].suite == hand[4].suite
    straight =  hand[0].card + 1 == hand[1].card and hand[1].card + 1 == hand[2].card and hand[2].card + 1 == hand[3].card and hand[3].card + 1 == hand[4].card
    royalstraight = hand[0].card == 0 and hand[1].card == 9 and hand[2].card == 10 and hand[3].card == 11 and hand[4].card == 12
    if royalstraight and flush:
        return (250, 0, "250x royal flush")
    if straight and flush:
        return (50, hand[0], "50x strght flush")
    for i in range(2):
        if hand[i].card == hand[i+1].card and hand[i].card == hand[i+2].card and hand[i].card == hand[i+3].card:
            return (25, hand[i], "25 four of kind")
    if (hand[0].card == hand[1].card and hand[1].card == hand[2].card and hand[3].card == hand[4].card) or (hand[0].card == hand[1].card and hand[2].card == hand[3].card and hand[3].card == hand[4].card):
        return (9, hand[2],"9x full house")
    if flush:
        return (6, hand[4], "6x flush")
    if straight:
        return (4, hand[4], "4x straight")
    for i in range(3):
        if hand[i].card == hand[i+1].card and hand[i].card == hand[i+2].card:
            return (3, hand[i], "3x three of kind")
    if (hand[0].card == hand[1].card and (hand[2].card == hand[3].card or hand[3].card == hand[4].card)) or (hand[1].card == hand[2].card and hand[3].card == hand[4].card):
        return (2, hand[2], "2x two pair")
    for i in range(4):
        if (hand[i].card == hand[i+1].card):
            if hand[i].card >= 10 or hand[i].card == 0:
                return (1, hand[i], "1x pair of " + hand[i].strCard() + 's')
            else:
                return (0, hand[i], "0x you loose")
    return (0, hand[4], "0x you loose")

    
i2c = I2C(0, sda=Pin(16), scl=Pin(17), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
rotary = RotaryIRQ(7, 6)
button = Button(26)
        
uiWidgets = [PlayingCardButton(oled, 0, 10, None),
      PlayingCardButton(oled, 24, 10, None),
      PlayingCardButton(oled, 48, 10, None),
      PlayingCardButton(oled, 72, 10, None),
      PlayingCardButton(oled, 96, 10, None),
      ChooserUIText(oled, 10, 50, "Deal")
      ]

balance = 10
hand = [None, None, None, None, None] 

TextScroll(oled, rotary, button, [
    "Jacks or better.",
    "Version "+VERSION,
    "This is a simple game of 5 card draw poker where you play against the house.  Bet is returned with a pair of jacks or higher. Better hands are paid, better."
    ]).display()

while True:
    ## show backs
    oled.fill(0)
    oled.text("Jacks or Better!",0,0)
    oled.text("You have $" + str(balance), 0, 40)
    oled.text("Click to bet.",0,50)
    for i in range(5):
        uiWidgets[i].card = None
        hand[i] = None
        uiWidgets[i].invese = False
        uiWidgets[i].draw()
    oled.show()
    button.wait()
    
    bet =  ChooseFaceNumber(oled, rotary, button, "Bet. Balance " + str(balance), 1, balance, 1, 10).get()

    # deal initialhand
    deck = PlayingCardDeck()
    deck.shuffle()
    for i in range(5):
        hand[i] = deck.deal()
        uiWidgets[i].card = hand[i]
    ui = ChooseUI(oled, rotary, button, uiWidgets)
    
    # allos user to mark carda and choose deal
    v = -1
    oled.fill(0)
    oled.text("Jacks or Better!",0,0)
    oled.text("Mark your hand.",0,40)
    while True:
        v = ui.get()
        if v >=0 and v < 5:
            uiWidgets[v].inverse = not uiWidgets[v].inverse
        elif v == 5:
            break
    
    # deal new cards
    for i in range(5):
        if uiWidgets[i].inverse:
            uiWidgets[i].inverse = False
        else:
            hand[i] = deck.deal()
            uiWidgets[i].card = hand[i]
            
    # show cards
    oled.fill(0)
    oled.text("Jacks or Better!",0,0)
    for i in range(5):
        uiWidgets[i].draw()
    score = jacksOrBetterScore(hand)
    balance = balance - bet
    balance = balance + score[0] * bet
    
    oled.text(score[2],0,40)
    oled.text("You have $" + str(balance), 0, 50)
    
    oled.show()
    button.wait()

    if balance <= 0:
        oled.fill(0)
        oled.text("game over.",0,20)
        oled.show()
        break
