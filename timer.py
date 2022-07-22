from machine import Timer
from machine import Pin
import stat
import gc
import db
import sensor
import esp32
import mqtt
import fileopr
import json
import appconstants

server_mode = 'wifi'

led = Pin(5, Pin.OUT)
led.value(0)

tim0 = Timer(0)
tim1 = Timer(1)
tim0.init(period=5000, mode=Timer.PERIODIC, callback= lambda t: gc.collect())
#tim0.init(period=2000, mode=Timer.ONE_SHOT, callback= lambda t: led.value(not led.value()))

def handle_callback(timer):
    global led, server_mode
    led.value(1)
    print('Timer... Callback...')
    stat.print_stat()
    print('Server Mode:', server_mode)
    db.sensor_val['mcu_temp_f'] = esp32.raw_temperature()
    db.sensor_val['hall'] = esp32.hall_sensor()
    sensor_reading = sensor.get_dht_reading()
    db.sensor_val['temp_c'] = sensor_reading['temp_c']
    db.sensor_val['humid'] = sensor_reading['humid']

    print('Sensor Values:', db.sensor_val)
    if server_mode == 'mqtt':
        client = mqtt.connect_broker()
        if client:
            print('Publishing Sensor Values...')
            msg = json.dumps(db.sensor_val)
            topic = 'esp32/'+ appconstants.MACHINE_ID +'/sensor/vals'
            try:
                client.publish(bytes(topic, 'utf-8'), bytes(msg, 'utf-8'))
                print('Published Sensor Values to MQTT Topic:', topic, 'Value:', msg)
            except OSError as e:
                print('Some error in publishing Values to MQTT Broker, Resetting connection, Error:', e)
                mqtt.reset_connection()
                
    led.value(0)


def init_sensor_value_read():
    global server_mode, tim1
    sm_config = fileopr.read_from_file(appconstants.SERVER_MODE_CONFIG_FILE_PATH)
    if sm_config:
        sm_config = json.loads(sm_config)
        server_mode = sm_config['server_mode']
        print("[timer]: Server Mode:", server_mode)
    tim1.init(period=30000, mode=Timer.PERIODIC, callback= handle_callback) # Every 30 seconds publish value
