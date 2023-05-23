# PicoHHG- Handheld Game for the Pico

The PicoHHG is an easy to build handheld game platform to explore the power of the RaspberryPI Pico microcintroller.

Please see the site [http://www.picohhg.com](http://www.picohhg.com) for more information and building instructions.

## Installing code onto the PicoHHG hardware

This tutorial uses the ```ampy``` utility from Adafruit.  There are other utilities and environments to upload and develop Python for the Micropython environment.

###  Install Ampy:

```
pip install adafruit-ampy
```

### Get your serial port:

Find out which serial port the Pico is attached (WINDOWS):

```
mode
```


### Install the base files and the games you want:

Please observe that your COM port may be different.

```
ampy -p COM5 put button.py
ampy -p COM5 put buttonConfigure.py
ampy -p COM5 put choosers.py
ampy -p COM5 put main.py
ampy -p COM5 put rotary.PY
ampy -p COM5 put rotaryIRQ.py
ampy -p COM5 put ssd1306.py
ampy -p COM5 put symbols.py
```

```
ampy -p COM5 put clockywoky.py
ampy -p COM5 put jacksorbetter.py
ampy -p COM5 put onehandedsolitare.py
ampy -p COM5 put pong.py
ampy -p COM5 put sst.py
```

Disconnect your PicoHHG and turn it on. You should see the menu and be able to scroll and click. If you are unable to click your rotary button may require configuration. Follow the on screen instructions.

```
ampy -p COM5 run buttonConfigure.py
```

Restart your PicoHHG and the button should work.

## Credits:
* rotary.py and rotaryIRQ.py - https://github.com/MikeTeachman/micropython-rotary
* ssd1306.py - https://github.com/stlehmann/micropython-ssd1306

