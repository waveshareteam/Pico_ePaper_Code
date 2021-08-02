# *****************************************************************************
# * | File        :  Pico_ePaper-5.65.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2021-06-04
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
EPD_WIDTH       = 600
EPD_HEIGHT      = 448

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

class EPD_5in65(framebuf.FrameBuffer):
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        
        self.Black = 0x00
        self.White = 0x01
        self.Green = 0x02
        self.Blue = 0x03
        self.Red = 0x04
        self.Yellow = 0x05
        self.Orange = 0x06
        self.Clean = 0x07
        
        
        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)
        

        self.buffer = bytearray(self.height * self.width // 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.GS4_HMSB)
        
        self.EPD_5IN65F_Init()

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
        self.delay_ms(200) 
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(1)
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
        
    def BusyHigh(self):
        while(self.digital_read(self.busy_pin) == 0):
            self.delay_ms(1)
            
    def BusyLow(self):
        while(self.digital_read(self.busy_pin) == 1):
            self.delay_ms(1)
        
    def EPD_5IN65F_Init(self):
    
        self.reset();
        self.BusyHigh();
        self.send_command(0x00);
        self.send_data(0xEF);
        self.send_data(0x08);
        self.send_command(0x01);
        self.send_data(0x37);
        self.send_data(0x00);
        self.send_data(0x23);
        self.send_data(0x23);
        self.send_command(0x03);
        self.send_data(0x00);
        self.send_command(0x06);
        self.send_data(0xC7);
        self.send_data(0xC7);
        self.send_data(0x1D);
        self.send_command(0x30);
        self.send_data(0x3C);
        self.send_command(0x41);
        self.send_data(0x00);
        self.send_command(0x50);
        self.send_data(0x37);
        self.send_command(0x60);
        self.send_data(0x22);
        self.send_command(0x61);
        self.send_data(0x02);
        self.send_data(0x58);
        self.send_data(0x01);
        self.send_data(0xC0);
        self.send_command(0xE3);
        self.send_data(0xAA);
        
        self.delay_ms(100);
        self.send_command(0x50);
        self.send_data(0x37);

    def EPD_5IN65F_Clear(self,color):
    
        self.send_command(0x61)   # Set Resolution setting
        self.send_data(0x02)
        self.send_data(0x58)
        self.send_data(0x01)
        self.send_data(0xC0)
        self.send_command(0x10)
        for i in range(0,int(self.width / 2)):
            for j in range(0, self.height):
                self.send_data((color<<4)|color)

        self.send_command(0x04)   # 0x04
        self.BusyHigh()
        self.send_command(0x12)   # 0x12
        self.BusyHigh()
        self.send_command(0x02)   # 0x02
        self.BusyLow()
        self.delay_ms(500)
        
    def EPD_5IN65F_Display(self,image):

        self.send_command(0x61)   # Set Resolution setting
        self.send_data(0x02)
        self.send_data(0x58)
        self.send_data(0x01)
        self.send_data(0xC0)
        self.send_command(0x10)
        for i in range(0, self.height):
            for j in range(0, int(self.width // 2)):            
                self.send_data(image[j+(int(self.width // 2)*i)])
            
        self.send_command(0x04)   # 0x04
        self.BusyHigh()
        self.send_command(0x12)   # 0x12
        self.BusyHigh()
        self.send_command(0x02)   # 0x02
        self.BusyLow()
        self.delay_ms(200)
    
    def EPD_5IN65F_Display_part(self,image,xstart,ystart,image_width,image_heigh):

        self.send_command(0x61)   # Set Resolution setting
        self.send_data(0x02)
        self.send_data(0x58)
        self.send_data(0x01)
        self.send_data(0xC0)
        self.send_command(0x10)
        for i in range(0, self.height):
            for j in range(0, int(self.width / 2)):
                if((i<(image_heigh+ystart)) & (i>(ystart-1) ) & (j<(image_width+xstart)/2) & (j>(xstart/2 - 1))):
                    self.send_data(image[(j-xstart/2) + (image_width/2*(i-ystart))])
                else:
                    self.send_data(0x11)

        self.send_command(0x04)   # 0x04
        self.BusyHigh()
        self.send_command(0x12)   # 0x12
        self.BusyHigh()
        self.send_command(0x02)   # 0x02
        self.BusyLow()
        self.delay_ms(200)
        

                
    def Sleep(self):
        self.delay_ms(100);
        self.send_command(0x07);
        self.send_data(0xA5);
        self.delay_ms(100);
        self.digital_write(self.reset_pin, 1)
    
if __name__=='__main__':
    
    epd = EPD_5in65()
    
    epd.fill(0xff)
    
    epd.text("Waveshare", 5, 5, epd.Black)
    epd.text("Pico_ePaper-5.65", 5, 20, epd.Black)
    epd.text("Raspberry Pico", 5, 35, epd.Black)
#     epd.EPD_5IN65F_Display(epd.buffer)
#     epd.delay_ms(500)
    
    epd.vline(10, 60, 60, epd.Black)
    epd.vline(90, 60, 60, epd.Black)
    epd.hline(10, 60, 80, epd.Black)
    epd.hline(10, 120, 80, epd.Black)
    epd.line(10, 60, 90, 120, epd.Black)
    epd.line(90, 60, 10, 120, epd.Black)
#     epd.EPD_5IN65F_Display(epd.buffer)
#     epd.delay_ms(500)
    
    epd.rect(10, 136, 50, 80, epd.Black)
    epd.fill_rect(70, 136, 50, 80, epd.Black)
#     epd.EPD_5IN65F_Display(epd.buffer)
#     epd.delay_ms(500)
#    
    epd.text('Black',200,11,epd.Black)
    epd.fill_rect(300, 0, 300, 30, epd.Black)
    epd.text('White',200,41,epd.White)
    epd.fill_rect(300, 30, 300, 30, epd.White)
    epd.text('Green',200,71,epd.Green)
    epd.fill_rect(300, 60, 300, 30, epd.Green)
    epd.text('Blue',200,101,epd.Blue)
    epd.fill_rect(300, 90, 300, 30, epd.Blue)
    epd.text('Red',200,131,epd.Red)
    epd.fill_rect(300, 120, 300, 30, epd.Red)
    epd.text('Yellow',200,161,epd.Yellow)
    epd.fill_rect(300, 150, 300, 30, epd.Yellow)
    epd.text('Orange',200,191,epd.Orange)
    epd.fill_rect(300, 180, 300, 30, epd.Orange)
    epd.text('Clean',200,221,epd.Black)
    epd.fill_rect(300, 210, 300, 30, epd.Clean)
#     epd.EPD_5IN65F_Display(epd.buffer)
#     epd.delay_ms(500)

    j = 0
    for i in range(-250,600):
        epd.line(i, 238, i+250, 448, j)
        if (i%30==0) :
            j = j+1
            j = j%7
    epd.EPD_5IN65F_Display(epd.buffer)
    epd.delay_ms(500)



    epd.Sleep()



