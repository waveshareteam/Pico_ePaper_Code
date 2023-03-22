# *****************************************************************************
# * | File        :	  Pico_ePaper-2.13-C.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2021-03-16
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from machine import Pin, SPI
import framebuf
import utime


EPD_WIDTH       = 104
EPD_HEIGHT      = 212

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

class EPD_2in13_C:
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        
        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)
        
        
        self.buffer_black = bytearray(self.height * self.width // 8)
        self.buffer_yellow = bytearray(self.height * self.width // 8)
        self.imageblack = framebuf.FrameBuffer(self.buffer_black, self.width, self.height, framebuf.MONO_HLSB)
        self.imageyellow = framebuf.FrameBuffer(self.buffer_yellow, self.width, self.height, framebuf.MONO_HLSB)
        self.init()

    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def module_exit(self):
        self.digital_write(self.reset_pin, 0)

    # Hardware reset
    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(5)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)


    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)
        
    def send_data1(self, buf):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buf))
        self.digital_write(self.cs_pin, 1)
        
    def ReadBusy(self):
        print('busy')
        while(self.digital_read(self.busy_pin) == 0): 
            self.delay_ms(10) 
        print('busy release')
        
    def TurnOnDisplay(self):
        self.send_command(0x12)
        self.ReadBusy()

    def init(self):
        print('init')
        self.reset()

        self.send_command(0x06) # BOOSTER_SOFT_START
        self.send_data(0x17)
        self.send_data(0x17)
        self.send_data(0x17)
        
        self.send_command(0x04) # POWER_ON
        self.ReadBusy()
        
        self.send_command(0x00) # PANEL_SETTING
        self.send_data(0x8F)
        
        self.send_command(0x50) # VCOM_AND_DATA_INTERVAL_SETTING
        self.send_data(0xF0)
        
        self.send_command(0x61) # RESOLUTION_SETTING
        self.send_data(self.width & 0xff)
        self.send_data(self.height >> 8)
        self.send_data(self.height & 0xff)
        return 0       
        
    def display(self):
        self.send_command(0x10)
        self.send_data1(self.buffer_black)   
        self.send_command(0x13)
        self.send_data1(self.buffer_yellow)   

        self.TurnOnDisplay()

    
    def Clear(self, colorblack, colorred):
        self.send_command(0x10)
        self.send_data1([colorred] * self.height * int(self.width / 8))
        
        self.send_command(0x13)
        self.send_data1([colorred] * self.height * int(self.width / 8))
                                
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0x02) # POWER_OFF
        self.ReadBusy()
        self.send_command(0x07) # DEEP_SLEEP
        self.send_data(0xA5) # check code
        
        self.delay_ms(2000)
        self.module_exit()
        
        
if __name__=='__main__':
    epd = EPD_2in13_C()
    epd.Clear(0xff, 0xff)
    
    epd.imageblack.fill(0xff)
    epd.imageyellow.fill(0xff)
    epd.imageblack.text("Waveshare", 0, 10, 0x00)
    epd.imageyellow.text("ePaper-2.13", 0, 25, 0x00)
    epd.imageblack.text("RPi Pico", 0, 40, 0x00)
    epd.imageyellow.text("Hello World", 0, 55, 0x00)
    epd.display()
    epd.delay_ms(2000)
    
    epd.imageyellow.vline(10, 90, 40, 0x00)
    epd.imageyellow.vline(90, 90, 40, 0x00)
    epd.imageblack.hline(10, 90, 80, 0x00)
    epd.imageblack.hline(10, 130, 80, 0x00)
    epd.imageyellow.line(10, 90, 90, 130, 0x00)
    epd.imageblack.line(90, 90, 10, 130, 0x00)
    epd.display()
    epd.delay_ms(2000)
    
    epd.imageblack.rect(10, 150, 40, 40, 0x00)
    epd.imageyellow.fill_rect(60, 150, 40, 40, 0x00)
    epd.display()
    epd.delay_ms(2000)
        
    epd.Clear(0xff, 0xff)
    epd.delay_ms(2000)
    print("sleep")
    epd.sleep()