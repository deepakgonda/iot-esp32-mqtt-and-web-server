import machine
import ubinascii
MACHINE_ID = ubinascii.hexlify(machine.unique_id()).decode("utf-8")

AP_SSID = 'ESP-32-SERVER'
AP_PASSW = 'password'
WIFI_CONFIG_FILE_PATH = '/config/network/wifi.txt'
MQTT_CONFIG_FILE_PATH = '/config/mqtt/mqtt.txt'
SERVER_MODE_CONFIG_FILE_PATH = '/config/server/mode.txt'