/*****************************************************************************
* | File      	:   Readme_EN.txt
* | Author      :   Waveshare team
* | Function    :   Help with use
* | Info        :
*----------------
* |	This version:   V1.0
* | Date        :   2021-02-04
* | Info        :   Here is an English version of the documentation for your quick use.
******************************************************************************/
This file is to help you use this routine.
Since our ink screens are getting more and more, it is not convenient for our maintenance, so all the ink screen programs are made into one project.
A brief description of the use of this project is here:

1. Basic information:
This routine is verified using the corresponding module with the PICO. 
You can see the corresponding test routine in the examples\ of the project.

2. Pin connection:
Pin connection You can look at dev_config.c/h in \lib\Config. Again, here:
EPD    =>    Pico
VCC    ->    VSYS
GND    ->    GND
DIN    ->    11
CLK    ->    10
CS     ->    9
DC     ->    8
RST    ->    12
BUSY   ->    13

3. Basic use:
As this project is a comprehensive project, for use, you may need to read the following:
You can see the nine functions that have been commented in main.c on lines 12 through 22,
Please pay attention to which type of ink screen you buy.
eg.1：
    If you purchased pico-epaper 2.13, 
	then you should uncomment the corresponding 18(or 19, depending on the version of your screen) lines of code, i.e. :
		// EPD_2in13_V2_test();
    change to：
		EPD_2in13_V2_test();
eg.2：
    If you bought pico-epaper 2.9-b, 
	then you should uncomment the corresponding 21 lines of code, i.e. :
		// EPD_2in13b_V3_test();
    change to：
		EPD_2in13b_V3_test();
Note: For the version of the screen, please pay attention to whether the back of your screen is labeled with V2/V3 etc.

Then you need to implement:
	Create the build directory: Open the terminal and type in the Pico_ePaper_Code/c directory:
		mkdir build
	Go to the build directory and type:
		cd build
	Execute cmake to automatically generate the Makefile file and type:
		cmake ..
	To create an executable file, type:
		make -j4

4. Directory structure (selection):
If you use our products frequently, we will be very familiar with our program directory structure. We have a copy of the specific function.
The API manual for the function, you can download it on our WIKI or request it as an after-sales customer service. Here is a brief introduction:
Config\: This directory is a hardware interface layer file. You can see many definitions in DEV_Config.c(.h), including:
   type of data;
    GPIO;
    Read and write GPIO;
    Delay: Note: This delay function does not use an oscilloscope to measure specific values.
    Module Init and exit processing:
        void DEV_Module_Init(void);
        void DEV_Module_Exit(void);
        Note: 1. Here is the processing of some GPIOs before and after using the ink screen.
              2. For the PCB with Rev2.1, the entire module will enter low power consumption after DEV_Module_Exit(). After testing, the power consumption is basically 0;
             
\lib\GUI\: This directory is some basic image processing functions, in GUI_Paint.c(.h):
    Common image processing: creating graphics, flipping graphics, mirroring graphics, setting pixels, clearing screens, etc.
    Common drawing processing: drawing points, lines, boxes, circles, Chinese characters, English characters, numbers, etc.;
    Common time display: Provide a common display time function;
    Commonly used display pictures: provide a function to display bitmaps;
    
\lib\Fonts\: for some commonly used fonts:
    Ascii:
        Font8: 5*8
        Font12: 7*12
        Font16: 11*16
        Font20: 14*20
        Font24: 17*24
    Chinese:
        font12CN: 16*21
        font24CN: 32*41
        
\lib\e-paper\: This screen is the ink screen driver function;
examples\: This is the test program for the ink screen. You can see the specific usage method in it.