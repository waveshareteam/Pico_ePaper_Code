# *****************************************************************************
# * | File        :  Pico_ePaper-2.7_V2.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2022-03-15
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

LUT_DATA_4Gray = [
        0x40,0x48,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x8,0x48,0x10,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x2,0x48,0x4,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x20,0x48,0x1,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,
        0xA,0x19,0x0,0x3,0x8,0x0,0x0,                    
        0x14,0x1,0x0,0x14,0x1,0x0,0x3,                    
        0xA,0x3,0x0,0x8,0x19,0x0,0x0,                    
        0x1,0x0,0x0,0x0,0x0,0x0,0x1,                    
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,                    
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,                    
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,                    
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,                    
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,                    
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,                    
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,                    
        0x0,0x0,0x0,0x0,0x0,0x0,0x0,                    
        0x22,0x22,0x22,0x22,0x22,0x22,0x0,0x0,0x0,            
        0x22,0x17,0x41,0x0,0x32,0x1C,
        ]


class EPD_2in7_V2:
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        
        self.black = 0x00
        self.white = 0xff
        self.darkgray = 0xaa
        self.grayish = 0x55
        
        self.LUT_DATA_4Gray = LUT_DATA_4Gray
        
        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)
        
        self.buffer_1Gray_Landscape = bytearray(self.height * self.width // 8)
        self.buffer_1Gray_Portrait = bytearray(self.height * self.width // 8)
        self.buffer_4Gray = bytearray(self.height * self.width // 4)
        
        self.image1Gray_Landscape = framebuf.FrameBuffer(self.buffer_1Gray_Landscape, self.height, self.width, framebuf.MONO_VLSB)
        self.image1Gray_Portrait = framebuf.FrameBuffer(self.buffer_1Gray_Portrait, self.width, self.height, framebuf.MONO_HLSB)
        self.image4Gray = framebuf.FrameBuffer(self.buffer_4Gray, self.width, self.height, framebuf.GS2_HMSB)
        
        self.init()
        self.clear()
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
        
    def send_data1(self, buf):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buf))
        self.digital_write(self.cs_pin, 1)
        
    def ReadBusy(self):
        print("e-Paper busy")
        while(self.digital_read(self.busy_pin) == 1):      #  1: idle, 0: busy
            self.delay_ms(2)
        self.delay_ms(200) 
        print("e-Paper busy release")
        
    def TurnOnDisplay(self):
        self.send_command(0x22) #Display Update Control
        self.send_data(0xF7)
        self.send_command(0x20) #Activate Display Update Sequence
        self.ReadBusy()
        
    def TurnOnDisplay_Fast(self):
        self.send_command(0x22) #Display Update Control
        self.send_data(0xC7)
        self.send_command(0x20) #Activate Display Update Sequence
        self.ReadBusy()
        
    def TurnOnDisplay_Partial(self):
        self.send_command(0x22) #Display Update Control
        self.send_data(0xFF)
        self.send_command(0x20) #Activate Display Update Sequence
        self.ReadBusy()
        
    def TurnOnDisplay_4GRAY(self):
        self.send_command(0x22) #Display Update Control
        self.send_data(0xC7)
        self.send_command(0x20) #Activate Display Update Sequence
        self.ReadBusy()
            
        
    def Lut(self):
        self.send_command(0x32)
        for i in range(159):
            self.send_data(self.LUT_DATA_4Gray[i])
            
    def init(self):
            
        # EPD hardware init start
        self.reset()
        self.ReadBusy()

        self.send_command(0x12) #SWRESET
        self.ReadBusy()

        self.send_command(0x45) #set Ram-Y address start/end position          
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x07) #0x0107-->(263+1)=264
        self.send_data(0x01)

        self.send_command(0x4F)   # set RAM y address count to 0;    
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x11)  # data entry mode
        self.send_data(0x03)
        return 0
        
    def init_Fast(self):
            
        # EPD hardware init start
        self.reset()
        self.ReadBusy()

        self.send_command(0x12) #SWRESET
        self.ReadBusy()

        self.send_command(0x12) #SWRESET
        self.ReadBusy()

        self.send_command(0x18) #Read built-in temperature sensor
        self.send_data(0x80)    

        self.send_command(0x22) # Load temperature value
        self.send_data(0xB1)    
        self.send_command(0x20)    
        self.ReadBusy()

        self.send_command(0x1A) # Write to temperature register
        self.send_data(0x64)    
        self.send_data(0x00)    

        self.send_command(0x45) #set Ram-Y address start/end position          
        self.send_data(0x00)   
        self.send_data(0x00)
        self.send_data(0x07) #0x0107-->(263+1)=264
        self.send_data(0x01)

        self.send_command(0x4F)   # set RAM y address count to 0;    
        self.send_data(0x00)
        self.send_data(0x00)

        self.send_command(0x11)   # data entry mode      
        self.send_data(0x03)

        self.send_command(0x22) # Load temperature value
        self.send_data(0x91)    
        self.send_command(0x20)    
        self.ReadBusy()
        return 0

    def init_4Gray(self):

        self.reset()
        
        self.send_command(0x12) # soft reset
        self.ReadBusy();

        self.send_command(0x74) #set analog block control       
        self.send_data(0x54)
        self.send_command(0x7E) #set digital block control          
        self.send_data(0x3B)
        
        self.send_command(0x01) #Driver output control      
        self.send_data(0x07)
        self.send_data(0x01)
        self.send_data(0x00) 
        
        self.send_command(0x11) #data entry mode       
        self.send_data(0x03)

        self.send_command(0x44) #set Ram-X address start/end position   
        self.send_data(0x00)
        self.send_data(0x15)   #0x15-->(21+1)*8=176

        self.send_command(0x45) #set Ram-Y address start/end position          
        self.send_data(0x00)
        self.send_data(0x00)
        self.send_data(0x07) #0x0107-->(263+1)=264
        self.send_data(0x01)

        self.send_command(0x3C) #BorderWavefrom
        self.send_data(0x00)    

        self.send_command(0x2C)     #VCOM Voltage
        self.send_data(self.LUT_DATA_4Gray[158])    #0x1C

        self.send_command(0x3F) #EOPQ    
        self.send_data(self.LUT_DATA_4Gray[153])

        self.send_command(0x03) #VGH      
        self.send_data(self.LUT_DATA_4Gray[154])

        self.send_command(0x04) #      
        self.send_data(self.LUT_DATA_4Gray[155]) #VSH1   
        self.send_data(self.LUT_DATA_4Gray[156]) #VSH2   
        self.send_data(self.LUT_DATA_4Gray[157]) #VSL   

        self.Lut() #LUT

        self.send_command(0x4E)   # set RAM x address count to 0;
        self.send_data(0x00)
        self.send_command(0x4F)  # set RAM y address count to 0X199;    
        self.send_data(0x00)
        self.send_data(0x00)
        self.ReadBusy()
        return 0
            
    def clear(self):
        if(self.width % 8 == 0):
            Width = self.width // 8
        else:
            Width = self.width // 8 +1
        Height = self.height
        self.send_command(0x24)
        self.send_data1([0xff] * Width * Height)
        self.TurnOnDisplay()
    
    def display(self, image):
        if(self.width % 8 == 0):
            Width = self.width // 8
        else:
            Width = self.width // 8 +1
        Height = self.height
        self.send_command(0x24)
        self.send_data1(image)
        self.TurnOnDisplay()
        
    def display_Landscape(self, image):
        if(self.width % 8 == 0):
            Width = self.width // 8
        else:
            Width = self.width // 8 +1
        Height = self.height
        self.send_command(0x24)
        for j in range(Height):
            for i in range(Width):
                self.send_data(image[(21-i) * Height + j])
        self.TurnOnDisplay()
        
    def display_Fast(self, image):
        if(self.width % 8 == 0):
            Width = self.width // 8
        else:
            Width = self.width // 8 +1
        Height = self.height
        self.send_command(0x24)
        self.send_data1(image)
        self.TurnOnDisplay_Fast()
        
    def display_Base(self, image):
        if(self.width % 8 == 0):
            Width = self.width // 8
        else:
            Width = self.width // 8 +1
        Height = self.height
        self.send_command(0x24)   #Write Black and White image to RAM
        self.send_data1(image)
                
        self.send_command(0x26)  #Write Black and White image to RAM
        self.send_data1(image)
        
        self.TurnOnDisplay()
        
    def display_Base_color(self, color):
        if(self.width % 8 == 0):
            Width = self.width // 8
        else:
            Width = self.width // 8 +1
        Height = self.height
        self.send_command(0x24)   #Write Black and White image to RAM
        self.send_data1([color] * Width * Height)
                
        self.send_command(0x26)  #Write Black and White image to RAM
        self.send_data1([color] * Width * Height)
        
        # self.TurnOnDisplay()
    
    def display_Partial(self, image):
        
        if(self.width % 8 == 0):
            Width = self.width // 8
        else:
            Width = self.width // 8 +1
        Height = self.height
        
        self.reset()

        self.send_command(0x3C) #BorderWavefrom
        self.send_data(0x80)

        self.send_command(0x24)   #Write Black and White image to RAM
        self.send_data1(image)
        
        self.TurnOnDisplay_Partial()
  
    def display_4Gray(self, image):
        self.send_command(0x24)
        for i in range(0, 5808):                     #5808*4  46464
            temp3=0
            for j in range(0, 2):
                temp1 = image[i*2+j]
                for k in range(0, 2):
                    temp2 = temp1&0x03 
                    if(temp2 == 0x03):
                        temp3 |= 0x00   # white
                    elif(temp2 == 0x00):
                        temp3 |= 0x01   # black
                    elif(temp2 == 0x02):
                        temp3 |= 0x00   # gray1
                    else:   # 0x01
                        temp3 |= 0x01   # gray2
                    temp3 <<= 1

                    temp1 >>= 2
                    temp2 = temp1&0x03 
                    if(temp2 == 0x03):   # white
                        temp3 |= 0x00;
                    elif(temp2 == 0x00):   # black
                        temp3 |= 0x01;
                    elif(temp2 == 0x02):
                        temp3 |= 0x00   # gray1
                    else:   # 0x01
                        temp3 |= 0x01   # gray2
                    
                    if (( j!=1 ) | ( k!=1 )):
                        temp3 <<= 1
                    temp1 >>= 2
            self.send_data(temp3)
            
        self.send_command(0x26)           
        for i in range(0, 5808):                #5808*4  46464
            temp3=0
            for j in range(0, 2):
                temp1 = image[i*2+j]
                for k in range(0, 2):
                    temp2 = temp1&0x03 
                    if(temp2 == 0x03):
                        temp3 |= 0x00   # white
                    elif(temp2 == 0x00):
                        temp3 |= 0x01   # black
                    elif(temp2 == 0x02):
                        temp3 |= 0x01   # gray1
                    else:   # 0x01
                        temp3 |= 0x00   # gray2
                    temp3 <<= 1

                    temp1 >>= 2
                    temp2 = temp1&0x03
                    if(temp2 == 0x03):   # white
                        temp3 |= 0x00;
                    elif(temp2 == 0x00):   # black
                        temp3 |= 0x01;
                    elif(temp2 == 0x02):
                        temp3 |= 0x01   # gray1
                    else:   # 0x01
                        temp3 |= 0x00   # gray2  
                    if(j!=1 or k!=1):                    
                        temp3 <<= 1
                    temp1 >>= 2
            self.send_data(temp3)
        
        self.TurnOnDisplay_4GRAY()

    def sleep(self):
        self.send_command(0X10)
        self.send_data(0x01)

    
if __name__=='__main__':
    
    epd = EPD_2in7_V2()
    
    epd.image1Gray_Landscape.fill(0xff)
    epd.image1Gray_Portrait.fill(0xff)
    epd.image4Gray.fill(0xff)
    # You are advised to fill the cache area inside the ink screen first. Otherwise, the office brush may be abnormal
    epd.display_Base_color(0xff)
    
    epd.image1Gray_Portrait.text("Waveshare", 5, 5, epd.black)
    epd.image1Gray_Portrait.text("Pico_ePaper-2.7", 5, 20, epd.black)
    epd.image1Gray_Portrait.text("Raspberry Pico", 5, 35, epd.black)
    epd.display_Fast(epd.buffer_1Gray_Portrait)
    epd.delay_ms(500)

    epd.image1Gray_Portrait.vline(10, 60, 60, epd.black)
    epd.image1Gray_Portrait.vline(90, 60, 60, epd.black)
    epd.image1Gray_Portrait.hline(10, 60, 80, epd.black)
    epd.image1Gray_Portrait.hline(10, 120, 80, epd.black)
    epd.image1Gray_Portrait.line(10, 60, 90, 120, epd.black)
    epd.image1Gray_Portrait.line(90, 60, 10, 120, epd.black)
    epd.display_Fast(epd.buffer_1Gray_Portrait)
    epd.delay_ms(500)
    
    epd.image1Gray_Portrait.rect(10, 136, 50, 80, epd.black)
    epd.image1Gray_Portrait.fill_rect(70, 136, 50, 80, epd.black)
    epd.display_Fast(epd.buffer_1Gray_Portrait)
    epd.delay_ms(500)
    
    for i in range(0, 10):
        epd.image1Gray_Portrait.fill_rect(60, 240, 40, 10, 0xff)
        epd.image1Gray_Portrait.text(str(i), 80, 241, 0x00)
        epd.display_Partial(epd.buffer_1Gray_Portrait)
   
    epd.init_4Gray()
    epd.image4Gray.fill_rect(0, 0, 175, 68, epd.black)
    epd.image4Gray.text('GRAY1',10, 30, epd.white)
    epd.image4Gray.fill_rect(0, 68, 175, 68, epd.darkgray)
    epd.image4Gray.text('GRAY2',10, 98, epd.grayish)
    epd.image4Gray.fill_rect(0, 136, 175, 68, epd.grayish)
    epd.image4Gray.text('GRAY3',10, 166, epd.darkgray)
    epd.image4Gray.fill_rect(0, 204, 175, 68, epd.white)
    epd.image4Gray.text('GRAY4',10, 234, epd.black)
    epd.display_4Gray(epd.buffer_4Gray)
    epd.delay_ms(500)

    epd.init()
    epd.clear()
    epd.image1Gray_Landscape.text("Waveshare", 5, 5, epd.black)
    epd.image1Gray_Landscape.text("Pico_ePaper-2.7", 5, 20, epd.black)
    epd.image1Gray_Landscape.text("Raspberry Pico", 5, 35, epd.black)
    epd.display_Landscape(epd.buffer_1Gray_Landscape)
    epd.delay_ms(500)
    
    epd.clear()
    print("Sleep")
    epd.sleep()




