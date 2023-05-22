import random
import math
import time
import sys
from choosers import ChooserUIButton


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
        super().__init__( oled, x, y, "", 20, 24, self.drawCardFace)
        
    def drawSuiteClub(self, x, y, fg):
        self.oled.vline(x + 0, y  + 4, 2, fg)
        self.oled.vline(x + 1, y  + 3, 4, fg)
        self.oled.vline(x + 2, y  + 3, 4, fg)
        self.oled.vline(x + 3, y  + 1, 2, fg)
        self.oled.vline(x + 3, y  + 4, 2, fg)
        self.oled.vline(x + 4, y  + 0, 4, fg)
        self.oled.vline(x + 4, y  + 6, 4, fg)
        self.oled.vline(x + 5, y  + 0, 4, fg)
        self.oled.vline(x + 5, y  + 8, 2, fg)
        self.oled.vline(x + 6, y  + 1, 2, fg)
        self.oled.vline(x + 6, y  + 4, 2, fg)
        self.oled.vline(x + 7, y  + 3, 4, fg)
        self.oled.vline(x + 8, y  + 3, 4, fg)
        self.oled.vline(x + 9, y  + 4, 2, fg)
        
    def drawSuiteSpade(self, x, y, fg):
        self.oled.vline(x+0, y+4, 1, fg)
        self.oled.vline(x+1, y+3, 4, fg)
        self.oled.vline(x+2, y+2, 5, fg)
        self.oled.vline(x+3, y+1, 5, fg)
        self.oled.vline(x+4, y+0, 10, fg)
        self.oled.vline(x+5, y+0, 10, fg)
        self.oled.vline(x+6, y+1, 5, fg)
        self.oled.vline(x+7, y+2, 5, fg)
        self.oled.vline(x+8, y+3, 4, fg)
        self.oled.vline(x+9, y+4, 1, fg)

    def drawSuiteHeart(self, x, y, fg):
        self.oled.vline(x+0, y+2, 2, fg)
        self.oled.vline(x+1, y+1, 4, fg)
        self.oled.vline(x+2, y+0, 7, fg)
        self.oled.vline(x+3, y+1, 7, fg)
        self.oled.vline(x+4, y+2, 8, fg)
        self.oled.vline(x+5, y+2, 8, fg)
        self.oled.vline(x+6, y+1, 7, fg)
        self.oled.vline(x+7, y+0, 7, fg)
        self.oled.vline(x+8, y+1, 4, fg)            
        self.oled.vline(x+9, y+2, 2, fg)
        
    def drawSuiteDiamond(self, x, y, fg):
        self.oled.vline(x+0, y+4, 2, fg)
        self.oled.vline(x+1, y+3, 4, fg)
        self.oled.vline(x+2, y+2, 6, fg)
        self.oled.vline(x+3, y+1, 8, fg)
        self.oled.vline(x+4, y+0, 10, fg)
        self.oled.vline(x+5, y+0, 10, fg)
        self.oled.vline(x+6, y+1, 8, fg)
        self.oled.vline(x+7, y+2, 6, fg)
        self.oled.vline(x+8, y+3, 4, fg)
        self.oled.vline(x+9, y+4, 2, fg)

    def drawCardFace(self, oled, x, y):
        fg = self.fgColor()
        #
        if self.card and not self.back:
            ## draw face
            (s, c) = self.card.short()
            if s == "S":
                self.drawSuiteSpade(x, y, fg)
            elif s == "H":
                self.drawSuiteHeart(x, y, fg)
            elif s == "C":
                self.drawSuiteClub(x, y, fg)
            elif s == "D":
                self.drawSuiteDiamond(x, y,fg)
            else:
                self.oled.text(s, x, y, fg)
            self.oled.text(c, x, y + 12, fg)
        else:
            ## leave back blank for now
            pass
        