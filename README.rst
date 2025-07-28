configure scr_ulp.S from template scr_ulp_tpl.S
map rtcio channel and TOUCH_PAD number from gpio
assemble scr_ulp.ulp from scr_ulp.S


Warning considering pin limitations: 
https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/gpio.html

I would recommend:

- GPIO34 to GPIO39 for input
- GPIO32-GPIO33 for output

If two pins are not sufficient for output, GPIO25-GPIO27 can be added if not using wifi

todo: open an issue for assemble() function to return offset in addition to print it. This would ease automation.

ESP32 (not S2 nor S3 or C3)

DR_REG_RTCIO_BASE 0x3ff48400

GPIO4 - RTCGPIO10 - RTCIO_TOUCH_PAD0_REG = 0x3FF48494 
0x94 -> 148

GPIO0 - RTCGPIO11 - RTCIO_TOUCH_PAD1_REG = 0x3FF48498 
0x98 -> 152

GPIO2 - RTCGPIO12 - RTCIO_TOUCH_PAD2_REG = 0x3FF4849C 
0x9c -> 156

GPIO15 - RTCGPIO13 - RTCIO_TOUCH_PAD3_REG = 0x3FF484A0 
0xa0 -> 160

GPIO13 - RTCGPIO14 - RTCIO_TOUCH_PAD4_REG = 0x3FF484A4 
0xa4 -> 164

GPIO12 - RTCGPIO15 - RTCIO_TOUCH_PAD5_REG = 0x3FF484A8 
0xa8 -> 168

GPIO14 - RTCGPIO16 - RTCIO_TOUCH_PAD6_REG = 0x3FF484AC 
0xac -> 172

GPIO27 - RTCGPIO17 - RTCIO_TOUCH_PAD7_REG = 0x3FF484B0 
0xb0 -> 176

GPIO33 - RTCGPIO8 - RTCIO_TOUCH_PAD8_REG = 0x3FF484B4 
0xb4 -> 180

GPIO32 - RTCGPIO9 - RTCIO_TOUCH_PAD9_REG = 0x3FF484B8 
0xb8 -> 184
