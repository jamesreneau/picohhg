""" SST - Super Star Trekking

Version 02
James M. Reneau Ph.D.
http://www.picohhg.com

This work is licensed under the Creative Commons Attribution-ShareAlike 2.0 Generic License.
To view a copy of this license, visit http://creativecommons.org/licenses/by-sa/2.0/ or send
a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

V
00		2023-04-30	jmr		original coding
01		2023-05-08	jmr		changed button and removed Empty object
02		2023-05-09	jmr		added quit
"""
import sys
if sys.implementation.name == 'micropython':
    from machine import Pin
    from machine import I2C
    from rotaryIRQ import RotaryIRQ
    from ssd1306 import SSD1306_I2C
    from button import Button
    
    # Hardware GPIO Pins used for Raspberry PI Pico
    I2CSDA = 16
    I2CSCL = 17
    ROTARY_CLOCK = 7
    ROTARY_DATA = 6
    BUTTON = 26
    
    i2c = I2C(0, sda=Pin(I2CSDA), scl=Pin(I2CSCL), freq=400000)
    oled = SSD1306_I2C(128, 64, i2c)
    rotary = RotaryIRQ(ROTARY_CLOCK, ROTARY_DATA)
    button = Button(BUTTON)
else:
    oled = False
    rotary = False
    button = False

import time
import math
import random
from choosers import ChooseList
from choosers import ChooseRoundNumber
from choosers import ChooseFaceNumber
from choosers import TextScroll
from choosers import MessageBox

class Static():
    
    VERSION = "02"

    MAXX = 64	## size of the Universe
    MAXY = 64
    SECX = 8	# size of a sector
    SECY = 8
    
    # objects in the universe tpes
    STAR = 0
    BASE = 1
    KLINGON = 2
    ENTERPRISE = 3
    NAMES = ['Star', 'Star Base', 'Klingon', 'USS Enterprise']

    ENERGY_MAX = 10000
    ENERGY_YELLOW = 1000

    PHO_MAX = 10
    PHO_DIST = 12		## max distance a photon torpedo travels
    
    PHA_MAXE = 1000		##  maximum phaser discharge
    
    STARS_MAX = 200
    STARS_PCT_PLANETS = .20	## % of stars with mineable planets
    
    BASES_MAX = 8
    BASE_ENERGY = 5000		## max shield energy for a base
    BASE_REGEN = .10		## percent regen up to max energy per stardate
    
    KLINGONS_MAX = 18		## max number of klingons
    KLINGON_ENERGY = 3000	## maximum energy of a klingom
    KLINGON_ENTERPRISE_AGRESSION = .9	## klingons attach this often
    KLINGON_BASE_AGRESSION = .1	## klingons attach this often
    KLINGON_REGEN = .10		## percent regen up to max energy per stardate
    KLINGON_MOVE = 4		## coordinates klingons may move in a stardate

    IMP_TIME = 1
    IMP_E = 200
    
    WRP_TIME = .5
    WRP_E = 200
    
    DOK_TIME = 2
    
    MNE_ENERGY = 12345		## maximum energy available to mine
    MNE_TIME = 3			## maximum time to mine a planet
    
    ABOUT = [
        "Welcome to SST for the Raspberry PI PICO.",
        VERSION,
        "c) J.M.Reneau",
        "Your mission is to explore brave new worlds and to eradicate the Klingon menace from the known universe.",
        "The Universe is made of a grid of 8x8 sectors divided up into 8x8 coordinates.",
        "Use the spinner to select a command or value and then press the spinner to execute.",
        "About:",
        "I remember playing SST on the Pr1me computer at Morehead State University in the '80s. It was probably the FORTRAN SST from Austin but the code has been lost for decades.",
        "This game is close to what I can remember from playing it all those years ago with many subtle and not so subtle differences.",
        "Have fun.",
        "c) J.M.Reneau - All Rights Reserved. jim@renejm.com"
        ]

    COMMANDS = ["LRS", "SRS", "MAP", "FSC", "IMP", "WRP", "PHA", "PHO", "DOK", "MNE", "HAI", "WAI", "SD!", "HELP"]

    HELP = [
        "HELP - Captian's Manual",
        "Command Reference",
        "LRS - Long Range Scanners show the current and surrounding sectors as a three digit number. The first"
            " is the number of Klingons, second Bases, and third stars.",
        "SRS - Short Range Scanners show the current sector and position of bases (squares), stars with planets"
            " (solar system), stars, Klingons, and the Enterprise.",
        "MAP - Show map of klingons, bases, and stars based on composite LRS and SRS scans.",
        "FSC - Fire Solutions Calculator shows the heading and distance to all objects in the sector.",
        "IMP - IMPulse drive to move within a 10 coordinate area.  You will be asked for heading and distance"
            " (in coordinates). You can not navigare into an occupied coordinate or off of the edge of the universe.",
        "WRP - WaRP drive to move from sector to sector. You will be asked for heading and distance (in in sectors)."
            " If you navigate into an obstical or the edge of the universe, you will be placed near it.",
        "PHA - PHAser - Fire energy beam at Klingons in sector. You may only fire 1000 units or 1/4 of the reserves,"
            " whichever is less.",
        "PHO - PHOton - Fire a photon torpedo in a speciied direction. Be careful not to hit unintended objects.",
        "DOK - DOcKing - You may dock with an adjacent star base to top off yor energy reserves and torpedo racks.",
        "MNE - MiNE a Planet - You may send an away party down to the planet to mine dilithium to add to the ship's"
            " energy reserves.",
        "HAI - HAIl - Communicate with... (Not implemented)",
        "HELP - Read this helpful summary.",
        "SD! - SELF DESTRUCT! When all is lost you may end the game the cowards way."
        ]
    
    @staticmethod
    def goodxy(x, y):
        return x >= 0 and y >= 0 and x < Static.MAXX and y < Static.MAXY
    
    @staticmethod
    def xyToString(x, y):
        #print(x,y)
        return str(int(x)//Static.SECX) + "," + str(int(y)//Static.SECY) + ' ' + str(int(x)%Static.SECX) + "," + str(int(y)%Static.SECY)
    
    @staticmethod
    def halfRandom(v):
        ## return a random decimal between 1/2v and 1v
        return v / 2 * random.random() + v / 2
    
    @staticmethod
    def halfRandomInt(v):
        return int((v / 2 + 1) * random.random()) + v // 2
    
    @staticmethod
    def DistHead(x0, y0, x1, y1):
        # find distance and heading from origin (0) to destintion(1)
        # heading are angle clockwise from 0000 (clock face as angle)
        dx = x1-x0	# +right, -left
        dy = y1-y0	# +down, -up
        d = ((dx)**2 + (dy)**2)**.5
        if d > 0:
            if dy <= 0 and dx >= 0:
                # quad 0 0-3
                h = math.asin(dx/d)*180/math.pi
            elif dy > 0 and dx >=0:
                # quad 1 3-6
                h = 180 - math.asin(dx/d)*180/math.pi
            elif dy > 0 and dx < 0:
                # quad 3 6-9
                h = 180 + math.asin(abs(dx)/d)*180/math.pi
            else:
                # quad 4 9-12
                h = 360 - math.asin(abs(dx)/d)*180/math.pi
        else:
            h = math.inf
        return(d, h)
    
    @staticmethod
    def intToString1(n):
        # convert an int to a one character
        if n >= 0 and n <= 9:
            return str(n)
        else:
            return '+'
                
    @staticmethod
    def countsToString(counts):
        ## take counts list (from universe) and return a three character string
        if counts:
            return Static.intToString1(counts[Static.KLINGON]) + Static.intToString1(counts[Static.BASE]) + Static.intToString1(counts[Static.STAR])
        else:
            return '???'

        
""" base class of stars, bases, and klingons. everything has a position and energy """
class Stuff():
    def __init__(self, universe, typeNumber, x, y, e):
        self.universe = universe
        self.type = typeNumber
        self._x = x
        self._y = y
        self. _addLocationIndex()
        self.e = e
        # add to the location xref

        
    def _delLocationIndex(self):
        ## if x or y is being changed remove it from the locationIndex of the universe 
        del self.universe.locationIndex[(self._x,self._y)]
        
    def _addLocationIndex(self):
        ## afrer x or y was changed add it from the locationIndex of the universe 
        self.universe.locationIndex[(self._x,self._y)] = self
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._delLocationIndex()
        self._x = value
        self._addLocationIndex()
        
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._delLocationIndex()
        self._y = value
        self._addLocationIndex()

        
    def name(self):
        return Static.NAMES[self.type]
    
    
    def remove(self):
        ## remove an object from the universe (Kill or blow up)
        self._delLocationIndex()
        self.universe.objects.remove(self)
    
    def __str__(self):
        return "t"+str(self.type)+" x"+str(self.x)+" y"+str(self.y)+" e"+str(self.e)

class Enterprise(Stuff):
    def __init__(self, universe, x, y):
        e = Static.halfRandom(Static.ENERGY_MAX)
        super().__init__(universe, Static.ENTERPRISE, x, y, e)
        self.pho = Static.PHO_MAX

class Klingon(Stuff):
    def __init__(self, universe, x, y):
        e = Static.halfRandomInt(Static.KLINGON_ENERGY)
        super().__init__(universe, Static.KLINGON, x, y, e)
        
    def randomMove(self, days):
        ## klingons move a little when we do longer things
        a = random.random() * 2 * math.pi
        d = Static.halfRandomInt(round(Static.KLINGON_MOVE * days))
        if d >0:
            x = int(self.x + math.sin(a) * d)
            y = int(self.y + math.cos(a) * d)
            if x >=0 and x <= Static.MAXX and y >=0 and y <= Static.MAXY:
                if not self.universe.getObjAt(x,y):
                    print("K moved from", self.x, self.y, "to", x, y)
                    self.x = x
                    self.y = y
    
class Star(Stuff):
    """ create a star with random minable planets """
    def __init__(self, universe, x, y):
        self.hasPlanet = random.random() < Static.STARS_PCT_PLANETS
        e = 0
        if self.hasPlanet:
            e = Static.halfRandomInt(Static.MNE_ENERGY)
        super().__init__(universe, Static.STAR, x, y, e)
    
class Base(Stuff):
    def __init__(self, universe, x, y):
        e = Static.halfRandomInt(Static.BASE_ENERGY)
        super().__init__(universe, Static.BASE, x, y, e)   
    

class Universe():    
    def __init__(self):
        self.objects = []			## list of all objcts in universe
        self.locationIndex = {}		## fast way to search by location [(x,y)]
        self.enterprise = None
        
    def getObjAt(self, x, y):
        ## return the object at a location or False if location is empty
        return self.locationIndex.get((x,y), False)
        
    def findSpace(self):
        # return (x, y) of empty space
        while True:
            x = int(random.random()*Static.MAXX)
            y = int(random.random()*Static.MAXY)
            if not self.getObjAt(x,y):
                return (x, y)
            
    def findSpaceNear(self, x, y):
        ## return r,c of enpty space near passed rc
        while True:
            if x < 0:
                x = 0
            if y < 0:
                y = 0
            if x >= Static.MAXX:
                x = Static.MAXX-1
            if y >= Static.MAXY:
                y = Static.MAXY-1
            if not self.getObjAt(x,y):
                return (x,y)
            x = x + int(random.random()*3) - 1
            y = y + int(random.random()*3) - 1
            
    def isAdjacent(self, x, y, typeNumber):
        ## return object if we are adjacent to an object of that type
        ## else return False
        for dx in range(-1,2):
            for dy in range(-1,2):
                if Static.goodxy(x+dx, y+dy):
                    obj = self.getObjAt(x+dx, y+dy)
                    if obj and obj.type == typeNumber:
                            return obj
        else:
            return False
                        

    def fillSpace(self):
        #
        # add Enterprise
        x,y = self.findSpace()
        self.enterprise = Enterprise(self, x, y)
        self.objects.append(self.enterprise)
        #
        # add stars (some have planets)
        for n in range( Static.halfRandomInt(Static.STARS_MAX)):
            x,y = self.findSpace()
            self.objects.append(Star(self, x, y))
        #
        # add bases
        for n in range(Static.halfRandomInt(Static.BASES_MAX)):
            x,y = self.findSpace()
            self.objects.append(Base(self, x, y))
        #
        # add KLINGONS
        for n in range(Static.halfRandomInt(Static.KLINGONS_MAX)):
            x,y = self.findSpace()
            self.objects.append(Klingon(self, x, y))

    def countSpace(self):
        ## return list of counts (0-4)
        counts = [0,0,0,0,0]
        for obj in self.objects:
            if obj:
                counts[obj.type] = counts[obj.type] + 1
        return counts
    
    def countSector(self, x, y):
        ## return list of counts (0-4)
        if Static.goodxy(x,y):
            counts = [0,0,0,0,0]
            for obj in self.objects:
                if obj and x//Static.SECX == obj.x//Static.SECX and y//Static.SECY == obj.y//Static.SECY:
                    counts[obj.type] = counts[obj.type] + 1
            return counts
        else:
            return False
    
    def selectSector(self, x, y, type):
        ##given xy coord find all objects of a type in sector and return 
        list = []
        if Static.goodxy(x,y):
            counts = [0,0,0,0,0]
            for obj in self.objects:
                if x//Static.SECX == obj.x//Static.SECX and y//Static.SECY == obj.y//Static.SECY and obj.type == type:
                    list.append(obj)
        return list
        
class Game():

    def __init__(self):            
        self.game_on = True
        
    def tick(self, days):
        # add days to stardate
        self.stardate = self.stardate + days
        # add back energy to klingons (prorated by days)
        for obj in self.universe.objects:
            if obj and obj.type == Static.KLINGON:
                obj.e = obj.e + obj.e * Static.KLINGON_REGEN * days
                if obj.e > Static.KLINGON_ENERGY:
                    obj.e = Static.KLINGON_ENERGY
                #
                obj.randomMove(days)
        # regenerate bases (prorated by days)
        for obj in self.universe.objects:
            if obj and obj.type == Static.BASE:
                obj.e = obj.e + obj.e * Static.BASE_REGEN * days
                if obj.e > Static.BASE_ENERGY:
                    obj.e = Static.BASE_ENERGY
        
    
    def display_status(self):
        #### STANDARD DISPLAY
        if sys.implementation.name == 'micropython':
            oled.fill(0)
        #
        if self.universe.enterprise.e < Static.ENERGY_YELLOW:
            status = "YELLOW"
        elif self.sector_counts[Static.KLINGON]:
            status="RED"
        else:
            status="Green"
        if sys.implementation.name == 'micropython':
            oled.text(status,0,10)
        else:
            print("Status:", status)
        #    
        sd = round(self.stardate,1)
        if sys.implementation.name == 'micropython':
            oled.text(str(sd),0,20)
        else:
            print("Star Date:", sd)
        #
        loc = Static.xyToString(self.universe.enterprise.x, self.universe.enterprise.y)
        if sys.implementation.name == 'micropython':
            oled.text(loc,0,30)
        else:
            print("Location:", loc)
        #
        if sys.implementation.name == 'micropython':
            oled.text("e " + str(round(self.universe.enterprise.e)),0,40)
        else:
            print("Energy:", str(self.universe.enterprise.e))
        #
        if sys.implementation.name == 'micropython':
            oled.text("pho " + str(self.universe.enterprise.pho),0,50)
        else:
            print("Torpedos:", str(self.universe.enterprise.pho))
        #
        if sys.implementation.name == 'micropython':
            oled.text("KGS " + str(self.universe_counts[Static.KLINGON]),64,10)
        else:
            print("Klingons:", str(self.universe_counts[Static.KLINGON]))
        #
        if sys.implementation.name == 'micropython':
            oled.text("Bases " + str(self.universe_counts[Static.BASE]),64,20)
        else:
            print("Bases:", str(self.universe_counts[Static.BASE]))
            
    def srs(self):
        if sys.implementation.name == 'micropython':
            tx = 20
            ty = 0
            dx = 8
            dy = 7
            oled.fill(0)
            ## show numbers
            for n in range(8):
                oled.text(str(n), tx + n*dx + dx, ty)
                oled.text(str(n), tx, ty + n*dy + dy)
            ##
            for x in range(Static.SECX):
                for y in range(Static.SECY):
                    ux = self.universe.enterprise.x//Static.SECX*Static.SECX+x
                    uy = self.universe.enterprise.y//Static.SECY*Static.SECY+y
                    u = self.universe.getObjAt(ux, uy)
                    c = tx + x*dx + dx
                    r = ty + y*dy + dy
                    if not u:
                        ## empty
                        oled.pixel(c+3, r+3, 1)
                    elif u.type == Static.ENTERPRISE:
                        ## THIS SHIP
                        oled.pixel(c, r+3, 1)
                        oled.vline(c+1, r+2, 3, 1) 
                        oled.vline(c+2, r+1, 5, 1) 
                        oled.vline(c+3, r+2, 3, 1) 
                        oled.pixel(c+4, r+3, 1)
                        oled.hline(c+4, r, 3, 1)
                        oled.hline(c+4, r+1, 3, 1)
                        oled.hline(c+4, r+5, 3, 1)
                        oled.hline(c+4, r+6, 3, 1)
                    elif u.type == Static.STAR:
                        if u.hasPlanet:
                            oled.hline(c+2, r+1, 3, 1)
                            oled.hline(c+2, r+5, 3, 1)
                            oled.vline(c+1, r+2, 3, 1)
                            oled.vline(c+5, r+2, 3, 1)
                            oled.pixel(c+3, r+3, 1)
                        else:
                            oled.pixel(c+3, r+1)
                            oled.hline(c+2, r+2, 3, 1)
                            oled.hline(c+1, r+3, 5, 1)
                            oled.hline(c+2, r+4, 3, 1)
                            oled.pixel(c+3, r+5)
                    elif u.type == Static.BASE:
                        oled.hline(c, r,7,1)
                        oled.hline(c, r+6,7,1)
                        oled.vline(c, r+1,6,1)
                        oled.vline(c+6, r+1,6,1)
                    elif u.type == Static.KLINGON:
                        oled.vline(c, r+3, 4, 1)
                        oled.vline(c+1, r+3, 4, 1)
                        oled.vline(c+2, r+2, 4, 1)
                        oled.vline(c+3, r, 5, 1)
                        oled.vline(c+4, r+2, 4, 1)
                        oled.vline(c+5, r+3, 4, 1)
                        oled.vline(c+6, r+3, 4, 1)
            ChooseList(oled, rotary, button, ["OK"], 0, 0, "").get()
        else:
            # terminal
            print("  01234567")
            for y in range(Static.SECX):
                line = str(y) + " "
                for x in range(Static.SECY):
                    ux = self.universe.enterprise.x//Static.SECX*Static.SECX+x
                    uy = self.universe.enterprise.y//Static.SECY*Static.SECY+y
                    u = self.universe.getObjAt(ux, uy)
                    if not u:
                        line = line + '.'
                    elif u.type == Static.STAR:
                        if u.hasPlanet:
                            line = line + "P"
                        else:
                            line = line + "*"
                    elif u.type == Static.KLINGON:
                        line = line + 'K'
                    elif u.type == Static.BASE:
                        line = line + 'B'
                    elif u.type == Static.ENTERPRISE:
                        line = line + 'E'
                print(line)

        ## add SRS to map
        counts = self.universe.countSector(self.universe.enterprise.x, self.universe.enterprise.y)
        self.mapdata[self.universe.enterprise.y//Static.SECY][self.universe.enterprise.x//Static.SECX] = counts

    def lrs(self):
                
        def _score(x, y):
            ## for sector containing x, y return kbs (klingons, bases, stars)
            counts = self.universe.countSector(x, y)
            if counts:
                self.mapdata[y//Static.SECY][x//Static.SECX] = counts
            return Static.countsToString(counts)
        
        dx = (-Static.SECX, 0, Static.SECX)
        dy = (-Static.SECY, 0, Static.SECY)
        
        if sys.implementation.name == 'micropython':
            oled.fill(0)
            c = (int(2*8), int(6.5*8), int(11*8))
            r = (15, 30, 45)
            oled.text(_score(self.universe.enterprise.x+dx[0], self.universe.enterprise.y+dy[0]), c[0], r[0])
            oled.text(_score(self.universe.enterprise.x+dx[0], self.universe.enterprise.y+dy[1]), c[0], r[1])
            oled.text(_score(self.universe.enterprise.x+dx[0], self.universe.enterprise.y+dy[2]), c[0], r[2])
            oled.text(_score(self.universe.enterprise.x+dx[1], self.universe.enterprise.y+dy[0]), c[1], r[0])
            oled.text(_score(self.universe.enterprise.x+dx[1], self.universe.enterprise.y+dy[1]), c[1], r[1])
            oled.text(_score(self.universe.enterprise.x+dx[1], self.universe.enterprise.y+dy[2]), c[1], r[2])
            oled.text(_score(self.universe.enterprise.x+dx[2], self.universe.enterprise.y+dy[0]), c[2], r[0])
            oled.text(_score(self.universe.enterprise.x+dx[2], self.universe.enterprise.y+dy[1]), c[2], r[1])
            oled.text(_score(self.universe.enterprise.x+dx[2], self.universe.enterprise.y+dy[2]), c[2], r[2])
            ChooseList(oled, rotary, button, ["OK"], 0, 0, "").get()
        else:
            print(_score(self.universe.enterprise.x+dx[0], self.universe.enterprise.y+dy[0]),
                _score(self.universe.enterprise.x+dx[1], self.universe.enterprise.y+dy[0]),
                _score(self.universe.enterprise.x+dx[2], self.universe.enterprise.y+dy[0]))
            print(_score(self.universe.enterprise.x+dx[0], self.universe.enterprise.y+dy[1]),
                _score(self.universe.enterprise.x+dx[1], self.universe.enterprise.y+dy[1]),
                _score(self.universe.enterprise.x+dx[2], self.universe.enterprise.y+dy[1]))
            print(_score(self.universe.enterprise.x+dx[0], self.universe.enterprise.y+dy[2]),
                _score(self.universe.enterprise.x+dx[1], self.universe.enterprise.y+dy[2]),
                _score(self.universe.enterprise.x+dx[2], self.universe.enterprise.y+dy[2]))
                
    def map(self):
        txt = []
        for object in (Static.KLINGON, Static.BASE, Static.STAR):
            txt.append("Map of " + Static.NAMES[object] + 's')
            txt.append("* 01234567")
            for y in range(Static.SECY):
                line = str(y)+' '
                for x in range(Static.SECX):
                    if self.mapdata[y][x]:
                        line = line + str(self.mapdata[y][x][object])
                    else:
                        line = line + ' '
                txt.append(line)
            txt.append('------------')
        return txt
    
    def fsc(self):
        text = ["FSC"]
        ex = self.universe.enterprise.x
        ey = self.universe.enterprise.y
        for x in range(Static.SECX):
            for y in range(Static.SECY):
                ux = ex//Static.SECX*Static.SECX+x
                uy = ey//Static.SECY*Static.SECY+y
                u = self.universe.getObjAt(ux, uy)
                if u and u.type != Static.ENTERPRISE:
                    d, h = Static.DistHead(ex, ey, ux, uy)
                    text.append("The "+ u.name() +
                        " at " + str(ux%8) + "," + str(uy%8) +
                        " is at heading " + str(round(h,0)) +
                        " and distance " + str(round(d,1)) + '.')
        TextScroll(oled, rotary, button, text).display()
        
    def imp(self, heading, dist):
        # impluse drive
        y = round(math.cos((heading-180) / 180 * math.pi) * dist + self.universe.enterprise.y)
        x = round(math.sin((heading) / 180 * math.pi) * dist + self.universe.enterprise.x)
        #print("IMP", heading, self.universe.enterprise.x,self.universe.enterprise.y, "--", x, y)
        if Static.goodxy(x,y):
            if self.universe.getObjAt(x,y):
                TextScroll(oled, rotary, button, [
                    "IMP - Order belayed.",
                    "Destination coordinates are not empty."
                    ]).display()
            else:
                self.universe.enterprise.x, self.universe.enterprise.y = self.universe.findSpaceNear(x, y)
                self.universe.enterprise.e = self.universe.enterprise.e - Static.halfRandom(Static.IMP_E * dist)
                self.tick(Static.halfRandom(Static.IMP_TIME * dist))
        else:
            TextScroll(oled, rotary, button, [
                "IMP - Order belayed.",
                "Destination out of known universe."
                ]).display()
        
    def wrp(self, heading, dist):
        # warp drive - Bends space so you bounce on the edge and dont land on anythong
        y = round(math.cos((heading-180) / 180 * math.pi) * dist * Static.SECX + self.universe.enterprise.y)
        x = round(math.sin(heading / 180 * math.pi) * dist * Static.SECY + self.universe.enterprise.x)
        ###print("WRP", heading, self.universe.enterprise.x,self.universe.enterprise.y, "--", x, y)
        if Static.goodxy(x,y):
            self.universe.enterprise.x, self.universe.enterprise.y = self.universe.findSpaceNear(x, y)
            self.universe.enterprise.e = self.universe.enterprise.e - Static.halfRandom(Static.WRP_E * dist)
            self.tick(Static.halfRandom(Static.WRP_TIME*dist))
        else:
            TextScroll(oled, rotary, button, [
                "WRP - Order belayed.",
                "Destination out of known universe."
                ]).display()
        
    def pho(self, heading):
        text = ["PHO"]
        if self.universe.enterprise.pho == 0:
            text.append("You don't have any torpedos to fire.")
        else:
            self.universe.enterprise.pho = self.universe.enterprise.pho - 1
            dx = math.sin(heading / 180 * math.pi)
            dy = math.cos((heading-180) / 180 * math.pi)
            x = self.universe.enterprise.x
            y = self.universe.enterprise.y
            text.append("Track:")
            for t in range(Static.PHO_DIST):
                x = x + dx
                y = y + dy
                rx = round(x)
                ry = round(y)
                text[1] = text[1] + ' (' + str(rx%Static.SECX) + "," + str(ry%Static.SECY) + ')'
                if rx < 0 or rx >= Static.MAXX or ry < 0 or ry >= Static.MAXY:
                    text.append("Photon Torpedo has left known space.")
                    break
                u = self.universe.getObjAt(rx, ry)
                if not u:
                    pass
                elif u.type == Static.ENTERPRISE:
                    pass
                elif u.type == Static.KLINGON:
                    text.append("Klingon destroyed.")
                    u.remove()
                    break
                elif u.type == Static.BASE:
                    text.append("Base destroyed. You have been found guilty of Treason and pushed out an airlock.")
                    u.remove()
                    self.game_on = False
                    break
                elif u.type == Static.STAR:
                    text.append("Star destroyed. It is a really bad idea to launch a torpedo into a star.")
                    text.append("The resulting supernova just destroyed the Enterprise.")
                    u.remove()
                    self.game_on = False
                    break
        TextScroll(oled, rotary, button, text).display()

    def pha(self):
        text = ["PHA"]
        ex = self.universe.enterprise.x
        ey = self.universe.enterprise.y
        for x in range(Static.SECX):
            for y in range(Static.SECY):
                ux = ex//Static.SECX*Static.SECX+x
                uy = ey//Static.SECY*Static.SECY+y
                u = self.universe.getObjAt(ux, uy)
                if u and u.type == Static.KLINGON:
                    avail = int(min(self.universe.enterprise.e/2, Static.PHA_MAXE))
                    e =  ChooseFaceNumber(oled, rotary, button,
                        "PHA to ("+str(ux%Static.SECX)+','+str(uy%Static.SECY) + ')'
                        , 0, avail, int(avail/11)).get()
                    self.universe.enterprise.e = self.universe.enterprise.e - e
                    d, h =  Static.DistHead(ex, ey, ux, uy)
                    e = e * (4/d)
                    u.e = u.e - e
                    if u.e < 0:
                        text.append("Klingon at (" + str(ux%Static.SECX) + ',' + str(uy%Static.SECY) + ') Destroyed.')
                        u.remove()
                    else:
                        text.append("Klingon at (" + str(ux%Static.SECX) + ',' + str(uy%Static.SECY) + ') Damaged by ' +
                            str(round(e)) + ' units.')
        TextScroll(oled, rotary, button, text).display()
                
        
    def run(self):
        ## init run
        self.stardate = 2500 + random.random() * 50
        self.universe = Universe()
        self.universe.fillSpace()
        self.universe_counts = self.universe.countSpace()
        # init map
        self.mapdata = []
        for x in range(Static.SECX):
            self.mapdata.append([False]*Static.SECY)
        
        self.game_on = True
        
        # main run loop
        while True:
            startcmd = MessageBox(oled, rotary, button, ["SST", "Do you accept",
                "command of the","USS Enterprise?"],['ACCEPT', 'ABOUT', 'QUIT']).get()
            if startcmd=="ABOUT":
                TextScroll(oled, rotary, button, Static.ABOUT).display()
            if startcmd=="QUIT":
                break
            elif startcmd=="ACCEPT":
                cmd = ""
                while self.game_on:
                    self.sector_counts = self.universe.countSector(self.universe.enterprise.x, self.universe.enterprise.y)
                    self.display_status()
                    
                    cmd = ChooseList(oled, rotary, button, Static.COMMANDS, 0, 0, "").get()
                    if cmd == "SD!":
                        if MessageBox(oled, rotary, button, ["SST", "Self Destruct?"]).get() == 'YES':
                            self.game_on = False
                    elif cmd == "LRS":
                        self.lrs()
                    elif cmd == "SRS":
                        self.srs()
                    elif cmd == "MAP":
                        #show pre-processed map text 
                        map = TextScroll(oled, rotary, button, [])
                        map.text = self.map()
                        map.display()
                    elif cmd == "FSC":
                        self.fsc()
                    elif cmd == "IMP":
                        heading =  ChooseRoundNumber(oled, rotary, button, "IMP Heading", 0, 360, 5, 8).get()
                        dist =  ChooseFaceNumber(oled, rotary, button, "Distance (coord)", 0, 10, 1).get()
                        self.imp(heading, dist)
                    elif cmd == "WRP":
                        heading =  ChooseRoundNumber(oled, rotary, button, "WRP Heading", 0, 360, 5, 8).get()
                        dist =  ChooseFaceNumber(oled, rotary, button, "Distance (sect)", 0, 8, .25, 8).get()
                        self.wrp(heading, dist)
                    elif cmd == "PHA":
                        self.pha()
                    elif cmd == "PHO":
                        heading =  ChooseRoundNumber(oled, rotary, button, "PHO Heading", 0, 360, 5, 8).get()
                        self.pho(heading)
                    elif cmd == "DOK":
                        obj = self.universe.isAdjacent(self.universe.enterprise.x, self.universe.enterprise.y, Static.BASE)
                        if obj:
                            self.universe.enterprise.e = Static.ENERGY_MAX
                            self.universe.enterprise.pho = Static.PHO_MAX
                            self.tick(Static.halfRandom(Static.DOK_TIME))
                            TextScroll(oled, rotary, button, [
                                "DOK - The tanks have been filled to capacity with dilithium and the torpedo racks are full.",
                                "The base at " + Static.xyToString(obj.x, obj.y) + " said 'Good luck captian.'"
                                ]).display()
                        else:
                            TextScroll(oled, rotary, button, [
                                "DOK - You are not adjcent to a star base.",
                                ]).display()
                    elif cmd == "MNE":
                        obj = self.universe.isAdjacent(self.universe.enterprise.x, self.universe.enterprise.y, Static.STAR)
                        if obj:
                            if obj.hasPlanet:
                                # find needed or existing e
                                e = min(obj.e, Static.ENERGY_MAX - self.universe.enterprise.e) 
                                # Take energy and KILL PLANET
                                self.universe.enterprise.e = self.universe.enterprise.e + e
                                obj.e = obj.e - e
                                if obj.e == 0:
                                    obj.hasPlanet = False
                                self.tick(Static.halfRandom(Static.MNE_TIME))
                                #
                                TextScroll(oled, rotary, button, [
                                    "MNE - You were able to mine the star at " + Static.xyToString(obj.x, obj.y) + " for " + str(e)+" units of dilithium."
                                    ]).display()
                            else:
                                TextScroll(oled, rotary, button, [
                                    "MNE - The star you are adjcent to does not have a planet.",
                                    ]).display()
                        else:
                            TextScroll(oled, rotary, button, [
                                "MNE - You are not adjcent to a star.",
                                ]).display()
                    elif cmd == "HAI":
                        TextScroll(oled, rotary, button, [
                            "HAI - Communications Not Installed.",
                            ]).display()
                    elif cmd == "WAI":
                        days =  ChooseFaceNumber(oled, rotary, button, "Wait - Repair", 0, 5, .25).get()
                        self.tick(days)
                    elif cmd== "HELP":
                        TextScroll(oled, rotary, button, Static.HELP ).display()

                    ## each move causes tick to happen
                    self.tick(1/12)
                    
                    ## Klingons attack!!!!
                    klingons = self.universe.selectSector(self.universe.enterprise.x, self.universe.enterprise.y, Static.KLINGON)
                    for k in klingons:
                        if random.random() <= Static.KLINGON_ENTERPRISE_AGRESSION:
                            e = k.e * .25
                            k.e = k.e - e
                            self.universe.enterprise.e = self.universe.enterprise.e- e
                            TextScroll(oled, rotary, button, [
                                "Klingon at (" + str(k.x%Static.SECX) + ',' + str(k.y%Static.SECY) + ') did ' +
                                str(round(e)) + ' damage to the Enterprise with a disruptor.'
                                ]).display()

                    ## need to attack bases
                    for obj in self.universe.objects:
                        if obj and obj.type == Static.BASE:
                            klingons = self.universe.selectSector(obj.x, obj.y, Static.KLINGON)
                            for k in klingons:
                                if random.random() <= Static.KLINGON_BASE_AGRESSION:
                                    e = k.e * .25
                                    k.e = k.e - e
                                    obj.e = obj.e- e
                                    if obj.e <= 0:
                                        TextScroll(oled, rotary, button, [
                                            "SUBSPACE COMM:",
                                            "Base at " + Static.xyToString(obj.x, obj.y) + " has been destroyed."
                                            ]).display()
                                        obj.remove()
                                    else:
                                        TextScroll(oled, rotary, button, [
                                            "SUBSPACE COMM:",
                                            "Base at " + Static.xyToString(obj.x, obj.y) + " is under attcack. Please send assistance."
                                            ]).display()
                                    
                
                    ## check condition after move
                    if self.universe.enterprise.e <= 0:
                        TextScroll(oled, rotary, button, [
                            "You have been relieved of duty, because you are dead.",
                            "The ship has no energy left to run the drives, shield, or life support.",
                            ]).display()
                        self.game_on = False

                    self.universe_counts = self.universe.countSpace()
                    ## check for klingon eradication
                    if self.universe_counts[Static.KLINGON] == 0:
                        TextScroll(oled, rotary, button, [
                            "Congratulations, You have successfuly exterminated a proud race and made the known"
                                " universe safe again.",
                            ]).display()
                        self.game_on = False                       

                
                TextScroll(oled, rotary, button, [
                    "Game Over.",
                    ]).display()
                    
g = Game().run()
