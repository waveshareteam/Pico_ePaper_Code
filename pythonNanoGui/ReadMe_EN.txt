Quick use
Rev0.1



1. Upload demos/ drivers/ gui/ and color_setup.py to RPi Pico


2. Open color_setup.py and uncomment the module import of the corresponding model
    1) Let's say you're using Pico-ePaper-2.13
        will
        # from drivers.ePaper2in13V3 import EPD as SSD
        Change to
        from drivers.ePaper2in13V3 import EPD as SSD

    2) Let's say you're using Pico-ePaper-7.5-B
        will
        # from drivers.ePaper7in5b import EPD as SSD
        # from drivers.ePaper7in5b import EPDred as SSDred
        # ssdred = SSDred(spi, pcs, pdc, prst, pbusy, landscape=False)  # Cread a red display instance (just for B model)
        Change to
        from drivers.ePaper7in5b import EPD as SSD
        from drivers.ePaper7in5b import EPDred as SSDred
        ssdred = SSDred(spi, pcs, pdc, prst, pbusy, landscape=False)  # Cread a red display instance (just for B model)


3. Open the program
    Black and white:
        demos/ePaper_test.py
    Three colors:
        demos/ePaper_test_B.py


4. Run the program