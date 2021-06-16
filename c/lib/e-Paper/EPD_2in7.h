/*****************************************************************************
* | File      	:   EPD_2in7.h
* | Author      :   Waveshare team
* | Function    :   2.9inch e-paper V2
* | Info        :
*----------------
* |	This version:   V1.0
* | Date        :   2021-06-03
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
#ifndef __EPD_2IN7_H_
#define __EPD_2IN7_H_

#include "DEV_Config.h"

// Display resolution
#define EPD_2IN7_WIDTH       176
#define EPD_2IN7_HEIGHT      264 //46464

#define KEY0      15
#define KEY1      17
#define KEY2      2

void EPD_2IN7_Init(void);
void EPD_2IN7_Clear(void);
void EPD_2IN7_Display(const UBYTE *Image);
void EPD_2IN7_Sleep(void);

void EPD_2IN7_Init_4Gray(void);
void EPD_2IN7_4GrayDisplay(const UBYTE *Image);
#endif
