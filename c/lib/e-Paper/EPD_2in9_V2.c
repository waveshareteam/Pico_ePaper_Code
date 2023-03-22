/*****************************************************************************
* | File      	:  	EPD_2in9_V2.c
* | Author      :   Waveshare team
* | Function    :   2.9inch e-paper V2
* | Info        :
*----------------
* |	This version:   V1.0
* | Date        :   2020-10-20
* | Info        :
* -----------------------------------------------------------------------------
#
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
******************************************************************************/
#include "EPD_2in9_V2.h"
#include "Debug.h"


// The chip that drives the display is an SSD1680

// This is based on the waveforms for driving the 3.7 inch display
UBYTE _WF_4GREY_2IN9[159] =
{
0b00101010, 0b00000110, 0b00010101, 0, 0, 0, 0, 0, 0, 0, 0, 0, // LUT 0
0b00101000, 0b00000110, 0b00010100, 0, 0, 0, 0, 0, 0, 0, 0, 0, // LUT 1
0b00100000, 0b00000110, 0b00010000, 0, 0, 0, 0, 0, 0, 0, 0, 0, // LUT 2
0b00010100, 0b00000110, 0b00101000, 0, 0, 0, 0, 0, 0, 0, 0, 0, // LUT 3
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // LUT 4
//TP[A]
//  TP[B]
//      SR[AB]
//          TB[C]
//              TB[D]
//                  SR[CD]
//                      RP
0,  2,  0,  2, 10,  0,  0, // Group 0
0,  0,  0,  8,  8,  0,  2, // Group 1
0,  2,  0,  2, 10,  0,  0, // Group 2
0,  0,  0,  0,  0,  0,  0, // Group 3
0,  0,  0,  0,  0,  0,  0, // Group 4
0,  0,  0,  0,  0,  0,  0, // Group 5
0,  0,  0,  0,  0,  0,  0, // Group 6
0,  0,  0,  0,  0,  0,  0, // Group 7
0,  0,  0,  0,  0,  0,  0, // Group 8
0,  0,  0,  0,  0,  0,  0, // Group 9
0,  0,  0,  0,  0,  0,  0, // Group 11
0,  0,  0,  0,  0,  0,  0, // Group 12

0x22,0x22,0x22,0x22,0x22,0x22, // Framerates (FR[0] to FR[11])
0, 0, 0, // Gate scan selection (XON)
0x22, // EOPT = Normal
0x17, // VGH  = 20 V
0x41, // VSH1 = 15 V
0xB0, // VSH2 = 5.8 V
0x32, // VSL  = -15 V
0x36, // VCOM = -1.3 to -1.4 (not shown on datasheet)
};

UBYTE _WF_PARTIAL_2IN9[159] =
{
0,          0b01000000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // LUT 0 (black to black)
0b10000000, 0b10000000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // LUT 1 (black to white)
0b01000000, 0b01000000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // LUT 2 (white to black)
0,          0b10000000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // LUT 3 (white to white)
0,          0,          0, 0, 0, 0, 0, 0, 0, 0, 0, 0, // LUT 4
//TP[A]
//  TP[B]
//      SR[AB]
//          TB[C]
//              TB[D]
//                  SR[CD]
//                      RP
10, 0,  0,  0,  0,  0,  2, // Group 0
1,  0,  0,  0,  0,  0,  0, // Group 1
1,  0,  0,  0,  0,  0,  0, // Group 2
0,  0,  0,  0,  0,  0,  0, // Group 3
0,  0,  0,  0,  0,  0,  0, // Group 4
0,  0,  0,  0,  0,  0,  0, // Group 5
0,  0,  0,  0,  0,  0,  0, // Group 6
0,  0,  0,  0,  0,  0,  0, // Group 7
0,  0,  0,  0,  0,  0,  0, // Group 8
0,  0,  0,  0,  0,  0,  0, // Group 9
0,  0,  0,  0,  0,  0,  0, // Group 11
0,  0,  0,  0,  0,  0,  0, // Group 12

0x22,0x22,0x22,0x22,0x22,0x22, // Framerates (FR[0] to FR[11])
0, 0, 0, // Gate scan selection (XON)
0x22, // EOPT = Normal
0x17, // VGH  = 20 V
0x41, // VSH1 = 15 V
0xB0, // VSH2 = 5.8 V
0x32, // VSL  = -15 V
0x36, // VCOM = -1.3 to -1.4 (not shown on datasheet)
};

UBYTE WS_20_30[159] =
{
//   0           1      2  3  4  5  6  7       8      9 10 11
0b10000000, 0b01100110, 0, 0, 0, 0, 0, 0, 0b01000000, 0, 0, 0, // LUT 0 (black to black)
0b00010000, 0b01100110, 0, 0, 0, 0, 0, 0, 0b00100000, 0, 0, 0, // LUT 1 (black to white)
0b10000000, 0b01100110, 0, 0, 0, 0, 0, 0, 0b01000000, 0, 0, 0, // LUT 2 (white to black)
0b00010000, 0b01100110, 0, 0, 0, 0, 0, 0, 0b00100000, 0, 0, 0, // LUT 3 (white to white)
0,          0,          0, 0, 0, 0, 0, 0, 0,          0, 0, 0, // LUT 4
//TP[A]
//  TP[B]
//      SR[AB]
//          TB[C]
//              TB[D]
//                  SR[CD]
//                      RP
20, 8,  0,  0,  0,  0,  1, // Group 0
10, 10, 0,  10, 10, 0,  1, // Group 1
0,  0,  0,  0,  0,  0,  0, // Group 2
0,  0,  0,  0,  0,  0,  0, // Group 3
0,  0,  0,  0,  0,  0,  0, // Group 4
0,  0,  0,  0,  0,  0,  0, // Group 5
0,  0,  0,  0,  0,  0,  0, // Group 6
0,  0,  0,  0,  0,  0,  0, // Group 7
20, 8,  0,  1,  0,  0,  1, // Group 8
0,  0,  0,  0,  0,  0,  1, // Group 9
0,  0,  0,  0,  0,  0,  0, // Group 11
0,  0,  0,  0,  0,  0,  0, // Group 12
0x44, 0x44, 0x44, 0x44, 0x44, 0x44, // Framerates (FR[0] to FR[11])
0, 0, 0, // Gate scan selection (XON)
0x22, // EOPT = Normal
0x17, // VGH  = 20V
0x41, // VSH1 = 15 V
0,    // VSH2 = Unknown
0x32, // VSL  = -15 V
0x36, // VCOM = -1.3 to -1.4 (not shown on datasheet)
};

/******************************************************************************
function :	Software reset
parameter:
******************************************************************************/
static void EPD_2IN9_V2_Reset(void)
{
    DEV_Digital_Write(EPD_RST_PIN, 1);
    DEV_Delay_ms(20);
    DEV_Digital_Write(EPD_RST_PIN, 0);
    DEV_Delay_ms(1);
    DEV_Digital_Write(EPD_RST_PIN, 1);
    DEV_Delay_ms(20);
}

/******************************************************************************
function :	send command
parameter:
     Reg : Command register
******************************************************************************/
static void EPD_2IN9_V2_SendCommand(UBYTE Reg)
{
    DEV_Digital_Write(EPD_DC_PIN, 0);
    DEV_Digital_Write(EPD_CS_PIN, 0);
    DEV_SPI_WriteByte(Reg);
    DEV_Digital_Write(EPD_CS_PIN, 1);
}

/******************************************************************************
function :	send data
parameter:
    Data : Write data
******************************************************************************/
static void EPD_2IN9_V2_SendData(UBYTE Data)
{
    DEV_Digital_Write(EPD_DC_PIN, 1);
    DEV_Digital_Write(EPD_CS_PIN, 0);
    DEV_SPI_WriteByte(Data);
    DEV_Digital_Write(EPD_CS_PIN, 1);
}

/******************************************************************************
function :	Wait until the busy_pin goes LOW
parameter:
******************************************************************************/
void EPD_2IN9_V2_ReadBusy(void)
{
    Debug("e-Paper busy\r\n");
	while(1)
	{	 //=1 BUSY
		if(DEV_Digital_Read(EPD_BUSY_PIN)==0)
			break;
		DEV_Delay_ms(50);
	}
	DEV_Delay_ms(50);
    Debug("e-Paper busy release\r\n");
}

static void EPD_2IN9_V2_LUT(UBYTE *lut)
{
	UBYTE count;
	EPD_2IN9_V2_SendCommand(0x32); // Write LUT Register
	for(count=0; count<153; count++)
		EPD_2IN9_V2_SendData(lut[count]);
	EPD_2IN9_V2_ReadBusy();
}

static void EPD_2IN9_V2_LUT_by_host(UBYTE *lut)
{
	EPD_2IN9_V2_LUT((UBYTE *)lut);			//lut
	EPD_2IN9_V2_SendCommand(0x3f);
	EPD_2IN9_V2_SendData(*(lut+153));
	EPD_2IN9_V2_SendCommand(0x03);	// gate voltage
	EPD_2IN9_V2_SendData(*(lut+154));
	EPD_2IN9_V2_SendCommand(0x04);	// source voltage
	EPD_2IN9_V2_SendData(*(lut+155));	// VSH
	EPD_2IN9_V2_SendData(*(lut+156));	// VSH2
	EPD_2IN9_V2_SendData(*(lut+157));	// VSL
	EPD_2IN9_V2_SendCommand(0x2c);		// VCOM
	EPD_2IN9_V2_SendData(*(lut+158));
	
}

/******************************************************************************
function :	Turn On Display
parameter:
******************************************************************************/
static void EPD_2IN9_V2_TurnOnDisplay(void)
{
	EPD_2IN9_V2_SendCommand(0x22); // Display Update Control 2
	EPD_2IN9_V2_SendData(0xC7); // Display mode 1
	EPD_2IN9_V2_SendCommand(0x20); // Master Activation
	EPD_2IN9_V2_ReadBusy();
}

static void EPD_2IN9_V2_TurnOnDisplay_Partial(void)
{
	EPD_2IN9_V2_SendCommand(0x22); // Display Update Control 2
	EPD_2IN9_V2_SendData(0x0F); // Display mode 2
	EPD_2IN9_V2_SendCommand(0x20); // Master Activation
	EPD_2IN9_V2_ReadBusy();
}

static void EPD_2IN9_V2_TurnOnDisplay_4Grey(void)
{
    EPD_2IN9_V2_SendCommand(0x22); // Display Update Control 2
    EPD_2IN9_V2_SendData(0xCF); // Display mode 2
    EPD_2IN9_V2_SendCommand(0x20); // Master Activation
    EPD_2IN9_V2_ReadBusy();
}

/******************************************************************************
function :	Setting the display window
parameter:
******************************************************************************/
static void EPD_2IN9_V2_SetWindows(UWORD Xstart, UWORD Ystart, UWORD Xend, UWORD Yend)
{
    EPD_2IN9_V2_SendCommand(0x44); // Set RAM X Address Start/End
    EPD_2IN9_V2_SendData((Xstart>>3) & 0xFF);
    EPD_2IN9_V2_SendData((Xend>>3) & 0xFF);

    EPD_2IN9_V2_SendCommand(0x45); // Set RAM Y Address Start/End
    EPD_2IN9_V2_SendData(Ystart & 0xFF);
    EPD_2IN9_V2_SendData((Ystart >> 8) & 0xFF);
    EPD_2IN9_V2_SendData(Yend & 0xFF);
    EPD_2IN9_V2_SendData((Yend >> 8) & 0xFF);
}

/******************************************************************************
function :	Set Cursor
parameter:
******************************************************************************/
static void EPD_2IN9_V2_SetCursor(UWORD Xstart, UWORD Ystart)
{
    EPD_2IN9_V2_SendCommand(0x4E); // Set RAM X Address Counter
    EPD_2IN9_V2_SendData(Xstart & 0xFF);

    EPD_2IN9_V2_SendCommand(0x4F); // Set RAM Y Address Counter
    EPD_2IN9_V2_SendData(Ystart & 0xFF);
    EPD_2IN9_V2_SendData((Ystart >> 8) & 0xFF);
}

/******************************************************************************
function :	Initialize the e-Paper register
parameter:
******************************************************************************/
void EPD_2IN9_V2_Init(void)
{
	EPD_2IN9_V2_Reset();
	DEV_Delay_ms(100);

	EPD_2IN9_V2_ReadBusy();
	EPD_2IN9_V2_SendCommand(0x12); // SW Reset
	EPD_2IN9_V2_ReadBusy();

	EPD_2IN9_V2_SendCommand(0x01); // Driver Output Control
	EPD_2IN9_V2_SendData(0x27);
	EPD_2IN9_V2_SendData(0x01);
	EPD_2IN9_V2_SendData(0x00);

	EPD_2IN9_V2_SendCommand(0x11); // Data Entry Mode Setting
	EPD_2IN9_V2_SendData(0x03);

	EPD_2IN9_V2_SetWindows(0, 0, EPD_2IN9_V2_WIDTH-1, EPD_2IN9_V2_HEIGHT-1);

	EPD_2IN9_V2_SendCommand(0x21); // Display Update Control 1
	EPD_2IN9_V2_SendData(0x00);
	EPD_2IN9_V2_SendData(0x80);

	EPD_2IN9_V2_SetCursor(0, 0);
	EPD_2IN9_V2_ReadBusy();

	EPD_2IN9_V2_LUT_by_host(WS_20_30);
}

/******************************************************************************
function :	Clear screen
parameter:
******************************************************************************/
void EPD_2IN9_V2_Clear(void)
{
	UWORD i;
	EPD_2IN9_V2_SendCommand(0x24); // Write RAM (B/W)
	for(i=0;i<4736;i++)
	{
		EPD_2IN9_V2_SendData(0xff);
	}
	EPD_2IN9_V2_TurnOnDisplay();
}

/******************************************************************************
function :	Sends the image buffer in RAM to e-Paper and displays
parameter:
******************************************************************************/
void EPD_2IN9_V2_Display(UBYTE *Image)
{
	UWORD i;	
	EPD_2IN9_V2_SendCommand(0x24); // Write RAM (B/W)
	for(i=0;i<4736;i++)
	{
		EPD_2IN9_V2_SendData(Image[i]);
	}
	EPD_2IN9_V2_TurnOnDisplay();
}

void EPD_2IN9_V2_Display_Base(UBYTE *Image)
{
	UWORD i;

	EPD_2IN9_V2_SendCommand(0x24); // Write RAM (B/W)
	for(i=0;i<4736;i++)
	{
		EPD_2IN9_V2_SendData(Image[i]);
	}
	EPD_2IN9_V2_SendCommand(0x26); // Write RAM (RED)
	for(i=0;i<4736;i++)
	{
		EPD_2IN9_V2_SendData(Image[i]);
	}
	EPD_2IN9_V2_TurnOnDisplay();
}

void EPD_2IN9_V2_Display_Partial(UBYTE *Image)
{
	UWORD i;

//Reset
    DEV_Digital_Write(EPD_RST_PIN, 0);
    DEV_Delay_ms(1);
    DEV_Digital_Write(EPD_RST_PIN, 1);
    DEV_Delay_ms(2);

	EPD_2IN9_V2_LUT(_WF_PARTIAL_2IN9);
	EPD_2IN9_V2_SendCommand(0x37); // Write Register for Display Option
	EPD_2IN9_V2_SendData(0x00); // Default VCOM OTP
	EPD_2IN9_V2_SendData(0x00); // WS[7:0]
	EPD_2IN9_V2_SendData(0x00); // WS[15:8]
	EPD_2IN9_V2_SendData(0x00); // WS[23:16] Display modes are set to 1
	EPD_2IN9_V2_SendData(0x00); // WS[31:24]
	EPD_2IN9_V2_SendData(0x40); // Ping Pong enable for display mode 2
	EPD_2IN9_V2_SendData(0x00); // Module id / waveform version is 0
	EPD_2IN9_V2_SendData(0x00);
	EPD_2IN9_V2_SendData(0x00);
	EPD_2IN9_V2_SendData(0x00);

	EPD_2IN9_V2_SendCommand(0x3C); // Border Waveform Control
	EPD_2IN9_V2_SendData(0x80);

	EPD_2IN9_V2_SendCommand(0x22); // Display Update Control 2
	EPD_2IN9_V2_SendData(0xC0);
	EPD_2IN9_V2_SendCommand(0x20); // Master Activation
	EPD_2IN9_V2_ReadBusy();

	EPD_2IN9_V2_SetWindows(0, 0, EPD_2IN9_V2_WIDTH-1, EPD_2IN9_V2_HEIGHT-1);
	EPD_2IN9_V2_SetCursor(0, 0);

	EPD_2IN9_V2_SendCommand(0x24); // Write RAM (B/W)
	for(i=0;i<4736;i++)
	{
		EPD_2IN9_V2_SendData(Image[i]);
	}
	EPD_2IN9_V2_TurnOnDisplay_Partial();
}

void EPD_2IN9_V2_Display_4grey(UBYTE *Image)
{
    UWORD i,j,k;
    UBYTE imgByte,currPix,value;

    // Reset
    DEV_Digital_Write(EPD_RST_PIN, 0);
    DEV_Delay_ms(5);
    DEV_Digital_Write(EPD_RST_PIN, 1);
    DEV_Delay_ms(10);

    EPD_2IN9_V2_LUT(_WF_4GREY_2IN9);

    EPD_2IN9_V2_SendCommand(0x3C); // Border Waveform Control
    EPD_2IN9_V2_SendData(0x80);

    EPD_2IN9_V2_SetWindows(0, 0, EPD_2IN9_V2_WIDTH-1, EPD_2IN9_V2_HEIGHT-1);
    EPD_2IN9_V2_SetCursor(0, 0);

    EPD_2IN9_V2_SendCommand(0x24); // Write RAM (B/W)
    for (i = 0;i < 4736;i ++)
    {
        // Fine layer (0 is darker)
        value = 0;
        for (j = 0; j < 2; j ++) {
            imgByte = Image[i * 2 + j];
            for (k = 0; k < 4; k ++) {
                // Take the current pixel
                currPix = imgByte & 0b11000000;
                if (currPix == 0b11000000 || // White (GRAY1)
                    currPix == 0b01000000)   // GREY3
                    value |= 1;

                if (j!=1 || k!=3)
                    value <<= 1;

                imgByte <<= 2;
            }
        }
        EPD_2IN9_V2_SendData(value);
    }

    EPD_2IN9_V2_SendCommand(0x26); // Write RAM (RED)
    for (i = 0;i < 4736;i ++)
    {
        // Coarse layer (0 is darker)
        value = 0;
        for (j = 0; j < 2; j ++) {
            imgByte = Image[i * 2 + j];
            for (k = 0; k < 4; k ++) {
                // Take the current pixel
                currPix = imgByte & 0b11000000;
                if (currPix == 0b11000000 || // White (GRAY1)
                    currPix == 0b10000000)   // GREY2
                    value |= 1;

                if (j!=1 || k!=3)
                    value <<= 1;

                imgByte <<= 2;
            }
        }
        EPD_2IN9_V2_SendData(value);
    }

    EPD_2IN9_V2_TurnOnDisplay_4Grey();
}

/******************************************************************************
function :	Enter sleep mode
parameter:
******************************************************************************/
void EPD_2IN9_V2_Sleep(void)
{
	EPD_2IN9_V2_SendCommand(0x10); // Deep Sleep Mode
	EPD_2IN9_V2_SendData(0x01);
	DEV_Delay_ms(100);
}
