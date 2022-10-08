# Released under the MIT license see LICENSE
# Thanks to @Peter for a great micropython-nano-gui: https://github.com/peterhinch/micropython-nano-gui

# Demo of initialisation procedure designed to minimise risk of memory fail
# when instantiating the frame buffer. The aim is to do this as early as
# possible before importing other modules.

# -----------------------------------------------------------------------------
# * | File        :	  color_setup.py
# * | Function    :   configuration file
# * | This version:   V1.1
# * | Date        :   2022-09-22
# -----------------------------------------------------------------------------

import machine
import gc

# from drivers.ePaper2in13V4 import EPD as SSD
# from drivers.ePaper2in13bV4 import EPD as SSD
# from drivers.ePaper2in7 import EPD as SSD
# from drivers.ePaper2in9 import EPD as SSD
# from drivers.ePaper3in7 import EPD as SSD
# from drivers.ePaper7in5b import EPD as SSD

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

prst = machine.Pin(RST_PIN, machine.Pin.OUT)
pbusy = machine.Pin(BUSY_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
pcs = machine.Pin(CS_PIN, machine.Pin.OUT)
spi = machine.SPI(1, baudrate=4_000_000)
pdc = machine.Pin(DC_PIN, machine.Pin.OUT)
gc.collect()  # Precaution before instantiating framebuf
ssd = SSD(spi, pcs, pdc, prst, pbusy, landscape=True, asyn=False)  # Create a display instance
ssd.demo_mode = True
