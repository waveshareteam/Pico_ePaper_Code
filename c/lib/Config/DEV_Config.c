/*****************************************************************************
* | File      	:   DEV_Config.c
* | Author      :   Waveshare team
* | Function    :   Hardware underlying interface
* | Info        :
*----------------
* |	This version:   V3.0
* | Date        :   2019-07-31
* | Info        :   
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of theex Software, and to permit persons to  whom the Software is
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
#include "DEV_Config.h"

#define SPI_PORT spi1

/**
 * GPIO
**/
int EPD_RST_PIN;
int EPD_DC_PIN;
int EPD_CS_PIN;
int EPD_BUSY_PIN;
int EPD_CLK_PIN;
int EPD_MOSI_PIN;

/**
 * GPIO read and write
**/
void DEV_Digital_Write(UWORD Pin, UBYTE Value)
{
	gpio_put(Pin, Value);
}

UBYTE DEV_Digital_Read(UWORD Pin)
{
	return gpio_get(Pin);
}

/**
 * SPI
**/
void DEV_SPI_WriteByte(uint8_t Value)
{
    spi_write_blocking(SPI_PORT, &Value, 1);
}

void DEV_SPI_Write_nByte(uint8_t *pData, uint32_t Len)
{
    spi_write_blocking(SPI_PORT, pData, Len);
}

/**
 * GPIO Mode
**/
void DEV_GPIO_Mode(UWORD Pin, UWORD Mode)
{
    gpio_init(Pin);
	if(Mode == 0 || Mode == GPIO_IN) {
		gpio_set_dir(Pin, GPIO_IN);
	} else {
		gpio_set_dir(Pin, GPIO_OUT);
	}
}

/**
 * delay x ms
**/
void DEV_Delay_ms(UDOUBLE xms)
{
	sleep_ms(xms);
}

void DEV_GPIO_Init(void)
{

	EPD_RST_PIN     = 12;
	EPD_DC_PIN      = 8;
	EPD_BUSY_PIN    = 13;
	
	EPD_CS_PIN      = 9;
	EPD_CLK_PIN		= 10;
	EPD_MOSI_PIN	= 11;

	DEV_GPIO_Mode(EPD_RST_PIN, 1);
	DEV_GPIO_Mode(EPD_DC_PIN, 1);
	DEV_GPIO_Mode(EPD_CS_PIN, 1);
	DEV_GPIO_Mode(EPD_BUSY_PIN, 0);

	DEV_Digital_Write(EPD_CS_PIN, 1);
}
/******************************************************************************
function:	Module Initialize, the library and initialize the pins, SPI protocol
parameter:
Info:
******************************************************************************/
UBYTE DEV_Module_Init(void)
{
    stdio_init_all();

	// GPIO Config
	DEV_GPIO_Init();
	
    spi_init(SPI_PORT, 4000 * 1000);
    gpio_set_function(EPD_CLK_PIN, GPIO_OUT);
    gpio_set_function(EPD_MOSI_PIN, GPIO_OUT);
	
    printf("DEV_Module_Init OK \r\n");
	return 0;
}

void DEV_GPIO_Init_1(void)
{
    spi_deinit(SPI_PORT);
    gpio_set_function(EPD_CLK_PIN, GPIO_FUNC_SPI);
    gpio_set_function(EPD_MOSI_PIN, GPIO_FUNC_SPI);
}

void DEV_SPI_Init(void)
{
    spi_init(SPI_PORT, 4000 * 1000);
    gpio_set_function(EPD_CLK_PIN, GPIO_FUNC_SPI);
    gpio_set_function(EPD_MOSI_PIN, GPIO_FUNC_SPI);
}


void DEV_SPI_SendData(UBYTE Reg)
{
	UBYTE i,j=Reg;
	DEV_GPIO_Mode(EPD_MOSI_PIN, 1);
    DEV_GPIO_Mode(EPD_CLK_PIN, 1);
	DEV_Digital_Write(EPD_CS_PIN, 0);
	for(i = 0; i<8; i++)
    {
        DEV_Digital_Write(EPD_CLK_PIN, 0);     
        if (j & 0x80)
        {
            DEV_Digital_Write(EPD_MOSI_PIN, 1);
        }
        else
        {
            DEV_Digital_Write(EPD_MOSI_PIN, 0);
        }
        
        DEV_Digital_Write(EPD_CLK_PIN, 1);
        j = j << 1;
    }
	DEV_Digital_Write(EPD_CLK_PIN, 0);
	DEV_Digital_Write(EPD_CS_PIN, 1);
}

UBYTE DEV_SPI_ReadData(void)
{
	UBYTE i,j=0xff;
	DEV_GPIO_Mode(EPD_MOSI_PIN, 0);
    DEV_GPIO_Mode(EPD_CLK_PIN, 1);
	DEV_Digital_Write(EPD_CS_PIN, 0);
	for(i = 0; i<8; i++)
	{
		DEV_Digital_Write(EPD_CLK_PIN, 0);
		j = j << 1;
		if (DEV_Digital_Read(EPD_MOSI_PIN))
		{
            j = j | 0x01;
		}
		else
		{
            j= j & 0xfe;
		}
		DEV_Digital_Write(EPD_CLK_PIN, 1);
	}
	DEV_Digital_Write(EPD_CLK_PIN, 0);
	DEV_Digital_Write(EPD_CS_PIN, 1);
	return j;
}


/******************************************************************************
function:	Module exits, closes SPI and BCM2835 library
parameter:
Info:
******************************************************************************/
void DEV_Module_Exit(void)
{

}
