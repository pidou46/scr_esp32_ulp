"""
The aim of this code is to drive a SCR (AC curent dimmer) from a esp32 MCU.
This code make use of esp32's ulp assembly code, therfore it is not suitable for
esp32-c3 because it is different from other esp32.

Caution: be careful there is no earth connection on my SCR. The 5V
is generated from phase and neutral tension, which can be any tension
relative to ground. If you plug your micro-controller to your PC via USB cable
you may fry it (like I do!) because your PC USB cable is linked to earth ground.
To avoid this hazard, use a laptop unplugged from wall socket to connect to MCU.

Wiring:
- zero crossing signal from the SCR -> GPIO4.
- output signal to trigger the SCR's tyristor -> GPIO2 

Note that the ULP needs to refer to GPIOs via their RTC channel number.
You can see the mapping in this file:
https://github.com/espressif/esp-idf/blob/v4.4.1/components/soc/esp32/include/soc/rtc_io_channel.h#L51

If you change to a different GPIO number, make sure to modify both the channel
number and also the RTC_IO_TOUCH_PAD0_* references appropriately. The best place
to see the mappings might be this table here (notice the "real GPIO numbers" as
comments to each line):
https://github.com/espressif/esp-idf/blob/v4.4.1/components/soc/esp32/rtc_io_periph.c#L61
"""

from esp32 import ULP
from machine import mem32
from time import sleep
from esp32_ulp import src_to_binary
import gc


ULP_MEM_BASE = 0x50000000
ULP_DATA_MASK = 0xffff  # ULP data is only in lower 16 bits


class SCR:
        
    def __init__(self, gpio_in_nb=4, gpio_out_nb=2, freq=50):
        
        self.f = 'scr_ulp.ulp' #bluid from scr_ulp_tpl.S using assemble_ulp.py
        self.setpt = 0
        self.load_addr = 0
        self.entry_addr = 4
                
        self.ulp = ULP()
        print("Upload binary...")
        
        with open('scr_ulp.ulp', 'r') as f:
            self.ulp.load_binary(self.load_addr, f.read())
            print("Done")

            gc.collect()

            mem32[ULP_MEM_BASE + self.load_addr] = 0x0  # initialise setpoint to 0
        
            self.ulp.run(self.entry_addr)
            gc.collect()
            print("start sending pulses...")

        
    def setpoint(self):
        '''return setpoint current value'''
        return setpt
        
    def setpoint(self, setpoint):
        '''set the setpoint value'''
        mem32[ULP_MEM_BASE + self.load_addr] = setpoint
        self.setpt=setpoint
        
    def power_percent_stp(self, setpoint):
        '''set setpoint by power %'''
        p_setpoint=setpoint
        setpoint=-0.0002421*setpoint**3+0.03519*setpoint**2-1.975*setpoint+96.833 #delay% vs power%
        gc.collect()
        setpoint=int(round(setpoint))
        gc.collect()
        print(f"power: {p_setpoint}%, cutting time: {setpoint:.2f}%")
        self.setpoint(setpoint)
        


    def alive(self):
        ''' check if ulp code is running'''
        
        #TODO: get the pulses count from ulp to check if it work correctly


if __name__=="__main__":
    
    scr=SCR(4,2,50)
    
    sleep(3) #wait until ulp pulse
    
    while True:
        power_percent=input("power percentage:")
        try:
            scr.power_percent_stp(int(power_percent))
        except:
            print("only integer between 0-100")
            
