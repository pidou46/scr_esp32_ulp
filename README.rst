TODO:

#def configure()
#configure scr_ulp.S from template scr_ulp_tpl.S
#map channel and TOUCH_PAD# from gpio

#def assemble()
#assemble scr_ulp.ulp from scr_ulp.S
#get offset of global symbols from assemble function
#open an issue for assemble() function to return offset
#in addition to print it


RTCIO_TOUCH_PAD0_REG = 0x3FF48494 GPIO4
0x94 -> 148

RTCIO_TOUCH_PAD1_REG = 0x3FF48498 GPIO0
0x98 -> 152

RTCIO_TOUCH_PAD2_REG = 0x3FF4849C GPIO2
0x9c -> 156

RTCIO_TOUCH_PAD3_REG = 0x3FF484A0 GPIO15
0xa0 -> 160

RTCIO_TOUCH_PAD4_REG = 0x3FF484A4 GPIO13
0xa4 -> 164

RTCIO_TOUCH_PAD5_REG = 0x3FF484A8 GPIO12
0xa8 -> 168

RTCIO_TOUCH_PAD6_REG = 0x3FF484AC GPIO14
0xac -> 172

RTCIO_TOUCH_PAD7_REG = 0x3FF484B0 GPIO27
0xb0 -> 176

RTCIO_TOUCH_PAD8_REG = 0x3FF484B4 GPIO33
0xb4 -> 180

RTCIO_TOUCH_PAD9_REG = 0x3FF484B8 GPIO32
0xb8 -> 184
