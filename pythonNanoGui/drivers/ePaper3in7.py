# ePaper3in7.py nanogui driver for Pico-ePpaper-3.7
# Tested with RPi Pico
# EPD is subclassed from framebuf.FrameBuffer for use with Writer class and nanogui.
# Optimisations to reduce allocations and RAM use.

# Released under the MIT license see LICENSE
# Thanks to @Peter for a great micropython-nano-gui: https://github.com/peterhinch/micropython-nano-gui

# -----------------------------------------------------------------------------
# * | File        :	  ePaper3in7.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | This version:   V1.0
# * | Date        :   2022-10-08
# -----------------------------------------------------------------------------

import framebuf
import uasyncio as asyncio
from time import sleep_ms, ticks_ms, ticks_us, ticks_diff

EPD_3IN7_lut_1Gray_GC =b"\
\x2A\x05\x00\x00\x00\x00\x00\x00\x00\x00\
\x05\x2A\x00\x00\x00\x00\x00\x00\x00\x00\
\x2A\x15\x00\x00\x00\x00\x00\x00\x00\x00\
\x05\x0A\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x02\x03\x0A\x00\x02\x06\x0A\x05\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\
\x22\x22\x22\x22\x22"


class EPD(framebuf.FrameBuffer):
    # A monochrome approach should be used for coding this. The rgb method ensures
    # nothing breaks if users specify colors.
    @staticmethod
    def rgb(r, g, b):
        return int((r > 127) or (g > 127) or (b > 127))

    def __init__(self, spi, cs, dc, rst, busy, landscape=False, asyn=False):
        self._spi = spi
        self._cs = cs  # Pins
        self._dc = dc
        self._rst = rst
        self._busy = busy
        self._lsc = landscape
        self._asyn = asyn
        self._as_busy = False  # Set immediately on start of task. Cleared when busy pin is logically false (physically 1).
        self._updated = asyncio.Event()
        # Public bound variables required by nanogui.
        self.width = 480 if landscape else 280  
        self.height = 280 if landscape else 480
        self.demo_mode = False  # Special mode enables demos to run
        self._buffer = bytearray(self.height * self.width // 8)
        self._mvb = memoryview(self._buffer)
        mode = framebuf.MONO_VLSB if landscape else framebuf.MONO_HLSB
        super().__init__(self._buffer, self.width, self.height, mode)
        self.init()

    def _command(self, command, data=None):
        self._dc(0)
        self._cs(0)
        self._spi.write(command)
        self._cs(1)
        if data is not None:
            self._data(data)

    def _data(self, data, buf1=bytearray(1)):
        self._dc(1)
        for b in data:
            self._cs(0)
            buf1[0] = b
            self._spi.write(buf1)
            self._cs(1)

    def init(self):
        # Hardware reset
        self._rst(1)
        sleep_ms(20)
        self._rst(0)
        sleep_ms(5)
        self._rst(1)
        sleep_ms(20)
        # Initialisation

        self._command(b'\x12')
        sleep_ms(300)  
        
        self._command(b'\x46')
        self._data(b'\xF7')
        self.wait_until_ready()
        self._command(b'\x47')
        self._data(b'\xF7')
        self.wait_until_ready()

        self._command(b'\x01')   # setting gaet number
        self._data(b'\xDF')
        self._data(b'\x01')
        self._data(b'\x00')

        self._command(b'\x03')   # set gate voltage
        self._data(b'\x00')

        self._command(b'\x04')   # set source voltage
        self._data(b'\x41')
        self._data(b'\xA8')
        self._data(b'\x32')

        self._command(b'\x11')   # set data entry sequence
        self._data(b'\x03')

        self._command(b'\x3C')   # set border 
        self._data(b'\x03')

        self._command(b'\x0C')   # set booster strength
        self._data(b'\xAE')
        self._data(b'\xC7')
        self._data(b'\xC3')
        self._data(b'\xC0')
        self._data(b'\xC0')

        self._command(b'\x18')   # set internal sensor on
        self._data(b'\x80')
         
        self._command(b'\x2C')   # set vcom value
        self._data(b'\x44')

        self._command(b'\x37')   # set display option, these setting turn on previous function
        self._data(b'\x00')      # can switch 1 gray or 4 gray
        self._data(b'\xFF')
        self._data(b'\xFF')
        self._data(b'\xFF')
        self._data(b'\xFF')  
        self._data(b'\x4F')
        self._data(b'\xFF')
        self._data(b'\xFF')
        self._data(b'\xFF')
        self._data(b'\xFF')  

        self._command(b'\x44')   # setting X direction start/end position of RAM
        self._data(b'\x00')
        self._data(b'\x00')
        self._data(b'\x17')
        self._data(b'\x01')

        self._command(b'\x45')   # setting Y direction start/end position of RAM
        self._data(b'\x00')
        self._data(b'\x00')
        self._data(b'\xDF')
        self._data(b'\x01')

        self._command(b'\x22')   # Display Update Control 2
        self._data(b'\xCF')

        self._command(b'\x32')
        self._data(EPD_3IN7_lut_1Gray_GC)

        print('Init Done.')

    def wait_until_ready(self):
        sleep_ms(50)
        t = ticks_ms()
        while not self.ready():  
            sleep_ms(100)
        dt = ticks_diff(ticks_ms(), t)
        print('wait_until_ready {}ms {:5.1f}mins'.format(dt, dt/60_000))

    async def wait(self):
        await asyncio.sleep_ms(0)  # Ensure tasks run that might make it unready
        while not self.ready():
            await asyncio.sleep_ms(100)

    # Pause until framebuf has been copied to device.
    async def updated(self):
        await self._updated.wait()

    # For polling in asynchronous code. Just checks pin state.
    # 1 == busy.
    def ready(self):
        return not(self._as_busy or (self._busy() == 1))  # 1 == busy

    async def _as_show(self, buf1=bytearray(1)):
        mvb = self._mvb
        send = self._spi.write
        cmd = self._command

        cmd(b'\x24')

        self._dc(1)
        # Necessary to deassert CS after each byte otherwise display does not
        # clear down correctly
        t = ticks_ms()
        if self._lsc:  # Landscape mode
            wid = self.width
            tbc = self.height // 8  # Vertical bytes per column
            iidx = wid * (tbc - 1)  # Initial index
            idx = iidx  # Index into framebuf
            vbc = 0  # Current vertical byte count
            hpc = 0  # Horizontal pixel count
            for i in range(len(mvb)):
                self._cs(0)
                buf1[0] = ~mvb[idx]  # INVERSION HACK ~data
                send(buf1)
                self._cs(1)
                idx -= self.width
                vbc += 1
                vbc %= tbc
                if not vbc:
                    hpc += 1
                    idx = iidx + hpc
                if not(i & 0x1f) and (ticks_diff(ticks_ms(), t) > 20):
                    await asyncio.sleep_ms(0)
                    t = ticks_ms()
        else:
            for i, b in enumerate(mvb):
                self._cs(0)
                buf1[0] = ~b  # INVERSION HACK ~data
                send(buf1)
                self._cs(1)
                if not(i & 0x1f) and (ticks_diff(ticks_ms(), t) > 20):
                    await asyncio.sleep_ms(0)
                    t = ticks_ms()

        self._updated.set()  # framebuf has now been copied to the device
        self._updated.clear()

        print('async full refresh')
        cmd(b'\x20')  # DISPLAY_REFRESH

        await asyncio.sleep(1)
        while self._busy() == 1:
            await asyncio.sleep_ms(200)  # Don't release lock until update is complete
        self._as_busy = False

    # draw the current frame memory. Blocking time ~180ms
    def show(self, buf1=bytearray(1)):
        if self._asyn:
            if self._as_busy:
                raise RuntimeError('Cannot refresh: display is busy.')
            self._as_busy = True
            asyncio.create_task(self._as_show())
            return
        t = ticks_us()
        mvb = self._mvb
        send = self._spi.write
        cmd = self._command

        cmd(b'\x24')

        self._dc(1)
        # Necessary to deassert CS after each byte otherwise display does not
        # clear down correctly
        if self._lsc:  # Landscape mode
            wid = self.width
            tbc = self.height // 8  # Vertical bytes per column
            iidx = wid * (tbc - 1)  # Initial index
            idx = iidx  # Index into framebuf
            vbc = 0  # Current vertical byte count
            hpc = 0  # Horizontal pixel count
            for _ in range(len(mvb)):
                self._cs(0)
                buf1[0] = ~mvb[idx]  # INVERSION HACK ~data
                send(buf1)
                self._cs(1)
                idx -= self.width
                vbc += 1
                vbc %= tbc
                if not vbc:
                    hpc += 1
                    idx = iidx + hpc
        else:
            for b in mvb:
                self._cs(0)
                buf1[0] = ~b  # INVERSION HACK ~data
                send(buf1)
                self._cs(1)

        print('sync full refresh')
        cmd(b'\x20')  # DISPLAY_REFRESH

        te = ticks_us()
        print('show time', ticks_diff(te, t)//1000, 'ms')
        if not self.demo_mode:
            # Immediate return to avoid blocking the whole application.
            # User should wait for ready before calling refresh()
            return
        self.wait_until_ready()
        sleep_ms(2000)  # Give time for user to see result
        

    # to wake call init()
    def sleep(self):
        self._as_busy = False
        self.wait_until_ready()
        self._command(b'\x10')
        self._data(b'\x03')
        self._rst(0)  # According to schematic this turns off the power


