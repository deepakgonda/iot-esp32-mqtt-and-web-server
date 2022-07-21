import time
import fileopr
import appconstants
from machine import Pin
from machine import Timer
from machine import reset

counter = 0
reset_button = Pin(19, Pin.IN)
is_timer_running = False
last_value_change_ms = time.ticks_ms()

def reset_counter():
    global counter, is_timer_running
    counter = 0
    is_timer_running = False
    print('Reset counter to Zero.')


def handle_reset_interrupt(pin):
    global counter, tim2, is_timer_running, last_value_change_ms
    print('Reset Interupt Pressed')
    t1 = time.ticks_ms()
    dt = time.ticks_diff(t1, last_value_change_ms)
    print('DT:', dt)
    if dt < 325:
        print('Interval Too Less to count reset, keeping counter value:', counter)
    else:
        last_value_change_ms = t1
        if not is_timer_running:
            is_timer_running = True
            tim2 = Timer(2)
            tim2.init(period=5000, mode=Timer.ONE_SHOT, callback= lambda t: reset_counter())
            print('Started Reset Timer...')
        
        counter +=1
        if counter >= 3:
            print('Deleting all config files on ESP32 Board b/c counter value is:', counter)   
            fileopr.delete_file(appconstants.WIFI_CONFIG_FILE_PATH)
            fileopr.delete_file(appconstants.MQTT_CONFIG_FILE_PATH)
            fileopr.delete_file(appconstants.SERVER_MODE_CONFIG_FILE_PATH)
            reset()  # Machine will restart
        else:
            print('Not resetting b/c counter value is:', counter)
    
def set_up_intrupts():
    global reset_button
    reset_button.irq(trigger=Pin.IRQ_RISING, handler=handle_reset_interrupt)

    
    
