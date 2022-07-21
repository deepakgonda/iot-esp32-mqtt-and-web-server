import esp
esp.osdebug(None)
import gc
gc.collect()
import time
import machine

from wifi import init_wifi
from timer import init_sensor_value_read
from stat import print_stat
from intr import set_up_intrupts
from server import start_server

# Main program loop until error
gc.collect()
try :
    print_stat()
    time.sleep(1)
    init_wifi()
    time.sleep(3)
    gc.collect()
    status = start_server()
    time.sleep(3)
    gc.collect()
    if status:
        print('Server Started, Setting up Tmers and interrupts')
        init_sensor_value_read()
        time.sleep(1)
        set_up_intrupts()
    else:
        print('Couldn\'t start server, hence restarting')
        machine.reset()
except OSError as e:
    print('Error:', str(e))