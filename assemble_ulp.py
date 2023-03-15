import esp32_ulp
import gc

'''modify both the channel number and also the RTC_IO_TOUCH_PAD0_* references appropriately.
The best place to see the mappings might be this table here (notice the "real GPIO numbers" as
comments to each line):
https://github.com/espressif/esp-idf/blob/v4.4.1/components/soc/esp32/rtc_io_periph.c#L61'''


CHANNELS={4:10,0:11,2:12,15:13,13:14,12:15,14:16,27:17}
PADS={4:0,0:1,2:2,15:3,13:4,12:5,14:6,27:7}
DELAYS={50:850,60:708}

def config(gpio_in=4,gpio_out=2,freq=50):
    '''configure ulp source code from template by
    changing gpio channel and pad'''
    try:
        with open('scr_ulp.S','w') as output:
            with open('scr_ulp_tpl.S','r') as template:
                for line in template:
                    line = line.replace('{channel_in}',str(CHANNELS[gpio_in]))
                    line = line.replace('{channel_out}',str(CHANNELS[gpio_out]))
                    line = line.replace('{pad_in}',str(PADS[gpio_in]))
                    line = line.replace('{pad_out}',str(PADS[gpio_out]))
                    line = line.replace('{delay}',str(DELAYS[freq]))
                    output.write(line)
    except OSError:
        print("scr_ulp_tlp.S in missing, reinstall")


def assemble():
    try:
         esp32_ulp.assemble_file('scr_ulp.S')  # this results in code.ulp
    except:
        print("error in assembling ulp code")
    

if __name__ == "__main__":
    
    gpio_in=255
    gpio_out=255
    freq=255
    
    pins=list(CHANNELS.keys())
    pins.sort()
    freqs=list(DELAYS.keys())
    while gpio_in not in pins:
        gpio_in=int(input(f"Enter GPIO input pin {pins}:"))
    pins.remove(gpio_in)
    while gpio_out not in pins:
        gpio_out=int(input(f"Enter GPIO output pin {pins}:"))
    while freq not in freqs:
        freq=int(input(f"Enter AC frequency {freqs}:"))

    config(gpio_in,gpio_out,freq)
    gc.collect()
    print(f"free: {gc.mem_free()}")
    assemble()
    gc.collect()
    print(f"free: {gc.mem_free()}")
    

# '''snipet to get offsets of global symbols/label printed by assemble_file function
# as a workaround of a PR to make assemble_file function return a tuple
# '''
# 
# import sys
# class ListStream:
#     def __init__(self):
#         self.data = []
#     def write(self, s):
#         self.data.append(s)
#     def __enter__(self):
#         sys.stdout = self
#         return self
#     def __exit__(self, ext_type, exc_value, traceback):
#         sys.stdout = sys.__stdout__
#         
# def assemble():
#     print("toto 52")
#         
# with ListStream() as x:
#     assemble()
# 
# data=x.data[0].split()
# 
# print(f"{data[0]} {data[1]}")
# '''