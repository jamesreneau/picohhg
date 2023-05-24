""" Button - Use a pull up or down is needed.
Running of the buttonConfigure program will set the configuration
file and will be needed if the default (pull up) does not work.

Version 02
James M. Reneau Ph.D.
http://www.picohhg.com

This work is licensed under the Creative Commons Attribution-ShareAlike 2.0 Generic License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/2.0/ or send
a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

V
00		2023-05-08	jmr		original coding
01		2023-05-09	jmr		split onfig out to buttonConfigure
02		2023-05-14	jmr		added wait
"""

import os
from machine import Pin
import time

class Button():
    def __init__(self, GPIO):
        filename = "pulldown"+str(GPIO)+".cfg"
        if filename in os.listdir():
            pull = Pin.PULL_DOWN
        else:
            # default
            pull = Pin.PULL_UP

        self.pin = Pin(GPIO, Pin.IN, pull)
        self.unpressed = self.pin.value()
            
    def pressed(self):
        ## return True/False after debounce
        if self.pin.value() != self.unpressed:
            while self.pin.value() != self.unpressed:
                time.sleep(.1)
            return True   
        return False
    
    def wait(self):
        ## wait til press
        while True:
            if self.pressed():
                break
            time.sleep(.1)
        
    def waitRelease(self):
        ## wait til press
        while True:
            if not self.pressed():
                break
            time.sleep(.1)
            