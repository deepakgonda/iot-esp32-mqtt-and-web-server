from time import sleep
from machine import Pin
from machine import Timer
from machine import reset
import fileopr
import appconstants

counter = 0
reset_button = Pin(19, Pin.IN)


def reset_counter():
    global counter
    counter = 0
    print('Reset counter to Zero.')


def handle_reset_interrupt(pin):
    global counter
    print('Reset Interupt Pressed')
    counter +=1
    if counter >= 3:
        print('Resetting ESP32 Board')
        fileopr.delete_file(appconstants.WIFI_CONFIG_FILE_PATH)
        fileopr.delete_file(appconstants.MQTT_CONFIG_FILE_PATH)
        fileopr.delete_file(appconstants.SERVER_MODE_CONFIG_FILE_PATH)
        reset()
    else:
        print('Not resetting b/c counter value is:', counter)
    
    
def set_up_intrupts():
    global reset_button
    reset_button.irq(trigger=Pin.IRQ_RISING, handler=handle_reset_interrupt)
    tim2 = Timer(2)
    tim2.init(period=5000, mode=Timer.PERIODIC, callback= lambda t: reset_counter())

    
    
