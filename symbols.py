""" Symbols - Draw non character symbols on a feramebuf

Version 00
James M. Reneau Ph.D.
http://www.picohhg.com

This work is licensed under the Creative Commons Attribution-ShareAlike 2.0 Generic License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/2.0/ or send
a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

There is probably a much better way to do this.  Storing the pixels in byte arrays and blitting
but this works for now and gets it all in one place to be reimplemented sometime.

V
00		2023-05-22	jmr		original coding

"""

import framebuf
from micropython import const

class Symbols(framebuf.FrameBuffer):
    
    ## 8x8
    ENTER = const(0)
    SHIFTUP = const(1)
    SHIFTDOWN = const(2)
    BACKSPACE = const(3)
    
    ## 10x10 (100 pixels)
    CLUB = const(100)
    HEART = const(101)
    DIAMOND = const(102)
    SPADE = const(103)
    
    def __init__(self, display):
        self.display = display
    
    def draw(self, x, y, symbol, fg=1):
        if symbol==Symbols.CLUB:
            self.__drawClub(x, y, fg)    
        elif symbol==Symbols.HEART:
            self.__drawHeart(x, y, fg)    
        elif symbol==Symbols.SPADE:
            self.__drawSpade(x, y, fg)    
        elif symbol==Symbols.DIAMOND:
            self.__drawDiamond(x, y, fg)    
        elif symbol==Symbols.ENTER:
            self.__drawEnter(x, y, fg)    
        elif symbol==Symbols.SHIFTUP:
            self.__drawShiftUp(x, y, fg)
        elif symbol==Symbols.SHIFTDOWN:
            self.__drawShiftDown(x, y, fg)
        elif symbol==Symbols.BACKSPACE:
            self.__drawBackspace(x, y, fg)     

    def _drawClub(self, x, y, fg):
        ## draw a Club (10x10)
        self.display.vline(x+0, y+4, 2, fg)
        self.display.vline(x+1, y+3, 4, fg)
        self.display.vline(x+2, y+3, 4, fg)
        self.display.vline(x+3, y+1, 2, fg)
        self.display.vline(x+3, y+4, 2, fg)
        self.display.vline(x+4, y+0, 4, fg)
        self.display.vline(x+4, y+6, 4, fg)
        self.display.vline(x+5, y+0, 4, fg)
        self.display.vline(x+5, y+8, 2, fg)
        self.display.vline(x+6, y+1, 2, fg)
        self.display.vline(x+6, y+4, 2, fg)
        self.display.vline(x+7, y+3, 4, fg)
        self.display.vline(x+8, y+3, 4, fg)
        self.display.vline(x+9, y+4, 2, fg)
        
    def __drawSpade(self, x, y, fg):
        ## draw a Spade (10x10)
        self.display.vline(x+0, y+4, 1, fg)
        self.display.vline(x+1, y+3, 4, fg)
        self.display.vline(x+2, y+2, 5, fg)
        self.display.vline(x+3, y+1, 5, fg)
        self.display.vline(x+4, y+0, 10, fg)
        self.display.vline(x+5, y+0, 10, fg)
        self.display.vline(x+6, y+1, 5, fg)
        self.display.vline(x+7, y+2, 5, fg)
        self.display.vline(x+8, y+3, 4, fg)
        self.display.vline(x+9, y+4, 1, fg)

    def __drawHeart(self, x, y, fg):
        ## draw a Heart (10x10)
        self.display.vline(x+0, y+2, 2, fg)
        self.display.vline(x+1, y+1, 4, fg)
        self.display.vline(x+2, y+0, 7, fg)
        self.display.vline(x+3, y+1, 7, fg)
        self.display.vline(x+4, y+2, 8, fg)
        self.display.vline(x+5, y+2, 8, fg)
        self.display.vline(x+6, y+1, 7, fg)
        self.display.vline(x+7, y+0, 7, fg)
        self.display.vline(x+8, y+1, 4, fg)            
        self.display.vline(x+9, y+2, 2, fg)
        
    def __drawDiamond(self, x, y, fg):
        ## draw a Diamond (10x10)
        self.display.vline(x+0, y+4, 2, fg)
        self.display.vline(x+1, y+3, 4, fg)
        self.display.vline(x+2, y+2, 6, fg)
        self.display.vline(x+3, y+1, 8, fg)
        self.display.vline(x+4, y+0, 10, fg)
        self.display.vline(x+5, y+0, 10, fg)
        self.display.vline(x+6, y+1, 8, fg)
        self.display.vline(x+7, y+2, 6, fg)
        self.display.vline(x+8, y+3, 4, fg)
        self.display.vline(x+9, y+4, 2, fg)
        
    def __drawEnter(self, x, y, fg):
        ## draw Enter Key (8x8)
        self.display.vline(x+0, y+3, 5, fg)
        self.display.vline(x+1, y+6, 2, fg)
        self.display.pixel(x+2, y+5, fg)
        self.display.pixel(x+2, y+7, fg)
        self.display.pixel(x+3, y+5, fg)
        self.display.pixel(x+3, y+7, fg)
        self.display.pixel(x+4, y+4, fg)
        self.display.pixel(x+4, y+7, fg)
        self.display.vline(x+5, y+2, 2, fg)
        self.display.vline(x+6, y+0, 3, fg)
                
    def __drawBackspace(self, x, y, fg):
        ## draw Enter Key (8x8)
        self.display.pixel(x+0, y+3, fg)
        self.display.vline(x+1, y+2, 3, fg)
        self.display.vline(x+2, y+1, 2, fg)
        self.display.vline(x+2, y+4, 2, fg)
        self.display.vline(x+3, y+0, 2, fg)
        self.display.vline(x+3, y+5, 2, fg)
        self.display.pixel(x+4, y+3, fg)
        self.display.pixel(x+5, y+3, fg)
        self.display.pixel(x+6, y+2, fg)
        self.display.pixel(x+6, y+4, fg)

    def __drawShiftUp(self, x, y, fg):
        for n in range(2):
            self.display.pixel(x+3, y+4*n+0, fg)
            self.display.hline(x+2, y+4*n+1, 3, fg)
            self.display.hline(x+1, y+4*n+2, 2, fg)
            self.display.hline(x+4, y+4*n+2, 2, fg)
            self.display.hline(x+0, y+4*n+3, 2, fg)
            self.display.hline(x+5, y+4*n+3, 2, fg)
        

    def __drawShiftdown(self, x, y, fg):
        for n in range(2):
            self.display.pixel(x+3, y+4*n+3, fg)
            self.display.hline(x+2, y+4*n+2, 3, fg)
            self.display.hline(x+1, y+4*n+1, 2, fg)
            self.display.hline(x+4, y+4*n+1, 2, fg)
            self.display.hline(x+0, y+4*n+0, 2, fg)
            self.display.hline(x+5, y+4*n+0, 2, fg)
        

