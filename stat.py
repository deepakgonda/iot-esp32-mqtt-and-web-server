import esp32
import gc
import machine

def print_stat():
    print('======================================')
    print('Free Memoory:', gc.mem_free())
    print('Aloc Memoory:', gc.mem_alloc())
    print('Frequency:', machine.freq())
    print('Internal MCU Temp:', esp32.raw_temperature(), "F")
    print()