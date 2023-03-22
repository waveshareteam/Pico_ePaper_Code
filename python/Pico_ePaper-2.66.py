# *****************************************************************************
# * | File        :	  Pico_ePaper-2.66.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2021-05-12
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
EPD_WIDTH       = 152
EPD_HEIGHT      = 296

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13


WF_PARTIAL_2IN66 =[
0x00,0x40,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x40,0x40,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x0A,0x00,0x00,0x00,0x00,0x00,0x02,0x01,0x00,0x00,
0x00,0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x22,0x22,0x22,0x22,0x22,0x22,
0x00,0x00,0x00,0x22,0x17,0x41,0xB0,0x32,0x36,
]

class EPD_2in66:
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        self.lut = WF_PARTIAL_2IN66

        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)
        
        self.buffer_Landscape = bytearray(self.height * self.width // 8)
        self.buffer_Portrait = bytearray(self.height * self.width // 8)
        
        self.image_Landscape = framebuf.FrameBuffer(self.buffer_Landscape, self.height, self.width, framebuf.MONO_VLSB)
        self.image_Portrait = framebuf.FrameBuffer(self.buffer_Portrait, self.width, self.height, framebuf.MONO_HLSB)
        self.init(0)

    # Hardware reset
    def reset(self):
        self.reset_pin(1)
        utime.sleep_ms(200) 
        self.reset_pin(0)
        utime.sleep_ms(200)
        self.reset_pin(1)
        utime.sleep_ms(200)   

    def send_command(self, command):
        self.cs_pin(1)
        self.dc_pin(0)
        self.cs_pin(0)
        self.spi.write(bytearray([command]))
        self.cs_pin(1)

    def send_data(self, data):
        self.cs_pin(1)
        self.dc_pin(1)
        self.cs_pin(0)
        self.spi.write(bytearray([data]))
        self.cs_pin(1)
        
    def send_data1(self, buf):
        self.cs_pin(1)
        self.dc_pin(1)
        self.cs_pin(0)
        self.spi.write(bytearray(buf))
        self.cs_pin(1)
        
    def ReadBusy(self):
        print('e-Paper busy')
        utime.sleep_ms(100)   
        while(self.busy_pin.value() == 1):      # 0: idle, 1: busy
            utime.sleep_ms(100)    
        print('e-Paper busy release')
        utime.sleep_ms(100)  
        
    def TurnOnDisplay(self):
        self.send_command(0x20)        
        self.ReadBusy()
        
    def SendLut(self):
        self.send_command(0x32)
        for i in range(0, 153):
            self.send_data(self.lut[i])
        self.ReadBusy()
    
    def SetWindow(self, x_start, y_start, x_end, y_end):
        self.send_command(0x44) # SET_RAM_X_ADDRESS_START_END_POSITION
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data((x_start>>3) & 0xFF)
        self.send_data((x_end>>3) & 0xFF)
        self.send_command(0x45) # SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(y_start & 0xFF)
        self.send_data((y_start >> 8) & 0xFF)
        self.send_data(y_end & 0xFF)
        self.send_data((y_end >> 8) & 0xFF)

    def SetCursor(self, x, y):
        self.send_command(0x4E) # SET_RAM_X_ADDRESS_COUNTER
        self.send_data(x & 0xFF)
        
        self.send_command(0x4F) # SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(y & 0xFF)
        self.send_data((y >> 8) & 0xFF)
    
    def init(self, mode):
        
        self.reset()
         
        self.send_command(0x12)  #SWRESET
        self.ReadBusy()
        
        self.send_command(0x11)
        self.send_data(0x03)
        
        self.SetWindow(8, 0, self.width, self.height)
   
        if(mode == 0):
            self.send_command(0x3c)
            self.send_data(0x01)
        elif(mode == 1):
            self.SendLut()
            self.send_command(0x37) # set display option, these setting turn on previous function
            self.send_data(0x00)
            self.send_data(0x00)
            self.send_data(0x00)
            self.send_data(0x00)
            self.send_data(0x00)  
            self.send_data(0x40)
            self.send_data(0x00)
            self.send_data(0x00)
            self.send_data(0x00)
            self.send_data(0x00)

            self.send_command(0x3C)
            self.send_data(0x80)

            self.send_command(0x22)
            self.send_data(0xcf)
            
            self.send_command(0x20)
            self.ReadBusy()
            
        else: 
            print("There is no such mode")
    
    def display(self, image):
        if (image == None):
            return            
            
        self.SetCursor(1, 295)
        
        self.send_command(0x24) # WRITE_RAM
        self.send_data1(image)
        self.TurnOnDisplay()
        
    def display_Landscape(self, image):
        if(self.width % 8 == 0):
            Width = self.width // 8
        else:
            Width = self.width // 8 +1
        Height = self.height
        
        self.SetCursor(1, 295)
        
        self.send_command(0x24)
        for j in range(Height):
            for i in range(Width):
                self.send_data(image[(Width-i-1) * Height + j])
                
        self.TurnOnDisplay()
    
    def Clear(self, color):
        self.send_command(0x24) # WRITE_RAM
        self.send_data1([color] * self.height * int(self.width / 8))
        self.TurnOnDisplay()
    
    def sleep(self):
        self.send_command(0x10) # DEEP_SLEEP_MODE
        self.send_data(0x01)





if __name__=='__main__':
    epd = EPD_2in66()
#     epd.Clear(0xff)
#     
#     epd.image_Portrait.fill(0xff)
#     epd.image_Portrait.text("Waveshare", 13, 10, 0x00)
#     epd.image_Portrait.text("Pico_ePaper-2.66", 13, 40, 0x00)
#     epd.image_Portrait.text("Raspberry Pico", 13, 70, 0x00)
#     epd.display(epd.buffer_Portrait)
#     utime.sleep_ms(2000)
#     
#     epd.image_Portrait.vline(10, 90, 60, 0x00)
#     epd.image_Portrait.vline(140, 90, 60, 0x00)
#     epd.image_Portrait.hline(10, 90, 130, 0x00)
#     epd.image_Portrait.hline(10, 150, 130, 0x00)
#     epd.image_Portrait.line(10, 90, 140, 150, 0x00)
#     epd.image_Portrait.line(140, 90, 10, 150, 0x00)
#     epd.display(epd.buffer_Portrait)
#     utime.sleep_ms(2000)
#     
#     epd.image_Portrait.rect(10, 180, 60, 80, 0x00)
#     epd.image_Portrait.fill_rect(80, 180, 60, 80, 0x00)
#     epd.display(epd.buffer_Portrait)
#     utime.sleep_ms(2000)
#     
#     epd.init(1)
#     for i in range(0, 10):
#         epd.image_Portrait.fill_rect(52, 270, 40, 20, 0xff)
#         epd.image_Portrait.text(str(i), 72, 270, 0x00)
#         epd.display(epd.buffer_Portrait)
#         
#     epd.Clear(0xff)
    epd.image_Landscape.fill(0xff)
    epd.image_Landscape.text("Waveshare", 13, 10, 0x00)
    epd.image_Landscape.text("Pico_ePaper-2.66", 13, 40, 0x00)
    epd.image_Landscape.text("Raspberry Pico", 13, 70, 0x00)
    epd.display_Landscape(epd.buffer_Landscape)
    utime.sleep_ms(2000)

    epd.init(0)
    epd.Clear(0xff)
    utime.sleep_ms(2000)
    print("sleep")
    epd.sleep()



