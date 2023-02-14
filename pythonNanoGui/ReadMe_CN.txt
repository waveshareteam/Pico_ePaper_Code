快速使用
Rev0.1



1. 将 demos/ drivers/ gui/ 和 color_setup.py 上传到 RPi Pico 中


2. 打开 color_setup.py, 将对应型号的模块导入注释取消
    1) 例如你使用的是 Pico-ePaper-2.13
        将
        # from drivers.ePaper2in13V3 import EPD as SSD
        改为
        from drivers.ePaper2in13V3 import EPD as SSD

    2) 例如你使用的是 Pico-ePaper-7.5-B
        将
        # from drivers.ePaper7in5b import EPD as SSD
        # from drivers.ePaper7in5b import EPDred as SSDred
        # ssdred = SSDred(spi, pcs, pdc, prst, pbusy, landscape=False)  # Cread a red display instance (just for B model)
        改为
        from drivers.ePaper7in5b import EPD as SSD
        from drivers.ePaper7in5b import EPDred as SSDred
        ssdred = SSDred(spi, pcs, pdc, prst, pbusy, landscape=False)  # Cread a red display instance (just for B model)


3. 打开程序
    黑白： 
        demos/ePaper_test.py 
    三色：
        demos/ePaper_test_B.py


4. 运行程序