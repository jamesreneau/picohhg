Please see the site http://www.picohhg.com for more information and building instructions.

Install Ampy:

pip install adafruit-ampy

Find out which serial port the Pico is attached (WINDOWS):

mode

Unzip the zip into a folder. You will find several “py” files. They are all required for the PicoHHG to play multiple games and have a boot menu. Your COM port may be different.

ampy -p COM5 put button.py
ampy -p COM5 put buttonConfigure.py
ampy -p COM5 put choosers.py
ampy -p COM5 put clockywoky.py
ampy -p COM5 put main.py
ampy -p COM5 put pong04.py
ampy -p COM5 put rotary.PY
ampy -p COM5 put rotaryIRQ.py
ampy -p COM5 put ssd1306.py
ampy -p COM5 put sst02.py

Disconnect your PicoHHG and turn it on. You should see the menu and be able to scroll and click. If you are unable to click your rotary button may require configuration. Follow the on screen instructions.

ampy -p COM5 run buttonConfigure.py

Restart your PicoHHG and the button should work.

Modules used by all games (These are included in the Zip Archive)
rotary.py and rotaryIRQ.py are from https://github.com/MikeTeachman/micropython-rotary
The OLED driver comes from GitHub – stlehmann/micropython-ssd1306: A fork of the driver for SSD1306 displays to make it installable via upip

