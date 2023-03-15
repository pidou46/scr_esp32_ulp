#define DR_REG_RTCIO_BASE            0x3ff48400

#define RTC_IO_TOUCH_PAD{pad_in}_REG        (DR_REG_RTCIO_BASE + 0x94)
#define RTC_IO_TOUCH_PAD{pad_in}_MUX_SEL_M  (BIT(19))
#define RTC_IO_TOUCH_PAD{pad_in}_FUN_IE_M   (BIT(13))
#define RTC_IO_TOUCH_PAD{pad_in}_RDE_M      (BIT(28))
#define RTC_GPIO_IN_REG              (DR_REG_RTCIO_BASE + 0x24)
#define RTC_GPIO_IN_NEXT_S           14
.set gpio_in, {channel_in}  # set by assemble_ulp.py


#define RTC_IO_TOUCH_PAD{pad_out}_REG        (DR_REG_RTCIO_BASE + 0x9c)
#define RTC_IO_TOUCH_PAD{pad_out}_MUX_SEL_M  (BIT(19))
#define RTC_GPIO_OUT_REG             (DR_REG_RTCIO_BASE + 0x0)
#define RTC_GPIO_ENABLE_REG          (DR_REG_RTCIO_BASE + 0xc)
#define RTC_GPIO_ENABLE_S            14
#define RTC_GPIO_OUT_DATA_S          14
.set gpio_out, {channel_out} # set by assemble_ulp.py


            .global setpoint  // make setpoint accessible from main python code
setpoint:   .long 0

entry:
            # WRITE_RTC_REG(rtc_reg, low_bit, bit_width, value)
            # connect GPIO to the RTC subsystem so the ULP can read it
            WRITE_RTC_REG(RTC_IO_TOUCH_PAD0_REG, RTC_IO_TOUCH_PAD{pad_in}_MUX_SEL_M, 1, 0)

            # switch the GPIO into input mode
            WRITE_RTC_REG(RTC_IO_TOUCH_PAD{pad_in}_REG, RTC_IO_TOUCH_PAD{pad_in}_FUN_IE_M, 1, 1)

            # switch the GPIO into input mode
            WRITE_RTC_REG(RTC_IO_TOUCH_PAD{pad_in}_REG, RTC_IO_TOUCH_PAD{pad_in}_RDE_M, 1, 1)

            # connect GPIO to ULP (0: GPIO connected to digital GPIO module, 1: GPIO connected to analog RTC module)
            WRITE_RTC_REG(RTC_IO_TOUCH_PAD{pad_out}_REG, RTC_IO_TOUCH_PAD{pad_out}_MUX_SEL_M, 1, 1);

            # GPIO shall be output, not input (this also enables a pull-down by default)
            WRITE_RTC_REG(RTC_GPIO_ENABLE_REG, RTC_GPIO_ENABLE_S + gpio_out, 1, 1)     

            jump edge_detect

edge_detect:

            # detect rising and falling edges on gpio_in (cross zero signal from scr)
            
            #init r3
            move r3, 0
            
            # read the GPIO's current setpoint into r0
            READ_RTC_REG(RTC_GPIO_IN_REG, RTC_GPIO_IN_NEXT_S + gpio_in, 1)

            #move gpio_in state in R1
            move r1, r0

            # add previous state with current state, then substarct 1
            # if setpoint of previous and current change result will be zero
            add r3, r1, r2
            
            #store setpoint for next iteration
            move r2, r1

            sub r0, r3, 1

            #jump to toggle if last ALU op result is zero : gpio_in setpoint is 1 
            jump delay_setup, EQ
            
            jump edge_detect


delay_setup:
            # setup the delay value get from main python script
            
            move r0, setpoint   //r0 <- address of setpoint
            ld r0, r0, 0     //r0 <- value of setpoint value

            jumpr limit, 12, LT //avoid gliches close to 100%

            jumpr edge_detect, 93, GT //avoid gliches close to 0%

            jump delay
            
limit:
            move r0, 12
            
            jump delay
            
            
delay:
            # the wait instruction does not accept register value
            # so implementing a loop allow to dynamically adjust delay
            sub R0,R0,1

            wait {delay} # 1% of half period, set by assemble_ulp.py script 850 - 50Hz | 708 - 60Hz
            
            jumpr delay, 2, GT //get out of the loop when 2 is greater than r0
            
            jump toggle

toggle:
            # toggle gpio_out on and off after some delay to triger scr's thyristor
            
            # set gpio_out to 1 (set GPIO)
            WRITE_RTC_REG(RTC_GPIO_OUT_REG, RTC_GPIO_OUT_DATA_S + gpio_out, 1, 1)
            
            WAIT 500 // duration of the square signal
            
            # set gpio_out to 0 (clear GPIO)
            WRITE_RTC_REG(RTC_GPIO_OUT_REG, RTC_GPIO_OUT_DATA_S + gpio_out, 1, 0)

            #jump back to main loop
            jump edge_detect