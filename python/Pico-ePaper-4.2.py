# *****************************************************************************
# * | File        :	  Pico_ePaper-3.7.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2021-06-01
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
EPD_WIDTH       = 400
EPD_HEIGHT      = 300

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

EPD_4IN2_lut_vcom0 = [
0x00, 0x17, 0x00, 0x00, 0x00, 0x02,
0x00, 0x17, 0x17, 0x00, 0x00, 0x02,
0x00, 0x0A, 0x01, 0x00, 0x00, 0x01,
0x00, 0x0E, 0x0E, 0x00, 0x00, 0x02,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00,
]
EPD_4IN2_lut_ww = [
0x40, 0x17, 0x00, 0x00, 0x00, 0x02,
0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
0x40, 0x0A, 0x01, 0x00, 0x00, 0x01,
0xA0, 0x0E, 0x0E, 0x00, 0x00, 0x02,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]
EPD_4IN2_lut_bw = [
0x40, 0x17, 0x00, 0x00, 0x00, 0x02,
0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
0x40, 0x0A, 0x01, 0x00, 0x00, 0x01,
0xA0, 0x0E, 0x0E, 0x00, 0x00, 0x02,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]
EPD_4IN2_lut_wb = [
0x80, 0x17, 0x00, 0x00, 0x00, 0x02,
0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
0x80, 0x0A, 0x01, 0x00, 0x00, 0x01,
0x50, 0x0E, 0x0E, 0x00, 0x00, 0x02,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]
EPD_4IN2_lut_bb = [
0x80, 0x17, 0x00, 0x00, 0x00, 0x02,
0x90, 0x17, 0x17, 0x00, 0x00, 0x02,
0x80, 0x0A, 0x01, 0x00, 0x00, 0x01,
0x50, 0x0E, 0x0E, 0x00, 0x00, 0x02,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
]

# ******************************partial screen update LUT********************************* #
EPD_4IN2_Partial_lut_vcom1 =[
0x00,0x19,0x01,0x00,0x00,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,
]

EPD_4IN2_Partial_lut_ww1 =[
0x00,0x19,0x01,0x00,0x00,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
]

EPD_4IN2_Partial_lut_bw1 =[
0x80,0x19,0x01,0x00,0x00,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
]

EPD_4IN2_Partial_lut_wb1 =[
0x40,0x19,0x01,0x00,0x00,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
]

EPD_4IN2_Partial_lut_bb1 =[
0x00,0x19,0x01,0x00,0x00,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
]

# ******************************gray********************************* #
# 0~3 gray
EPD_4IN2_4Gray_lut_vcom=[
0x00,0x0A,0x00,0x00,0x00,0x01,
0x60,0x14,0x14,0x00,0x00,0x01,
0x00,0x14,0x00,0x00,0x00,0x01,
0x00,0x13,0x0A,0x01,0x00,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00
]
# R21
EPD_4IN2_4Gray_lut_ww =[
0x40,0x0A,0x00,0x00,0x00,0x01,
0x90,0x14,0x14,0x00,0x00,0x01,
0x10,0x14,0x0A,0x00,0x00,0x01,
0xA0,0x13,0x01,0x00,0x00,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
]
# R22H r
EPD_4IN2_4Gray_lut_bw =[
0x40,0x0A,0x00,0x00,0x00,0x01,
0x90,0x14,0x14,0x00,0x00,0x01,
0x00,0x14,0x0A,0x00,0x00,0x01,
0x99,0x0C,0x01,0x03,0x04,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
]
# R23H w
EPD_4IN2_4Gray_lut_wb =[
0x40,0x0A,0x00,0x00,0x00,0x01,
0x90,0x14,0x14,0x00,0x00,0x01,
0x00,0x14,0x0A,0x00,0x00,0x01,
0x99,0x0B,0x04,0x04,0x01,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
]
#  R24H b
EPD_4IN2_4Gray_lut_bb =[
0x80,0x0A,0x00,0x00,0x00,0x01,
0x90,0x14,0x14,0x00,0x00,0x01,
0x20,0x14,0x0A,0x00,0x00,0x01,
0x50,0x13,0x01,0x00,0x00,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
]

class EPD_4in2:
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        
        self.lut_vcom0 = EPD_4IN2_lut_vcom0
        self.lut_ww = EPD_4IN2_lut_ww
        self.lut_bw = EPD_4IN2_lut_bw
        self.lut_wb = EPD_4IN2_lut_wb
        self.lut_bb = EPD_4IN2_lut_bb
        
        self.lut_Partial_vcom = EPD_4IN2_Partial_lut_vcom1
        self.lut_Partial_ww = EPD_4IN2_Partial_lut_ww1
        self.lut_Partial_bw = EPD_4IN2_Partial_lut_bw1
        self.lut_Partial_wb = EPD_4IN2_Partial_lut_wb1
        self.lut_Partial_bb = EPD_4IN2_Partial_lut_bb1
        
        self.lut_4Gray_vcom = EPD_4IN2_4Gray_lut_vcom
        self.lut_4Gray_ww = EPD_4IN2_4Gray_lut_ww
        self.lut_4Gray_bw = EPD_4IN2_4Gray_lut_bw
        self.lut_4Gray_wb = EPD_4IN2_4Gray_lut_wb
        self.lut_4Gray_bb = EPD_4IN2_4Gray_lut_bb

        
        self.black = 0x00
        self.white = 0xff
        self.darkgray = 0xaa
        self.grayish = 0x55
        
        
        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)
        
        
        self.buffer_1Gray = bytearray(self.height * self.width // 8)
        self.buffer_4Gray = bytearray(self.height * self.width // 4)
        self.image1Gray = framebuf.FrameBuffer(self.buffer_1Gray, self.width, self.height, framebuf.MONO_HLSB)
        self.image4Gray = framebuf.FrameBuffer(self.buffer_4Gray, self.width, self.height, framebuf.GS2_HMSB)
        
        self.EPD_4IN2_Init_4Gray()
        self.EPD_4IN2_Clear()
        utime.sleep_ms(500)

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
        self.delay_ms(20) 
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(20)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(20)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(20)  

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
        print("e-Paper busy")
        while(self.digital_read(self.busy_pin) == 0):      #  LOW: idle, HIGH: busy
            self.send_command(0x71)
            self.delay_ms(100) 
        print("e-Paper busy release")
        
        
    def TurnOnDisplay(self):
        self.send_command(0x12)
        self.delay_ms(100) 
        self.ReadBusy()
    
    def EPD_4IN2_SetLut(self):
        self.send_command(0x20)
        for count in range(0, 44):
            self.send_data(self.lut_vcom0[count])
            
        self.send_command(0x21)
        for count in range(0, 42):
            self.send_data(self.lut_ww[count])
        
        self.send_command(0x22)
        for count in range(0, 42):
            self.send_data(self.lut_bw[count])
            
        self.send_command(0x23)
        for count in range(0, 42):
            self.send_data(self.lut_wb[count])
            
        self.send_command(0x24)
        for count in range(0, 42):
            self.send_data(self.lut_bb[count])
            
            
    def EPD_4IN2_Partial_SetLut(self):
        self.send_command(0x20)
        for count in range(0, 44):
            self.send_data(self.lut_Partial_vcom[count])
            
        self.send_command(0x21)
        for count in range(0, 42):
            self.send_data(self.lut_Partial_ww[count])
        
        self.send_command(0x22)
        for count in range(0, 42):
            self.send_data(self.lut_Partial_bw[count])
            
        self.send_command(0x23)
        for count in range(0, 42):
            self.send_data(self.lut_Partial_wb[count])
            
        self.send_command(0x24)
        for count in range(0, 42):
            self.send_data(self.lut_Partial_bb[count])
            
            
    def EPD_4IN2_4Gray_lut(self):
        self.send_command(0x20)
        for count in range(0, 42):
            self.send_data(self.lut_4Gray_vcom[count])
            
        self.send_command(0x21)
        for count in range(0, 42):
            self.send_data(self.lut_4Gray_ww[count])
        
        self.send_command(0x22)
        for count in range(0, 42):
            self.send_data(self.lut_4Gray_bw[count])
            
        self.send_command(0x23)
        for count in range(0, 42):
            self.send_data(self.lut_4Gray_wb[count])
            
        self.send_command(0x24)
        for count in range(0, 42):
            self.send_data(self.lut_4Gray_bb[count])
            
        self.send_command(0x25)
        for count in range(0, 42):
            self.send_data(self.lut_4Gray_ww[count])
            
    def EPD_4IN2_Init(self):
        self.reset()

        self.send_command(0x01)  # POWER SETTING
        self.send_data(0x03)
        self.send_data(0x00)
        self.send_data(0x2b)
        self.send_data(0x2b)

        self.send_command(0x06)  # boost soft start
        self.send_data(0x17)  # A
        self.send_data(0x17)  # B
        self.send_data(0x17)  # C

        self.send_command(0x04)  # POWER_ON
        self.ReadBusy()

        self.send_command(0x00)  # panel setting
        self.send_data(0xbf)  # KW-BF   KWR-AF	BWROTP 0f	BWOTP 1f
        self.send_data(0x0d)

        self.send_command(0x30)  #  PLL setting
        self.send_data(0x3C)  #  3A 100HZ   29 150Hz 39 200HZ	31 171HZ

        self.send_command(0x61)  #  resolution setting
        self.send_data(0x01)
        self.send_data(0x90)  # 128
        self.send_data(0x01)
        self.send_data(0x2c)

        self.send_command(0x82)  # vcom_DC setting
        self.send_data(0x28)

        self.send_command(0X50)  # VCOM AND DATA INTERVAL SETTING
        self.send_data(0x97)  # 97white border 77black border		VBDF 17|D7 VBDW 97 VBDB 57		VBDF F7 VBDW 77 VBDB 37  VBDR B7

        self.EPD_4IN2_SetLut()
        
    def EPD_4IN2_Init_4Gray(self):
        self.reset();
        self.send_command(0x01)  # POWER SETTING
        self.send_data (0x03)
        self.send_data (0x00)  # VGH=20V,VGL=-20V
        self.send_data (0x2b)  # VDH=15V															 
        self.send_data (0x2b)  # VDL=-15V
        self.send_data (0x13)

        self.send_command(0x06)  # booster soft start
        self.send_data (0x17)  # A
        self.send_data (0x17)  # B
        self.send_data (0x17)  # C 

        self.send_command(0x04)
        self.ReadBusy()

        self.send_command(0x00)  # panel setting
        self.send_data(0x3f)  # KW-3f   KWR-2F	BWROTP 0f	BWOTP 1f

        self.send_command(0x30)  # PLL setting
        self.send_data (0x3c)  # 100hz 

        self.send_command(0x61)  # resolution setting
        self.send_data (0x01)  # 400
        self.send_data (0x90)   
        self.send_data (0x01)  # 300
        self.send_data (0x2c)

        self.send_command(0x82)  # vcom_DC setting
        self.send_data (0x12)

        self.send_command(0X50)  # VCOM AND DATA INTERVAL SETTING			
        self.send_data(0x97)
            
    def EPD_4IN2_Clear(self):
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1

        self.send_command(0x10)
        for j in range(0, high):
            for i in range(0, wide):
                self.send_data(0xff)
                
        self.send_command(0x13)
        for j in range(0, high):
            for i in range(0, wide):
                self.send_data(0xff)

        
        self.send_command(0x12)
        self.delay_ms(10)
        self.TurnOnDisplay()
        
    def EPD_4IN2_Display(self,Image):
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1
                
        self.send_command(0x13)
        for j in range(0, high):
            for i in range(0, wide):
                self.send_data(Image[i + j * Width])
                
        self.TurnOnDisplay()
        
    def EPD_4IN2_PartialDisplay(self,X_start,Y_start,X_end,Y_end,Image):
        high = self.height
        if( self.width % 8 == 0) :
            wide =  self.width // 8
        else :
            wide =  self.width // 8 + 1
            
        if( X_start % 8 == 0) :
            X_start =  X_start
        else :
            X_start =  X_start // 8 * 8 + 8
            
        if( X_end % 8 == 0) :
            X_end =  X_end
        else :
            X_end =  X_end // 8 * 8 + 8
                
        self.send_command(0X50);
        self.send_data(0xf7);
        self.delay_ms(100);
        
        self.send_command(0x82)  # vcom_DC setting  	
        self.send_data (0x08)
        self.send_command(0X50)
        self.send_data(0x47)
        EPD_4IN2_Partial_SetLut()
        self.send_command(0x91)  # This command makes the display enter partial mode
        self.send_command(0x90)  # resolution setting
        self.send_data ((X_start)/256)
        self.send_data ((X_start)%256)  # x-start    

        self.send_data ((X_end )/256)
        self.send_data ((X_end )%256-1)  # x-end

        self.send_data (Y_start/256)
        self.send_data (Y_start%256)  # y-start    

        self.send_data (Y_end/256)
        self.send_data (Y_end%256-1)  # y-end
        self.send_data (0x28)

        self.send_command(0x10)  # writes Old data to SRAM for programming
        for j in range(0, high):
            for i in range(0, wide):
                self.send_data(0xff)
                
        self.send_command(0x13)  # writes New data to SRAM.
        for j in range(0, high):
            for i in range(0, wide):
                self.send_data(0xff)

        self.send_command(0x12)  # DISPLAY REFRESH     
        self.delay_ms(10)  # The delay here is necessary, 200uS at least!!!     
        self.TurnOnDisplay()
        
    def EPD_4IN2_4GrayDisplay(self,Image):
        self.send_command(0x10)
        for i in range(0, 15000):
            temp3=0
            for j in range(0, 2):
                temp1 = Image[i*2+j]
                for k in range(0, 2):
                    temp2 = temp1&0x03 
                    if(temp2 == 0x03):
                        temp3 |= 0x01   # white
                    elif(temp2 == 0x00):
                        temp3 |= 0x00   # black
                    elif(temp2 == 0x02):
                        temp3 |= 0x00   # gray1
                    else:   # 0x01
                        temp3 |= 0x01   # gray2
                    temp3 <<= 1

                    temp1 >>= 2
                    temp2 = temp1&0x03 
                    if(temp2 == 0x03):   # white
                        temp3 |= 0x01;
                    elif(temp2 == 0x00):   # black
                        temp3 |= 0x00;
                    elif(temp2 == 0x02):
                        temp3 |= 0x00   # gray1
                    else:   # 0x01
                        temp3 |= 0x01   # gray2
                    
                    if (( j!=1 ) | ( k!=1 )):
                        temp3 <<= 1

                    temp1 >>= 2
                    
            self.send_data(temp3)
        
        self.send_command(0x13)
        for i in range(0, 15000):
            temp3=0
            for j in range(0, 2):
                temp1 = Image[i*2+j]
                for k in range(0, 2):
                    temp2 = temp1&0x03 
                    if(temp2 == 0x03):
                        temp3 |= 0x01   # white
                    elif(temp2 == 0x00):
                        temp3 |= 0x00   # black
                    elif(temp2 == 0x02):
                        temp3 |= 0x01   # gray1
                    else:   # 0x01
                        temp3 |= 0x00   # gray2
                    temp3 <<= 1

                    temp1 >>= 2
                    temp2 = temp1&0x03
                    if(temp2 == 0x03):   # white
                        temp3 |= 0x01;
                    elif(temp2 == 0x00):   # black
                        temp3 |= 0x00;
                    elif(temp2 == 0x02):
                        temp3 |= 0x01   # gray1
                    else:   # 0x01
                        temp3 |= 0x00   # gray2
                    
                    if (( j!=1 ) | ( k!=1 )):
                        temp3 <<= 1

                    temp1 >>= 2

            self.send_data(temp3)
        
        self.EPD_4IN2_4Gray_lut()
        self.TurnOnDisplay()
        
    def Sleep(self):
#         self.send_command(0X02)  # power off
#         self.ReadBusy()
        self.send_command(0X07)  # deep sleep
        self.send_data(0xA5)
    
if __name__=='__main__':
    
    epd = EPD_4in2()
    
    epd.image1Gray.fill(0xff)
    epd.image4Gray.fill(0xff)
    
    epd.image4Gray.text("Waveshare", 5, 10, epd.black)
    epd.image4Gray.text("Pico_ePaper-4.2", 5, 40, epd.black)
    epd.image4Gray.text("Raspberry Pico", 5, 70, epd.black)
    epd.EPD_4IN2_4GrayDisplay(epd.buffer_4Gray)
    epd.delay_ms(500)
    
    epd.image4Gray.vline(10, 90, 60, epd.black)
    epd.image4Gray.vline(90, 90, 60, epd.black)
    epd.image4Gray.hline(10, 90, 80, epd.black)
    epd.image4Gray.hline(10, 150, 80, epd.black)
    epd.image4Gray.line(10, 90, 90, 150, epd.black)
    epd.image4Gray.line(90, 90, 10, 150, epd.black)
    epd.EPD_4IN2_4GrayDisplay(epd.buffer_4Gray)
    epd.delay_ms(500)
    
    epd.image4Gray.rect(10, 180, 50, 80, epd.black)
    epd.image4Gray.fill_rect(70, 180, 50, 80, epd.black)
    epd.EPD_4IN2_4GrayDisplay(epd.buffer_4Gray)
    epd.delay_ms(500)
   
    epd.image4Gray.fill_rect(150, 10, 250, 30, epd.black)
    epd.image4Gray.text('GRAY1 with black background',155, 21, epd.white)
    epd.image4Gray.text('GRAY2 with white background',155, 51, epd.grayish)
    epd.image4Gray.text('GRAY3 with white background',155, 81, epd.darkgray)
    epd.image4Gray.text('GRAY4 with white background',155, 111, epd.black)
    epd.EPD_4IN2_4GrayDisplay(epd.buffer_4Gray)
    epd.delay_ms(500)
    

    



    epd.Sleep()


