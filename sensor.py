import machine
import time
import dht

sensor = dht.DHT22(machine.Pin(18))
#sensor = dht.DHT11(machine.Pin(18))

def get_dht_reading():
    try:
        sensor.measure() 
        t = sensor.temperature()
        h = sensor.humidity()
        print('Temp:',t, 'Humidity:', h)
        return {'temp_c': t, 'humid': h}
    except OSError as e:
        print('[dht] Error:', e)
        return None
