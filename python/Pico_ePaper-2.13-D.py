# *****************************************************************************
# * | File        :	  Pico_ePaper-2.13-D.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2021-05-14
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

EPD_2IN13D_lut_vcomDC =[
    0x00, 0x08, 0x00, 0x00, 0x00, 0x02,
    0x60, 0x28, 0x28, 0x00, 0x00, 0x01,
    0x00, 0x14, 0x00, 0x00, 0x00, 0x01,
    0x00, 0x12, 0x12, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00,
]
EPD_2IN13D_lut_ww =[
    0x40, 0x08, 0x00, 0x00, 0x00, 0x02,
    0x90, 0x28, 0x28, 0x00, 0x00, 0x01,
    0x40, 0x14, 0x00, 0x00, 0x00, 0x01,
    0xA0, 0x12, 0x12, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]
EPD_2IN13D_lut_bw =[
    0x40, 0x17, 0x00, 0x00, 0x00, 0x02,
    0x90, 0x0F, 0x0F, 0x00, 0x00, 0x03,
    0x40, 0x0A, 0x01, 0x00, 0x00, 0x01,
    0xA0, 0x0E, 0x0E, 0x00, 0x00, 0x02,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]
EPD_2IN13D_lut_wb =[
    0x80, 0x08, 0x00, 0x00, 0x00, 0x02,
    0x90, 0x28, 0x28, 0x00, 0x00, 0x01,
    0x80, 0x14, 0x00, 0x00, 0x00, 0x01,
    0x50, 0x12, 0x12, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]
EPD_2IN13D_lut_bb =[
    0x80, 0x08, 0x00, 0x00, 0x00, 0x02,
    0x90, 0x28, 0x28, 0x00, 0x00, 0x01,
    0x80, 0x14, 0x00, 0x00, 0x00, 0x01,
    0x50, 0x12, 0x12, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]


'''
 # partial screen update LUT
'''
EPD_2IN13D_lut_vcom1 =[
    0x00, 0x19, 0x01, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ,0x00, 0x00,
]
EPD_2IN13D_lut_ww1 =[
    0x00, 0x19, 0x01, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]
EPD_2IN13D_lut_bw1 =[
    0x80, 0x19, 0x01, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]
EPD_2IN13D_lut_wb1 =[
    0x40, 0x19, 0x01, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]
EPD_2IN13D_lut_bb1 =[
    0x00, 0x19, 0x01, 0x00, 0x00, 0x01,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]

EPD_WIDTH       = 104 
EPD_HEIGHT      = 212

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

FULL_UPDATE = 0
PART_UPDATE = 1

class EPD_2in13_D(framebuf.FrameBuffer):
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        
        self.lut_vcomDC = EPD_2IN13D_lut_vcomDC
        self.lut_ww = EPD_2IN13D_lut_ww
        self.lut_bw = EPD_2IN13D_lut_bw
        self.lut_wb = EPD_2IN13D_lut_wb
        self.lut_bb = EPD_2IN13D_lut_bb
        
        self.lut_vcom1 = EPD_2IN13D_lut_vcom1
        self.lut_ww1 = EPD_2IN13D_lut_ww1
        self.lut_bw1 = EPD_2IN13D_lut_bw1
        self.lut_wb1 = EPD_2IN13D_lut_wb1
        self.lut_bb1 = EPD_2IN13D_lut_bb1
        
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
        utime.sleep_ms(delaytime)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def module_exit(self):
        self.digital_write(self.reset_pin, 0)

    # Hardware reset
    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(200)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(200)   


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
        print('e-Paper busy')
        busy = 1
        self.send_command(0x71)
        while(self.digital_read(self.busy_pin) == 0): 
            self.send_command(0x71)
        self.delay_ms(200)    
        print('e-Paper busy release')
    
    def SetFullReg(self):
        self.send_command(0x50)
        self.send_data(0xB7)
        
        self.send_command(0x20)
        self.send_data1(self.lut_vcomDC[0:44])
            
        self.send_command(0x21)
        self.send_data1(self.lut_ww[0:42])
        
        self.send_command(0x22)
        self.send_data1(self.lut_bw[0:42])

        self.send_command(0x23)
        self.send_data1(self.lut_bb[0:42])
            
        self.send_command(0x24)
        self.send_data1(self.lut_wb[0:42])
          
    
    def SetPartReg(self):
        self.send_command(0x82)
        self.send_data(0x00)
        self.send_command(0x50)
        self.send_data(0xB7)
        
        self.send_command(0x20)
        self.send_data1(self.lut_vcom1[0:44])
            
        self.send_command(0x21)
        self.send_data1(self.lut_ww1[0:42])
            
        self.send_command(0x22)
        self.send_data1(self.lut_bw1[0:42])
            
        self.send_command(0x23)
        self.send_data1(self.lut_wb1[0:42])
            
        self.send_command(0x24)
        self.send_data1(self.lut_bb1[0:42])
    
    def TurnOnDisplay(self):
        self.send_command(0x12)
        self.delay_ms(100)       
        self.ReadBusy()


    def init(self):
        print('init')
        self.reset()

        self.send_command(0x01)
        self.send_data(0x03)
        self.send_data(0x00)
        self.send_data(0x2B)
        self.send_data(0x2B)
        self.send_data(0x03)
        
        
        self.send_command(0x06)
        self.send_data(0x17)
        self.send_data(0x17)
        self.send_data(0x17)

        self.send_command(0x04) 
        self.ReadBusy()
        
        self.send_command(0x00)
        self.send_data(0xBF)
        self.send_data(0x0E)
        
        self.send_command(0x30)
        self.send_data(0x3A)
        
        self.send_command(0x61)
        self.send_data(self.width)
        self.send_data((self.height&0x100)>>8)
        self.send_data(self.height&0xff)
        
        self.send_command(0x82)
        self.send_data(0x28)
        
        
    def display(self, image):
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1
        self.send_command(0x10)
        self.send_data1([0x00] * high * wide)
        
        self.send_command(0x13)
        self.send_data1(image)
            
        self.SetFullReg()
        self.TurnOnDisplay()
        
    def displayPartial(self, image):
        self.SetPartReg()
        self.send_command(0x91)
        self.send_command(0x90)
        self.send_data(0)
        self.send_data(self.width - 1)
        
        self.send_data(0)
        self.send_data(0)
        self.send_data(self.height//256)
        self.send_data(self.height%256 - 1)
        self.send_data(0X28)
        
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1
        self.send_command(0x10)
        for j in range(0, high):
            for i in range(0, wide):
                self.send_data(~image[i + j * wide])
        self.send_command(0x13)
        for j in range(0, high):
            for i in range(0, wide):
                self.send_data(image[i + j * wide])
        
        self.TurnOnDisplay()


    
    def Clear(self, color):
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1
        self.send_command(0x10)
        self.send_data1([color] * high * wide)
        
        self.send_command(0x13)
        self.send_data1([~color] * high * wide)
            
        self.SetFullReg()
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0x50)
        self.send_data(0xF7)
        self.send_command(0x02)
        self.send_command(0x07)
        self.send_data(0xA5)

        
        
if __name__=='__main__':
    epd = EPD_2in13_D()
    epd.Clear(0x00)
    
    epd.fill(0xff)
    epd.text("Waveshare", 0, 10, 0x00)
    epd.text("ePaper-2.13", 0, 30, 0x00)
    epd.text("RPi Pico", 0, 50, 0x00)
    epd.text("Hello World", 0, 70, 0x00)
    epd.display(epd.buffer)
    epd.delay_ms(2000)
    
    epd.vline(10, 90, 60, 0x00)
    epd.vline(90, 90, 60, 0x00)
    epd.hline(10, 90, 80, 0x00)
    epd.hline(10, 150, 80, 0x00)
    epd.line(10, 90, 90, 150, 0x00)
    epd.line(90, 90, 10, 150, 0x00)
    epd.display(epd.buffer)
    epd.delay_ms(2000)

    
    for i in range(0, 10):
        epd.fill_rect(40, 180, 40, 10, 0xff)
        epd.text(str(i), 50, 180, 0x00)
        epd.displayPartial(epd.buffer)

    epd.Clear(0x00)
    epd.delay_ms(2000)
    epd.sleep()