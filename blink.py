import machine
import time

LED = machine.Pin(2, machine.Pin.OUT)

def do_blink(interval_sec):
    LED.value(1)
    time.sleep(interval_sec) # delay in seconds
    LED.value(0)
    time.sleep(interval_sec)
    
