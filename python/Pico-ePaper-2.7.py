# *****************************************************************************
# * | File        :  Pico_ePaper-2.7.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2021-06-03
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
EPD_WIDTH       = 176
EPD_HEIGHT      = 264

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

EPD_2in7_lut_vcom_dc = [
    0x00,0x00,
    0x00,0x08,0x00,0x00,0x00,0x02,
    0x60,0x28,0x28,0x00,0x00,0x01,
    0x00,0x14,0x00,0x00,0x00,0x01,
    0x00,0x12,0x12,0x00,0x00,0x01,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00
]
EPD_2in7_lut_ww = [
    0x40,0x08,0x00,0x00,0x00,0x02,
    0x90,0x28,0x28,0x00,0x00,0x01,
    0x40,0x14,0x00,0x00,0x00,0x01,
    0xA0,0x12,0x12,0x00,0x00,0x01,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
]
EPD_2in7_lut_bw = [
    0x40,0x08,0x00,0x00,0x00,0x02,
    0x90,0x28,0x28,0x00,0x00,0x01,
    0x40,0x14,0x00,0x00,0x00,0x01,
    0xA0,0x12,0x12,0x00,0x00,0x01,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
]
EPD_2in7_lut_bb = [
    0x80,0x08,0x00,0x00,0x00,0x02,
    0x90,0x28,0x28,0x00,0x00,0x01,
    0x80,0x14,0x00,0x00,0x00,0x01,
    0x50,0x12,0x12,0x00,0x00,0x01,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
]
EPD_2in7_lut_wb = [
    0x80,0x08,0x00,0x00,0x00,0x02,
    0x90,0x28,0x28,0x00,0x00,0x01,
    0x80,0x14,0x00,0x00,0x00,0x01,
    0x50,0x12,0x12,0x00,0x00,0x01,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,
]

# # # # # # # # # # # # # # # # # # # full screen update LUT# # # # # # # # # # # # # # # # # # # # # # 
# 0~3 gray
EPD_2in7_gray_lut_vcom =[
0x00,0x00,
0x00,0x0A,0x00,0x00,0x00,0x01,
0x60,0x14,0x14,0x00,0x00,0x01,
0x00,0x14,0x00,0x00,0x00,0x01,
0x00,0x13,0x0A,0x01,0x00,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
]
# R21
EPD_2in7_gray_lut_ww =[
0x40,0x0A,0x00,0x00,0x00,0x01,
0x90,0x14,0x14,0x00,0x00,0x01,
0x10,0x14,0x0A,0x00,0x00,0x01,
0xA0,0x13,0x01,0x00,0x00,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
]
# R22Hr
EPD_2in7_gray_lut_bw =[
0x40,0x0A,0x00,0x00,0x00,0x01,
0x90,0x14,0x14,0x00,0x00,0x01,
0x00,0x14,0x0A,0x00,0x00,0x01,
0x99,0x0C,0x01,0x03,0x04,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
]
# R23Hw
EPD_2in7_gray_lut_wb =[
0x40,0x0A,0x00,0x00,0x00,0x01,
0x90,0x14,0x14,0x00,0x00,0x01,
0x00,0x14,0x0A,0x00,0x00,0x01,
0x99,0x0B,0x04,0x04,0x01,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
]
# R24Hb
EPD_2in7_gray_lut_bb =[
0x80,0x0A,0x00,0x00,0x00,0x01,
0x90,0x14,0x14,0x00,0x00,0x01,
0x20,0x14,0x0A,0x00,0x00,0x01,
0x50,0x13,0x01,0x00,0x00,0x01,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,
]

class EPD_2in7:
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        
        self.lut_vcom_dc = EPD_2in7_lut_vcom_dc
        self.lut_ww = EPD_2in7_lut_ww
        self.lut_bw = EPD_2in7_lut_bw
        self.lut_bb = EPD_2in7_lut_bb
        self.lut_wb = EPD_2in7_lut_wb
        
        self.gray_lut_vcom = EPD_2in7_gray_lut_vcom
        self.gray_lut_ww = EPD_2in7_gray_lut_ww
        self.gray_lut_bw = EPD_2in7_gray_lut_bw
        self.gray_lut_wb = EPD_2in7_gray_lut_wb
        self.gray_lut_bb = EPD_2in7_gray_lut_bb
        
        self.black = 0x00
        self.white = 0xff
        self.darkgray = 0xaa
        self.grayish = 0x55
        
        
        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)
        
        self.buffer_1Gray_Landscape = bytearray(self.height * self.width // 8)
        self.buffer_1Gray_Portrait = bytearray(self.height * self.width // 8)
        self.buffer_4Gray = bytearray(self.height * self.width // 4)
        
        self.image1Gray_Landscape = framebuf.FrameBuffer(self.buffer_1Gray_Landscape, self.height, self.width, framebuf.MONO_VLSB)
        self.image1Gray_Portrait = framebuf.FrameBuffer(self.buffer_1Gray_Portrait, self.width, self.height, framebuf.MONO_HLSB)
        self.image4Gray = framebuf.FrameBuffer(self.buffer_4Gray, self.width, self.height, framebuf.GS2_HMSB)
        
        self.EPD_2IN7_Init_4Gray()
        self.EPD_2IN7_Clear()
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
        
    def ReadBusy(self):
        print("e-Paper busy")
        while(self.digital_read(self.busy_pin) == 0):      #  0: idle, 1: busy
            self.send_command(0x71)
        self.delay_ms(200) 
        print("e-Paper busy release")
        
    def SetLut(self):
        self.send_command(0x20)
        for count in range(0, 44):
            self.send_data(self.lut_vcom_dc[count])
            
        self.send_command(0x21)
        for count in range(0, 42):
            self.send_data(self.lut_ww[count])
        
        self.send_command(0x22)
        for count in range(0, 42):
            self.send_data(self.lut_bw[count])
            
        self.send_command(0x23)
        for count in range(0, 42):
            self.send_data(self.lut_bb[count])
            
        self.send_command(0x24)
        for count in range(0, 42):
            self.send_data(self.lut_wb[count])
            
    def gray_SetLut(self):
        self.send_command(0x20)
        for count in range(0, 44):
            self.send_data(self.gray_lut_vcom[count])
            
        self.send_command(0x21)
        for count in range(0, 42):
            self.send_data(self.gray_lut_ww[count])
        
        self.send_command(0x22)
        for count in range(0, 42):
            self.send_data(self.gray_lut_bw[count])
            
        self.send_command(0x23)
        for count in range(0, 42):
            self.send_data(self.gray_lut_wb[count])
            
        self.send_command(0x24)
        for count in range(0, 42):
            self.send_data(self.gray_lut_bb[count])
            
        self.send_command(0x25)
        for count in range(0, 42):
            self.send_data(self.gray_lut_ww[count])
            
        
    def EPD_2IN7_Init(self):
    
        self.reset();

        self.send_command(0x01)  # POWER_SETTING
        self.send_data(0x03)  # VDS_EN, VDG_EN
        self.send_data(0x00)  # VCOM_HV, VGHL_LV[1], VGHL_LV[0]
        self.send_data(0x2b)  # VDH
        self.send_data(0x2b)  # VDL
        self.send_data(0x09)  # VDHR
        
        self.send_command(0x06)  # BOOSTER_SOFT_START
        self.send_data(0x07)
        self.send_data(0x07)
        self.send_data(0x17)
        
        # Power optimization
        self.send_command(0xF8)
        self.send_data(0x60)
        self.send_data(0xA5)
        
        # Power optimization
        self.send_command(0xF8)
        self.send_data(0x89)
        self.send_data(0xA5)
            
        # Power optimization
        self.send_command(0xF8)
        self.send_data(0x90)
        self.send_data(0x00)
            
        # Power optimization
        self.send_command(0xF8)
        self.send_data(0x93)
        self.send_data(0x2A)
            
        # Power optimization
        self.send_command(0xF8)
        self.send_data(0xA0)
        self.send_data(0xA5)
            
        # Power optimization
        self.send_command(0xF8)
        self.send_data(0xA1)
        self.send_data(0x00)
            
        # Power optimization
        self.send_command(0xF8)
        self.send_data(0x73)
        self.send_data(0x41)
            
        self.send_command(0x16)  # PARTIAL_DISPLAY_REFRESH
        self.send_data(0x00)
            
        self.send_command(0x04)  # POWER_ON
        self.ReadBusy();

        self.send_command(0x00)  # PANEL_SETTING
        self.send_data(0xAF)  # KW-BF   KWR-AF    BWROTP 0f
        self.send_command(0x30)  #  PLL_CONTROL
        self.send_data(0x3A)  # 3A 100HZ   29 150Hz 39 200HZ    31 171HZ
        self.send_command(0x82)  # VCM_DC_SETTING_REGISTER
        self.send_data(0x12)

        self.SetLut()

    def EPD_2IN7_Init_4Gray(self):
        
        self.reset()
        
        self.send_command(0x01)  # POWER SETTING
        self.send_data (0x03)
        self.send_data (0x00)   
        self.send_data (0x2b)
        self.send_data (0x2b)


        self.send_command(0x06)  # booster soft start
        self.send_data (0x07)  # A
        self.send_data (0x07)  # B
        self.send_data (0x17)  # C 

        self.send_command(0xF8)  # boost??
        self.send_data (0x60)
        self.send_data (0xA5)

        self.send_command(0xF8)  # boost??
        self.send_data (0x89)
        self.send_data (0xA5)

        self.send_command(0xF8)  # boost??
        self.send_data (0x90)
        self.send_data (0x00)

        self.send_command(0xF8)  # boost??
        self.send_data (0x93)
        self.send_data (0x2A)

        self.send_command(0xF8)  # boost??
        self.send_data (0xa0)
        self.send_data (0xa5)

        self.send_command(0xF8)  # boost??
        self.send_data (0xa1)
        self.send_data (0x00)

        self.send_command(0xF8)  # boost??
        self.send_data (0x73)
        self.send_data (0x41)

        self.send_command(0x16)
        self.send_data(0x00)

        self.send_command(0x04)
        self.ReadBusy()

        self.send_command(0x00)  # panel setting
        self.send_data(0xbf)  # KW-BF   KWR-AF	BWROTP 0f

        self.send_command(0x30)  # PLL setting
        self.send_data (0x90)  # 100hz 

        self.send_command(0x61)  # resolution setting
        self.send_data (0x00)  # 176
        self.send_data (0xb0)
        self.send_data (0x01)  # 264
        self.send_data (0x08)

        self.send_command(0x82)  # vcom_DC setting
        self.send_data (0x12)

        self.send_command(0X50)  # VCOM AND DATA INTERVAL SETTING			
        self.send_data(0x97)
            
    def EPD_2IN7_Clear(self):
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
        self.ReadBusy()

    def EPD_2IN7_Display_Portrait(self,Image):
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
                self.send_data(Image[i + j * wide])

    
    def EPD_2IN7_Display_Landscape(self,Image):
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
                self.send_data(Image[(21-i) * high + j])

        
        self.send_command(0x12)
        self.ReadBusy()
        
    def EPD_2IN7_4Gray_Display(self,Image):
        
        self.send_command(0x10)
        for i in range(0, 5808):
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
        for i in range(0, 5808):
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
        
        self.gray_SetLut()
        
        self.send_command(0x12)
        self.delay_ms(500)
        
        self.ReadBusy()

        
    def Sleep(self):
        self.send_command(0X50)
        self.send_data(0xf7)
        self.send_command(0X02)  # power off
        self.send_command(0X07)  # deep sleep
        self.send_data(0xA5)
    
if __name__=='__main__':
    
    epd = EPD_2in7()
    
    epd.image1Gray_Landscape.fill(0xff)
    epd.image1Gray_Portrait.fill(0xff)
    epd.image4Gray.fill(0xff)
    
    epd.image4Gray.text("Waveshare", 5, 5, epd.black)
    epd.image4Gray.text("Pico_ePaper-2.7", 5, 20, epd.black)
    epd.image4Gray.text("Raspberry Pico", 5, 35, epd.black)
    epd.EPD_2IN7_4Gray_Display(epd.buffer_4Gray)
    epd.delay_ms(500)
    
    epd.image4Gray.vline(10, 60, 60, epd.black)
    epd.image4Gray.vline(90, 60, 60, epd.black)
    epd.image4Gray.hline(10, 60, 80, epd.black)
    epd.image4Gray.hline(10, 120, 80, epd.black)
    epd.image4Gray.line(10, 60, 90, 120, epd.black)
    epd.image4Gray.line(90, 60, 10, 120, epd.black)
    epd.EPD_2IN7_4Gray_Display(epd.buffer_4Gray)
    epd.delay_ms(500)
    
    epd.image4Gray.rect(10, 136, 50, 80, epd.black)
    epd.image4Gray.fill_rect(70, 136, 50, 80, epd.black)
    epd.EPD_2IN7_4Gray_Display(epd.buffer_4Gray)
    epd.delay_ms(500)
   
    epd.image4Gray.fill_rect(0, 232, 88, 16, epd.black)
    epd.image4Gray.text('GRAY1',24, 236, epd.white)
    epd.image4Gray.text('GRAY2',24, 252, epd.grayish)
    epd.image4Gray.text('GRAY3',112, 236, epd.darkgray)
    epd.image4Gray.text('GRAY4',112, 252, epd.black)
    epd.EPD_2IN7_4Gray_Display(epd.buffer_4Gray)
    epd.delay_ms(500)
    

    
    epd.EPD_2IN7_Init()
    epd.EPD_2IN7_Clear()
    epd.image1Gray_Landscape.text("Waveshare", 5, 5, epd.black)
    epd.image1Gray_Landscape.text("Pico_ePaper-2.7", 5, 20, epd.black)
    epd.image1Gray_Landscape.text("Raspberry Pico", 5, 35, epd.black)
    epd.EPD_2IN7_Display_Landscape(epd.buffer_1Gray_Landscape)
    epd.delay_ms(500)
    
    epd.EPD_2IN7_Clear()
    print("Sleep")
    epd.Sleep()




