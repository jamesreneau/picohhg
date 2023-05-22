""" Choosers - A collection of UI Widgets for the Pico (that will also
work on a console).

Version 02
James M. Reneau Ph.D.
http://www.picohhg.com

This work is licensed under the Creative Commons Attribution-ShareAlike 2.0 Generic License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/2.0/ or send
a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

V
00		2023-04-30	jmr		original coding
01		2023-05-08	jmr		changed button to use new button object
02		2023-05-14	jmr		adde choose ui widget
"""

import time
import math
import sys

if sys.implementation.name == 'micropython':
    from ssd1306 import SSD1306_I2C
    from machine import Pin
    from rotaryIRQ import RotaryIRQ

class ChooserBaseClass():
    """ ChooserBaseClass - Holds the UI classed for the pico. """
    
    CHARH = 10
    CHARW = 8
    
    def __init__(self, oled, rotary, button, prompt):
        self.oled = oled ## OLED Object
        self.rotary = rotary ## RotaryIRQ object
        self.button = button ## Button object for rotary button
        self.prompt = prompt
        
    def consoleNumber(self):
        """ get a number from the console """
        if self.prompt:
            print(self.prompt)
        while True:
            v = input(">>")
            try:
                v = float(v)
                if v >= self.minval and v < self.maxval:
                    return v
            except:
                pass
            print('A number between', self.minval, 'and', self.maxval)
            
class ChooserUIBase():
    def __init__(self, oled, x, y, text, w, h):
        self.oled = oled
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.hasFocus = False ## big border
        self.inverse = False ## inverse colors
          
    def fgColor(self):
        if self.inverse:
            return 0
        else:
            return 1
        
    def bgColor(self):
        if self.inverse:
            return 1
        else:
            return 0
        
    def draw(self):
        pass
    
    def erase(self):
        ## generic erase
        self.oled.fill_rect(self.x, self.y, self.w, self.h, self.bgColor())        

class ChooserUIText(ChooserUIBase):
    
    """
    create a ChooserUIText that will draw a rotatable text on the UI.
    """
    
    def __init__(self, oled, x, y, text=""):
        """
        Parameters:
        :x: column location of the top left corner
        :y: row location of the top left corner
        :text: Text to display on button 
        
        """
        w = ChooserBaseClass.CHARW * len(text)
        h = ChooserBaseClass.CHARH
        super().__init__(oled, x, y, text, w, h)

    def fgColor(self):
        # Invert XOR inverse or focus
        if bool(self.inverse) ^ bool(self.hasFocus):
            return 0
        else:
            return 1
        
    def bgColor(self):
        if bool(self.inverse) ^ bool(self.hasFocus):
            return 1
        else:
            return 0
        
    def draw(self):
        fg = self.fgColor()
        self.erase()
        self.oled.text(self.text, self.x, self.y, fg)
        
    def erase(self):
        self.oled.fill_rect(self.x, self.y, self.w, self.h, self.bgColor()) 
            
class ChooserUIButton(ChooserUIBase):
    
    """ create a ChooserUIButton (different from a button) that will draw a button on the UI.
    """
    
    def __init__(self, oled, x, y, text="", w=0, h=0, drawTextCall=None):
        """
        Parameters:
        :x: column location of the top left corner
        :y: row location of the top left corner
        :text: Text to display on button
        :drawTextCall: function to draw the text on the screen (oled, x, y) 
        
        """
        self.drawTextCall = drawTextCall
        super().__init__(oled, x, y, text, w, h)


    def draw(self):
        fg = self.fgColor()
        self.erase()
        ## draw border - 1 or 2 pixeld
        self.oled.rect(self.x, self.y, self.w, self.h, fg)
        if self.hasFocus:
            self.oled.rect(self.x+1, self.y+1, self.w-2, self.h-2, fg)
        #
        if self.text:
            self.oled.text(self.text, self.x + 3, self.y + 3, fg)
        if self.drawTextCall:
            self.drawTextCall(self.oled, self.x+3, self.y+3)

class ChooseString(ChooserBaseClass):
    """ ChooseString - displays an optional promot and allows user to enter one letter at a time
    to build a string.  The capital B is backspace, and the capital E is enter.  Soon will add uppercase
    and pretty glyphs for the actions """
    
    def __init__(self, oled, rotary, button, l=10, x=0, y=0, prompt=">", isPassword=False):
        super().__init__(oled, rotary, button, prompt)
        self.l = l	## max length
        self.x = x	## x pixel for top left
        self.y = y	## y pixel
        self.isPassword = isPassword
    
    def get(self):
        chars = "abcdefghijklmnopqrstuvwxyz BE"
        if sys.implementation.name == 'micropython':
            # clear field
            self.oled.fill_rect(self.x,self.y,(self.l+len(self.prompt))*ChooserBaseClass.CHARW,ChooserBaseClass.CHARH,0)
            self.oled.text(self.prompt, self.x, self.y)    
            l = 0
            s = ""
            while True:
                x = self.x + (len(self.prompt) + l) * ChooserBaseClass.CHARW
                c = ChooseList(self.oled, self.rotary, self.button, chars, x, self.y, prompt="").get()
                if c == 'E':
                    return s
                elif c == 'B':
                    self.oled.fill_rect(x,self.y,x+ChooserBaseClass.CHARW,ChooserBaseClass.CHARH,0)
                    l = l - 1
                    if l < 0:
                        l = 0
                    s = s[0:l]
                else:
                    self.oled.fill_rect(x,self.y,x+ChooserBaseClass.CHARW,ChooserBaseClass.CHARH,0)
                    if self.isPassword:
                        self.oled.text('*', x, self.y)
                    else:
                        self.oled.text(c, x, self.y)
                    s = s + c
                    l = l + 1
                    if l == self.l:
                        return s
        while True:
            txt = input(self.prompt)
            return txt.lower()

class ChooseList(ChooserBaseClass):
    """ ChooseList - Allow the user to scroll through a list of items and select one with a click
    of thr button. """
    
    def __init__(self, oled, rotary, button, options, x=0, y=0, prompt="??"):
        super().__init__(oled, rotary, button, prompt)
        self.options = options # list of pbtions
        self.x = x
        self.y = y
        
    def get(self):
        txt = '' ## last displayed
        ## show prompt
        if self.prompt:
            if sys.implementation.name == 'micropython':
                txt = self.prompt
                self.oled.fill_rect(self.x,self.y,len(txt)*ChooserBaseClass.CHARW,ChooserBaseClass.CHARH,1)
                self.oled.text(txt, self.x, self.y, 0)
                self.oled.show()
                v = self.rotary.value()
                while True:
                    if v != self.rotary.value() or self.button.pressed():
                        break
                    time.sleep(.1)
            else:
                ### Do it on the terminal
                print(self.prompt)
        ## now get option
        if sys.implementation.name == 'micropython':
            offset = self.rotary.value()
            v = math.inf
            while True:
                if v != self.rotary.value():
                    v = self.rotary.value()
                    if txt:                            
                        self.oled.fill_rect(self.x,self.y,len(txt)*ChooserBaseClass.CHARW,ChooserBaseClass.CHARH,0)
                    txt = self.options[(offset-v)%len(self.options)]
                    self.oled.fill_rect(self.x,self.y,len(txt)*ChooserBaseClass.CHARW,ChooserBaseClass.CHARH,1)
                    self.oled.text(txt, self.x, self.y, 0)
                    self.oled.show()
                # return current command after debounce
                if self.button.pressed():
                    if txt:                            
                        self.oled.fill_rect(self.x,self.y,len(txt)*ChooserBaseClass.CHARW,ChooserBaseClass.CHARH,0)
                        self.oled.show()
                    return txt
                time.sleep(.1)
        else:
            print(self.options)
            while True:
                txt = input(">>")
                if txt in self.options:
                    return txt
                if txt.upper() in self.options:
                    return txt.upper()

class ChooseUI(ChooserBaseClass):
    """ ChooseList - Allow the user to scroll through a list of UI widgets and select one with a click
    of thr button. Return the index in widget array. """
    
    def __init__(self, oled, rotary, button, widgets=[]):
        super().__init__(oled, rotary, button, "")
        self.widgets = widgets
        
    def get(self):
        offset = self.rotary.value()
        v = math.inf
        while True:
            newv = (- self.rotary.value()) % len(self.widgets)
            if v != newv:
                v = newv
                for i in range(len(self.widgets)):
                    self.widgets[i].hasFocus = i == v
                    self.widgets[i].draw()
                self.oled.show()
            # return current index
            if self.button.pressed():
                return v
            time.sleep(.1)

class ChooseRoundNumber(ChooserBaseClass):
    """ ChooseRoundNumber - Sshow a 360 degree face and allow the rotary to spin a hand.  The value
    is returned when the button is pressed. """
    def __init__(self, oled, rotary, button, prompt = '', minval = 0, maxval = 100, stepval = 1, marks=10):
        super().__init__(oled, rotary, button, prompt)
        self.minval = minval
        self.maxval = maxval
        self.stepval = stepval
        self.marks = marks
        ## center or face
        if sys.implementation.name == 'micropython':
            self.facex = int(oled.width*.75)
            self.facey = int(oled.height*.5)
            self.facer = int(oled.height*.5)
    
    def hand(self, v):
        """ draw the hand """
        pct = v/self.maxval - .25
        x = math.cos(pct*math.pi*2)*self.facer+self.facex
        y = math.sin(pct*math.pi*2)*self.facer+self.facey
        self.oled.line(self.facex, self.facer,int(x),int(y),1)

    def face(self):
        """ draw the face of the dial """
        for t in range(self.marks):
            pct = t/self.marks-.25
            x = math.cos(pct*math.pi*2)*self.facer+self.facex
            y = math.sin(pct*math.pi*2)*self.facer+self.facey
            x2 = math.cos(pct*math.pi*2)*self.facer*.9+self.facex
            y2 = math.sin(pct*math.pi*2)*self.facer*.9+self.facey
            self.oled.line(int(x2),int(y2),int(x),int(y),1)
        
    def get(self):
        ## now get option
        if sys.implementation.name == 'micropython':
            v = math.inf
            start = self.rotary.value()
            while True:
                newv = round((start - self.rotary.value()) % ((self.maxval - self.minval)/self.stepval)) * self.stepval + self.minval
                if v != newv:
                    v = newv
                    self.oled.fill(0)
                    self.face()
                    y = 0
                    if self.prompt:
                        self.oled.text(str(self.prompt),0,y)
                        y = y + ChooserBaseClass.CHARH
                    self.oled.text(str(v),0,y)
                    self.hand(v)
                    self.oled.show()
                # return current command after debounce
                if self.button.pressed():
                    return v
                time.sleep(.1)
        else:
            return self.consoleNumber()
 

class ChooseFaceNumber(ChooserBaseClass):
    """ ChooseFaceNumber shows a 1/2 face dial and allows a user to use the rotary and button to select a number. """
    
    def __init__(self, oled, rotary, button, prompt = "", minval = 0, maxval = 100, stepval = 1, marks=10):
        super().__init__(oled, rotary, button, prompt)
        self.minval = minval
        self.maxval = maxval
        self.stepval = stepval
        self.marks = marks
        ## center or face
        if sys.implementation.name == 'micropython':
            self.facex = int(oled.width*.5)
            self.facey = int(oled.height-1)
            self.facer = int(oled.height)
    
    def hand(self, v):
        pct = v/self.maxval/2 - .5
        x = math.cos(pct*math.pi*2)*self.facer+self.facex
        y = math.sin(pct*math.pi*2)*self.facer+self.facey
        self.oled.line(self.facex, self.facer,int(x),int(y),1)

    def face(self):
        for t in range(self.marks + 1):
            pct = t/(self.marks)/2-.5
            x = math.cos(pct*math.pi*2)*self.facer+self.facex
            y = math.sin(pct*math.pi*2)*self.facer+self.facey
            x2 = math.cos(pct*math.pi*2)*self.facer*.9+self.facex
            y2 = math.sin(pct*math.pi*2)*self.facer*.9+self.facey
            self.oled.line(int(x2),int(y2),int(x),int(y),1)
        
    def get(self):
        ## now get option
        if sys.implementation.name == 'micropython':
            v = math.inf
            start = self.rotary.value()
            while True:
                newv = (start - self.rotary.value()) * self.stepval + self.minval
                if newv < self.minval:
                    newv = self.minval
                if newv > self.maxval:
                    newv = self.maxval
                if v != newv:
                    v = newv
                    self.oled.fill(0)
                    self.face()
                    y = 0
                    if self.prompt:
                        self.oled.text(str(self.prompt),0,y)
                        y = y + 10
                    self.oled.text(str(v),0,y)
                    self.hand(v)
                    self.oled.show()
                # return current command after debounce
                if self.button.pressed():
                    return v
                time.sleep(.1)
        else:
            return self.consoleNumber()

class TextScroll(ChooserBaseClass):
    """ TextScroll displays text (wrapped by space) on the oled screen.  User can scroll up and down using
    the rotary.  Clickling the button exits. """
    def __init__(self, oled, rotary, button, text):
        super().__init__(oled, rotary, button, "")
        self.text = self.chopText(text)
        
    def chopText(self, text):
        chop = []
        for p in text:
            l = ""
            p = p.split(' ')
            for w in p:
                if len(l) + len(w) <= 15:
                    if l:
                        l = l + " "
                    l = l + w
                else:
                    chop.append(l)
                    l = w
            if l:
                chop.append(l)
            chop.append('')
        #print(len(chop))
        while len(chop) < 5:
            chop.append("")
        return chop
    
    def display(self):
        if sys.implementation.name == 'micropython':
            rows = 5
            v = math.inf
            start = self.rotary.value()
            while True:
                newv = start - self.rotary.value()
                if newv > len(self.text)-rows:
                    newv = len(self.text)-rows
                    start = self.rotary.value() + len(self.text)-rows
                if newv < 0:
                    newv = 0
                    start = self.rotary.value()
                if v != newv:
                    v = newv
                    self.oled.fill(0)
                    self.oled.fill_rect(0, 0 ,self.oled.width, 10, 1)
                    self.oled.text("< close > " + str(v) + '/' + str(len(self.text)-rows), 0, 0, 0)
                    for l in range(rows):
                        self.oled.text(self.text[v+l],0,l *10+10)
                    self.oled.show()
                # return current command after debounce
                if self.button.pressed():
                    return True
                time.sleep(.1)
        else:
            for l in self.text:
                print(l)    

           
class MessageBox(ChooserBaseClass):
    """ MessageBox displays lines of messages in the center of the screen and allow user to use the
    ChooseList to select a response to the message. """
    
    def __init__(self, oled, rotary, button, prompt='messagebox', options=['YES','NO']):
        super().__init__(oled, rotary, button, prompt)
        self.options = options # list of pbtions
        self.chooser = ChooseList(oled, rotary, button, options, 50, 50)
    
    def get(self):
        if sys.implementation.name == 'micropython':
            self.oled.fill(0)
            self.oled.rect(0, 0, self.oled.width, self.oled.height, 1)
            for i in range(len(self.prompt)):
                x = (128-len(self.prompt[i])*ChooserBaseClass.CHARW)//2
                y = i * 10 + 5
                self.oled.text(self.prompt[i], x, y)
            ans = self.chooser.get()
            return ans
        else:
            print(self.prompt)
            return self.chooser.get()
