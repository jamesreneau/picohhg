""" PlayingCards - Card, deck and button objects for playing cards

Version 01
James M. Reneau Ph.D.
http://www.picohhg.com

This work is licensed under the Creative Commons Attribution-ShareAlike 2.0 Generic License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/2.0/ or send
a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

V
00		2023-05-08	jmr		original coding
01		2023-05-22	jmr		Split out symbols

"""

import random
import math
import time
import sys
from choosers import ChooserUIButton
from symbols import Symbols


class PlayingCard():
    SUITE = ["Spades", "Hearts", "Clubs", "Diamonds", ""]
    SUITE_SHORT = ["S", "H", "C", "D", ""]
    CARD = ["Ace","2","3","4","5","6","7","8","9","10","Jack","Queen","King"]
    CARD_SHORT = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
    OTHERCARD = ["Joker"]
    OTHERCARD_SHORT = ["X"]
    
    def __init__(self, suite, card):
        self.suite = suite
        self.card = card
        self.hasFocus = False
        
    def __str__(self):
        c = self.strCard()
        if self.suite < 4:
            return  c + " " + self.strSuite()
        else:
            return c
    
    def strSuite(self):
        return PlayingCard.SUITE[self.suite]
    
    def strCard(self):
        if self.suite < 4:
            return  PlayingCard.CARD[self.card]
        else:
            return PlayingCard.OTHERCARD[self.card]
    
    def short(self):
        if self.suite < 4:
            return (PlayingCard.SUITE_SHORT[self.suite], PlayingCard.CARD_SHORT[self.card])
        else:
            return (PlayingCard.SUITE_SHORT[self.suite], PlayingCard.OTHERCARD_SHORT[self.card])
        
    def isSameCard(self, pc):
        return self.card == pc.card
    
    def isSameSuite(self, pc):
        return self.suite == pc.suite


class PlayingCardDeck():
    def __init__(self, includeJokers=False):
        self.cards = []
        for s in range(4):
            for c in range(13):
                self.cards.append(PlayingCard(s,c))
        if includeJokers:
            self.cards.append(PlayingCard(4,0))
            self.cards.append(PlayingCard(4,0))

    def shuffle(self):
        # random on micropython does not implement shuffle
        for r in range(2):
            for i in range(len(self.cards)):
                j = int(random.random() * len(self.cards))
                t = self.cards[j]
                self.cards[j] = self.cards[i]
                self.cards[i] = t
    
    def __getitem__(self, index):
        return self.cards[index]
    
    def __len__(self):
        return len(self.cards)
    
    def deal(self, location=0):
        # deal one card and remove from deck
        if len(self.cards)==0:
            return False
        else:
            return self.cards.pop(location)
        
    def __str__(self):
        s = ""
        for c in self.cards:
            s = s + str(c) + " "
        return s
    
class PlayingCardButton(ChooserUIButton):
    def __init__(self, oled, x, y, card, back=False):
        self.card = card
        self.back = back ## show back
        self.symbols = Symbols(oled)
        super().__init__( oled, x, y, "", 20, 24, self.drawCardFace)
        

    def drawCardFace(self, oled, x, y):
        fg = self.fgColor()
        #
        if self.card and not self.back:
            ## draw face
            (s, c) = self.card.short()
            if s == "S":
                self.symbols.draw(x, y, Symbols.SPADE, fg)
            elif s == "H":
                self.symbols.draw(x, y, Symbols.HEART, fg)
            elif s == "C":
                self.symbols.draw(x, y, Symbols.CLUB, fg)
            elif s == "D":
                self.symbols.draw(x, y, Symbols.DIAMOND, fg)
            else:
                self.oled.text(s, x, y, fg)
            self.oled.text(c, x, y + 12, fg)
        else:
            ## leave back blank for now
            pass
        