# ePaper2in9.py nanogui driver for Pico-ePpaper-2.9
# Tested with RPi Pico
# EPD is subclassed from framebuf.FrameBuffer for use with Writer class and nanogui.
# Optimisations to reduce allocations and RAM use.

# Released under the MIT license see LICENSE
# Thanks to @Peter for a great micropython-nano-gui: https://github.com/peterhinch/micropython-nano-gui

# -----------------------------------------------------------------------------
# * | File        :	  ePaper2in9.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | This version:   V1.0
# * | Date        :   2022-09-08
# -----------------------------------------------------------------------------

import framebuf
import uasyncio as asyncio
from time import sleep_ms, ticks_ms, ticks_us, ticks_diff


class EPD(framebuf.FrameBuffer):
    # A monochrome approach should be used for coding this. The rgb method ensures
    # nothing breaks if users specify colors.
    @staticmethod
    def rgb(r, g, b):
        return int((r > 127) or (g > 127) or (b > 127))

    def __init__(self, spi, cs, dc, rst, busy, landscape=False, asyn=False, full=True):
        self._spi = spi
        self._cs = cs  # Pins
        self._dc = dc
        self._rst = rst
        self._busy = busy
        self._lsc = landscape
        self._asyn = asyn
        self._full = full
        self._as_busy = False  # Set immediately on start of task. Cleared when busy pin is logically false (physically 1).
        self._updated = asyncio.Event()
        # Dimensions in pixels. Waveshare code is portrait mode.
        # Public bound variables required by nanogui.
        self.width = 296 if landscape else 128  
        self.height = 128 if landscape else 296
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
        sleep_ms(200)
        self._rst(0)
        sleep_ms(20)  # 5ms in Waveshare code
        self._rst(1)
        sleep_ms(200)
        # Initialisation
        cmd = self._command
        self.wait_until_ready() 
        cmd(b'\x12')
        self.wait_until_ready() #SWRESET     
        cmd(b'\x01', b'\x27\x01\x00') # Driver output control
        cmd(b'\x11', b'\x03')
        cmd(b'\x21', b'\x00\x80')

        cmd(b'\x44', b'\x00\x0F')
        cmd(b'\x45', b'\x00\x00\x27\x01')
        cmd(b'\x4E', b'\x00')
        cmd(b'\x4F', b'\x00\x00')
        self.wait_until_ready()

        print('Init Done.')

    def init_partial(self):
        # Hardware reset
        self._rst(0)
        sleep_ms(2)
        self._rst(1)
        sleep_ms(2)
        # Initialisation
        cmd = self._command
        lut_wf_2in9 =\
            b'\x00\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
            b'\x80\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
            b'\x40\x40\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
            b'\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'\
            b'\x0A\x00\x00\x00\x00\x00\x01'\
            b'\x01\x00\x00\x00\x00\x00\x00'\
            b'\x01\x00\x00\x00\x00\x00\x00'\
            b'\x00\x00\x00\x00\x00\x00\x00'\
            b'\x00\x00\x00\x00\x00\x00\x00'\
            b'\x00\x00\x00\x00\x00\x00\x00'\
            b'\x00\x00\x00\x00\x00\x00\x00'\
            b'\x00\x00\x00\x00\x00\x00\x00'\
            b'\x00\x00\x00\x00\x00\x00\x00'\
            b'\x00\x00\x00\x00\x00\x00\x00'\
            b'\x00\x00\x00\x00\x00\x00\x00'\
            b'\x00\x00\x00\x00\x00\x00\x00'\
            b'\x22\x22\x22\x22\x22\x22\x00\x00\x00'\
            b'\x22\x17\x41\xB0\x32\x36'

        cmd(b'\x32', lut_wf_2in9)
        cmd(b'\x37', b'\x00\x00\x00\x00\x00\x40\x00\x00\x00\x00')
        cmd(b'\x3c', b'\x80')
        cmd(b'\x22', b'\xc0')
        cmd(b'\x20')

        self.wait_until_ready()

        cmd(b'\x44', b'\x00\x0F')
        cmd(b'\x45', b'\x00\x00\x27\x01')
        cmd(b'\x4E', b'\x00')
        cmd(b'\x4F', b'\x00\x00')


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

        cmd(b'\x24')  # DATA_START_TRANSMISSION_2 not in datasheet

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
        if self._full:
            print('async full refresh')
            cmd(b'\x22', b'\xF7')
            cmd(b'\x20')  # DISPLAY_REFRESH
        else:
            print('async partial refresh')
            cmd(b'\x22', b'\x0F')
            cmd(b'\x20')  # DISPLAY_REFRESH
        await asyncio.sleep(1)
        while self._busy() == 1:
            await asyncio.sleep_ms(200)  # Don't release lock until update is complete
        self._as_busy = False

    # draw the current frame memory. Blocking time ~180ms
    def show(self, buf1=bytearray(1)):
        
        if not self._full:
            self.init_partial()
        
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

        cmd(b'\x24')  # DATA_START_TRANSMISSION_2 not in datasheet

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

        if self._full:
            print('sync full refresh')
            cmd(b'\x22', b'\xF7')
            cmd(b'\x20')  # DISPLAY_REFRESH
        else:
            print('sync partial refresh')
            cmd(b'\x22', b'\x0F')
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
        cmd = self._command
        cmd(b'\x10', b'\x01')  # DEEP_SLEEP
        self._rst(0)  # According to schematic this turns off the power


