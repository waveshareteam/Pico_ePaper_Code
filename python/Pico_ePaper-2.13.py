# *****************************************************************************
# * | File        :	  Pico_ePaper-2.13.py
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

lut_full_update= [
    0x80,0x60,0x40,0x00,0x00,0x00,0x00,             #LUT0: BB:     VS 0 ~7
    0x10,0x60,0x20,0x00,0x00,0x00,0x00,             #LUT1: BW:     VS 0 ~7
    0x80,0x60,0x40,0x00,0x00,0x00,0x00,             #LUT2: WB:     VS 0 ~7
    0x10,0x60,0x20,0x00,0x00,0x00,0x00,             #LUT3: WW:     VS 0 ~7
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,             #LUT4: VCOM:   VS 0 ~7

    0x03,0x03,0x00,0x00,0x02,                       # TP0 A~D RP0
    0x09,0x09,0x00,0x00,0x02,                       # TP1 A~D RP1
    0x03,0x03,0x00,0x00,0x02,                       # TP2 A~D RP2
    0x00,0x00,0x00,0x00,0x00,                       # TP3 A~D RP3
    0x00,0x00,0x00,0x00,0x00,                       # TP4 A~D RP4
    0x00,0x00,0x00,0x00,0x00,                       # TP5 A~D RP5
    0x00,0x00,0x00,0x00,0x00,                       # TP6 A~D RP6

    0x15,0x41,0xA8,0x32,0x30,0x0A,
]

lut_partial_update = [ #20 bytes
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,             #LUT0: BB:     VS 0 ~7
    0x80,0x00,0x00,0x00,0x00,0x00,0x00,             #LUT1: BW:     VS 0 ~7
    0x40,0x00,0x00,0x00,0x00,0x00,0x00,             #LUT2: WB:     VS 0 ~7
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,             #LUT3: WW:     VS 0 ~7
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,             #LUT4: VCOM:   VS 0 ~7

    0x0A,0x00,0x00,0x00,0x00,                       # TP0 A~D RP0
    0x00,0x00,0x00,0x00,0x00,                       # TP1 A~D RP1
    0x00,0x00,0x00,0x00,0x00,                       # TP2 A~D RP2
    0x00,0x00,0x00,0x00,0x00,                       # TP3 A~D RP3
    0x00,0x00,0x00,0x00,0x00,                       # TP4 A~D RP4
    0x00,0x00,0x00,0x00,0x00,                       # TP5 A~D RP5
    0x00,0x00,0x00,0x00,0x00,                       # TP6 A~D RP6

    0x15,0x41,0xA8,0x32,0x30,0x0A,
]

EPD_WIDTH       = 128 # 122
EPD_HEIGHT      = 250

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

FULL_UPDATE = 0
PART_UPDATE = 1

class EPD_2in13(framebuf.FrameBuffer):
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        
        self.full_lut = lut_full_update
        self.partial_lut = lut_partial_update
        
        self.full_update = FULL_UPDATE
        self.part_update = PART_UPDATE
        
        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)
        
        
        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HLSB)
        self.init(FULL_UPDATE)

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
        
    def ReadBusy(self):
        print('busy')
        while(self.digital_read(self.busy_pin) == 1):      # 0: idle, 1: busy
            self.delay_ms(10)    
        print('busy release')
        
    def TurnOnDisplay(self):
        self.send_command(0x22)
        self.send_data(0xC7)
        self.send_command(0x20)        
        self.ReadBusy()

    def TurnOnDisplayPart(self):
        self.send_command(0x22)
        self.send_data(0x0c)
        self.send_command(0x20)        
        self.ReadBusy()

    def init(self, update):
        print('init')
        self.reset()
        if(update == self.full_update):
            self.ReadBusy()
            self.send_command(0x12) # soft reset
            self.ReadBusy()

            self.send_command(0x74) #set analog block control
            self.send_data(0x54)
            self.send_command(0x7E) #set digital block control
            self.send_data(0x3B)

            self.send_command(0x01) #Driver output control
            self.send_data(0x27)
            self.send_data(0x01)
            self.send_data(0x01)
            
            self.send_command(0x11) #data entry mode
            self.send_data(0x01)

            self.send_command(0x44) #set Ram-X address start/end position
            self.send_data(0x00)
            self.send_data(0x0F)    #0x0C-->(15+1)*8=128

            self.send_command(0x45) #set Ram-Y address start/end position
            self.send_data(0x27)   #0xF9-->(249+1)=250
            self.send_data(0x01)
            self.send_data(0x2e)
            self.send_data(0x00)
            
            self.send_command(0x3C) #BorderWavefrom
            self.send_data(0x03)

            self.send_command(0x2C)     #VCOM Voltage
            self.send_data(0x55)    #

            self.send_command(0x03)
            self.send_data(self.full_lut[70])

            self.send_command(0x04) #
            self.send_data(self.full_lut[71])
            self.send_data(self.full_lut[72])
            self.send_data(self.full_lut[73])

            self.send_command(0x3A)     #Dummy Line
            self.send_data(self.full_lut[74])
            self.send_command(0x3B)     #Gate time
            self.send_data(self.full_lut[75])

            self.send_command(0x32)
            for count in range(70):
                self.send_data(self.full_lut[count])

            self.send_command(0x4E)   # set RAM x address count to 0
            self.send_data(0x00)
            self.send_command(0x4F)   # set RAM y address count to 0X127
            self.send_data(0x0)
            self.send_data(0x00)
            self.ReadBusy()
        else:
            self.send_command(0x2C)     #VCOM Voltage
            self.send_data(0x26)

            self.ReadBusy()

            self.send_command(0x32)
            for count in range(70):
                self.send_data(self.partial_lut[count])

            self.send_command(0x37)
            self.send_data(0x00)
            self.send_data(0x00)
            self.send_data(0x00)
            self.send_data(0x00)
            self.send_data(0x40)
            self.send_data(0x00)
            self.send_data(0x00)

            self.send_command(0x22)
            self.send_data(0xC0)
            self.send_command(0x20)
            self.ReadBusy()

            self.send_command(0x3C) #BorderWavefrom
            self.send_data(0x01)
        return 0       
        
    def display(self, image):
        self.send_command(0x24)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(image[i + j * int(self.width / 8)])   
        self.TurnOnDisplay()
        
    def displayPartial(self, image):
        self.send_command(0x24)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(image[i + j * int(self.width / 8)])   
                
        self.send_command(0x26)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(~image[i + j * int(self.width / 8)])  
        self.TurnOnDisplayPart()

    def displayPartBaseImage(self, image):
        self.send_command(0x24)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(image[i + j * int(self.width / 8)])   
                
        self.send_command(0x26)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(image[i + j * int(self.width / 8)])  
        self.TurnOnDisplay()
    
    def Clear(self, color):
        self.send_command(0x24)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(color)
        self.send_command(0x26)
        for j in range(0, self.height):
            for i in range(0, int(self.width / 8)):
                self.send_data(color)
                                
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0x10) #enter deep sleep
        self.send_data(0x03)
        self.delay_ms(2000)
        self.module_exit()
        
        
if __name__=='__main__':
    epd = EPD_2in13()
    epd.Clear(0xff)
    
    epd.fill(0xff)
    epd.text("Waveshare", 0, 10, 0x00)
    epd.text("ePaper-2.13", 0, 30, 0x00)
    epd.text("Raspberry Pico", 0, 50, 0x00)
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
    
    epd.rect(10, 180, 50, 40, 0x00)
    epd.fill_rect(60, 180, 50, 40, 0x00)
    epd.displayPartBaseImage(epd.buffer)
    epd.delay_ms(2000)
    
    epd.init(epd.part_update)
    for i in range(0, 10):
        epd.fill_rect(40, 230, 40, 10, 0xff)
        epd.text(str(i), 60, 230, 0x00)
        epd.displayPartial(epd.buffer)
        
    epd.init(epd.full_update)
    epd.Clear(0xff)
    epd.delay_ms(2000)
    epd.sleep()