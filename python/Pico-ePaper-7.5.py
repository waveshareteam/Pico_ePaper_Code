# *****************************************************************************
# * | File        :	  Pico_ePaper-7.5.py
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
EPD_WIDTH       = 800
EPD_HEIGHT      = 480

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

class EPD_7in5(framebuf.FrameBuffer):
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
        
    def send_data1(self, buf):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buf))
        self.digital_write(self.cs_pin, 1)

    def WaitUntilIdle(self):
        print("e-Paper busy")
        while(self.digital_read(self.busy_pin) == 0):    # Wait until the busy_pin goes LOW
            self.send_command(0x71)
            self.delay_ms(20)
        self.delay_ms(20) 
        print("e-Paper busy release")  

    def TurnOnDisplay(self):
        self.send_command(0x12) # DISPLAY REFRESH
        self.delay_ms(100)      #!!!The delay here is necessary, 200uS at least!!!
        self.WaitUntilIdle()
        
    def init(self):
        self.reset()
        
        self.send_command(0x06)     # btst
        self.send_data(0x17)
        self.send_data(0x17)
        self.send_data(0x28)        # If an exception is displayed, try using 0x38
        self.send_data(0x17)
        
        self.send_command(0x01)			#POWER SETTING
        self.send_data(0x07)
        self.send_data(0x07)    #VGH=20V,VGL=-20V
        self.send_data(0x28)		#VDH=15V
        self.send_data(0x17)		#VDL=-15V

        self.send_command(0x04) #POWER ON
        self.delay_ms(100)
        self.WaitUntilIdle()

        self.send_command(0X00)			#PANNEL SETTING
        self.send_data(0x1F)   #KW-3f   KWR-2F	BWROTP 0f	BWOTP 1f

        self.send_command(0x61)        	#tres
        self.send_data(0x03)		#source 800
        self.send_data(0x20)
        self.send_data(0x01)		#gate 480
        self.send_data(0xE0)

        self.send_command(0X15)
        self.send_data(0x00)

        self.send_command(0X50)			#VCOM AND DATA INTERVAL SETTING
        self.send_data(0x10)
        self.send_data(0x07)

        self.send_command(0X60)			#TCON SETTING
        self.send_data(0x22)

        # EPD hardware init end
        return 0
    
    def init_fast(self):
        self.reset()
        
        self.send_command(0X00)			#PANNEL SETTING
        self.send_data(0x1F)   #KW-3f   KWR-2F	BWROTP 0f	BWOTP 1f

        self.send_command(0X50)			#VCOM AND DATA INTERVAL SETTING
        self.send_data(0x10)
        self.send_data(0x07)

        self.send_command(0x04) #POWER ON
        self.delay_ms(100) 
        self.WaitUntilIdle()        #waiting for the electronic paper IC to release the idle signal

        #Enhanced display drive(Add 0x06 command)
        self.send_command(0x06)			#Booster Soft Start 
        self.send_data (0x27)
        self.send_data (0x27)   
        self.send_data (0x18)		
        self.send_data (0x17)		

        self.send_command(0xE0)
        self.send_data(0x02)
        self.send_command(0xE5)
        self.send_data(0x5A)

        # EPD hardware init end
        return 0
    
    def init_part(self):
        self.reset()

        self.send_command(0X00)			#PANNEL SETTING
        self.send_data(0x1F)   #KW-3f   KWR-2F	BWROTP 0f	BWOTP 1f

        self.send_command(0x04) #POWER ON
        self.delay_ms(100) 
        self.WaitUntilIdle()        #waiting for the electronic paper IC to release the idle signal

        self.send_command(0xE0)
        self.send_data(0x02)
        self.send_command(0xE5)
        self.send_data(0x6E)

        # EPD hardware init end
        return 0

    def Clear(self):
        
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1
        
        self.send_command(0x10)
        for i in range(0, wide):
            self.send_data1([0xff] * high)
                
        self.send_command(0x13) 
        for i in range(0, wide):
            self.send_data1([0x00] * high)
                
        self.TurnOnDisplay()
        
    def ClearBlack(self):
        
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1
        
        self.send_command(0x10)
        for i in range(0, wide):
            self.send_data1([0x00] * high)
                
        self.send_command(0x13) 
        for i in range(0, wide):
            self.send_data1([0xff] * high)
                
        self.TurnOnDisplay()
        
    def display(self,blackimage):
        
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1
                       
        self.send_command(0x10) 
        for i in range(0, wide):
            self.send_data1(blackimage[(i * high) : ((i+1) * high)])
        
        self.send_command(0x13) 
        for j in range(high):
            for i in range(wide):
                self.send_data(~blackimage[i + j * wide])
                
        self.TurnOnDisplay()
        
    def display_Partial(self, Image, Xstart, Ystart, Xend, Yend):
        if((Xstart % 8 + Xend % 8 == 8 & Xstart % 8 > Xend % 8) | Xstart % 8 + Xend % 8 == 0 | (Xend - Xstart)%8 == 0):
            Xstart = Xstart // 8 * 8
            Xend = Xend // 8 * 8
        else:
            Xstart = Xstart // 8 * 8
            if Xend % 8 == 0:
                Xend = Xend // 8 * 8
            else:
                Xend = Xend // 8 * 8 + 1
                
        Width = (Xend - Xstart) // 8
        Height = Yend - Ystart
	
        self.send_command(0x50)
        self.send_data(0xA9)
        self.send_data(0x07)

        self.send_command(0x91)		#This command makes the display enter partial mode
        self.send_command(0x90)		#resolution setting
        self.send_data(Xstart//256)
        self.send_data(Xstart%256)   #x-start    

        self.send_data((Xend-1)//256)		
        self.send_data((Xend-1)%256)  #x-end	

        self.send_data(Ystart//256)  #
        self.send_data(Ystart%256)   #y-start    

        self.send_data((Yend-1)//256)		
        self.send_data((Yend-1)%256)  #y-end
        self.send_data(0x01)
                       
        self.send_command(0x13) 
        for j in range(Height):
            for i in range(Width):
                self.send_data(~Image[i + j * Width])
        

        self.send_command(0x12)
        self.delay_ms(100)
        self.WaitUntilIdle()


    def sleep(self):
        self.send_command(0x02) # power off
        self.WaitUntilIdle()
        self.send_command(0x07) # deep sleep
        self.send_data(0xa5)

if __name__=='__main__':
    epd = EPD_7in5()
    epd.Clear()
    
    epd.fill(0xFF)
    
    epd.text("Waveshare", 5, 10, 0x00)
    epd.text("Pico_ePaper-7.5", 5, 40, 0x00)
    epd.text("Raspberry Pico", 5, 70, 0x00)
    epd.display(epd.buffer)
    epd.delay_ms(5000)
    
    epd.vline(10, 90, 60, 0x00)
    epd.vline(120, 90, 60, 0x00)
    epd.hline(10, 90, 110, 0x00)
    epd.hline(10, 150, 110, 0x00)
    epd.line(10, 90, 120, 150, 0x00)
    epd.line(120, 90, 10, 150, 0x00)
    epd.display(epd.buffer)
    epd.delay_ms(5000)
    
    epd.rect(10, 180, 50, 80, 0x00)
    epd.fill_rect(70, 180, 50, 80, 0x00)
    epd.display(epd.buffer)
    epd.delay_ms(5000)
    
    epd.fill_rect(250, 150, 480, 20, 0x00)
    epd.fill_rect(250, 310, 480, 20, 0x00)
    epd.fill_rect(400, 0, 20, 480, 0x00)
    epd.fill_rect(560, 0, 20, 480, 0x00)

    for j in range(0, 3):
        for i in range(0, 15):
            epd.line(270+j*160+i, 20+j*160, 375+j*160+i, 140+j*160, 0x00)
        for i in range(0, 15):
            epd.line(375+j*160+i, 20+j*160, 270+j*160+i, 140+j*160, 0x00)
        for i in range(0, 15):
            epd.line(270+j*160, 20+j*160+i, 390+j*160, 125+j*160+i, 0x00)
        for i in range(0, 15):
            epd.line(270+j*160, 125+j*160+i, 390+j*160, 20+j*160+i, 0x00)        
    epd.fill_rect(270, 190, 100, 100, 0x00)
    epd.fill_rect(270, 350, 100, 100, 0x00)
    epd.display(epd.buffer)
    epd.delay_ms(5000)
    
    # epd.init_part()
    # for i in range(0, 10):
        # epd.fill_rect(40, 260, 40, 10, 0x00)
        # epd.text(str(i), 60, 260, 0xFF)
        # epd.display_Partial(epd.buffer, 0, 0, 800, 480)
     
    epd.init() 
    epd.Clear()
    epd.delay_ms(2000)
    print("sleep")
    epd.sleep()
