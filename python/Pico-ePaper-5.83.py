# *****************************************************************************
# * | File        :	  Pico_ePaper-5.83.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2021-05-27
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

# Display resolution
EPD_WIDTH       = 648
EPD_HEIGHT      = 480

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13


class EPD_5in83(framebuf.FrameBuffer):
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        
        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)
        
        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HLSB)
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
        self.delay_ms(2)
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
        
    def send_data1(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte(data)
        self.digital_write(self.cs_pin, 1)

    def ReadBusy(self):
        print("e-Paper busy")
        while(self.digital_read(self.busy_pin) == 0):      #  1: idle, 0: busy
            self.delay_ms(10)
        print("e-Paper busy release")  

    def TurnOnDisplay(self):
        self.send_command(0x12) 
        self.delay_ms(100)
        self.ReadBusy()
        
    def init(self):
        # EPD hardware init start     
        self.reset()
        
        self.send_command(0x01)    #POWER SETTING
        self.send_data (0x07)
        self.send_data (0x07)  #VGH=20V,VGL=-20V
        self.send_data (0x3f)  #VDH=15V
        self.send_data (0x3f)  #VDL=-15V

        self.send_command(0x04)    #POWER ON
        self.delay_ms(100) 
        self.ReadBusy()   #waiting for the electronic paper IC to release the idle signal

        self.send_command(0X00)    #PANNEL SETTING
        self.send_data(0x1F)   #KW-3f   KWR-2F	BWROTP 0f	BWOTP 1f

        self.send_command(0x61)    #tres
        self.send_data (0x02)		#source 648
        self.send_data (0x88)
        self.send_data (0x01)		#gate 480
        self.send_data (0xE0)

        self.send_command(0X15)		
        self.send_data(0x00)		

        self.send_command(0X50)			#VCOM AND DATA INTERVAL SETTING
        self.send_data(0x10)
        self.send_data(0x07)

        self.send_command(0X60)			#TCON SETTING
        self.send_data(0x22)
        # EPD hardware init end
        return 0

    def display(self, image):
        if (image == None):
            return         
        self.send_command(0x13) # WRITE_RAM
        self.send_data1(image)
        self.TurnOnDisplay()

    def Clear(self, color):
        self.send_command(0x13) # WRITE_RAM
        for i in range(0, int(self.width / 8)):
            self.send_data1([color] * self.height)
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0x02) # DEEP_SLEEP_MODE
        self.ReadBusy()
        self.send_command(0x07)
        self.send_data(0xa5)
        
        self.delay_ms(2000)
        self.module_exit()

if __name__=='__main__':
    epd = EPD_5in83()
    epd.Clear(0x00)
    
    epd.fill(0x00)
    epd.text("Waveshare", 5, 10, 0xff)
    epd.text("Pico_ePaper-5.83", 5, 40, 0xff)
    epd.text("Raspberry Pico", 5, 70, 0xff)
    epd.display(epd.buffer)
    epd.delay_ms(2000)
    
    epd.vline(10, 90, 60, 0xff)
    epd.vline(120, 90, 60, 0xff)
    epd.hline(10, 90, 110, 0xff)
    epd.hline(10, 150, 110, 0xff)
    epd.line(10, 90, 120, 150, 0xff)
    epd.line(120, 90, 10, 150, 0xff)
    epd.display(epd.buffer)
    epd.delay_ms(2000)
    
    epd.rect(10, 180, 50, 80, 0xff)
    epd.fill_rect(70, 180, 50, 80, 0xff)
    epd.display(epd.buffer)
    epd.delay_ms(2000)

    epd.fill_rect(200, 100, 400, 100, 0xff)
    epd.display(epd.buffer)
    epd.delay_ms(2000)

    epd.init()
    epd.Clear(0x00)
    epd.delay_ms(2000)
    print("sleep")
    epd.sleep()