import network
import time
import json

import fileopr
import appconstants


AP_SSID = appconstants.AP_SSID
AP_PASSW = appconstants.AP_PASSW
WIFI_CONFIG_FILE_PATH = appconstants.WIFI_CONFIG_FILE_PATH


def init_wifi():
    try:
        ssid_config = fileopr.read_from_file(WIFI_CONFIG_FILE_PATH)
        if ssid_config:
            ssid_config = json.loads(ssid_config)
            print('SSID config exists:', ssid_config)
            wlan = network.WLAN(network.STA_IF)
            #wlan.config(reconnects=10)
            wlan.active(True)
            if not wlan.isconnected():
                print('connecting to network...')
                wlan.connect(ssid_config["ssid"], ssid_config["passwd"])
                while not wlan.isconnected():
                    pass
            time.sleep(5)
            print('Connected To:', ssid_config["ssid"],'on IP:', wlan.ifconfig())
        else:
            print('No SSID config exists, We will create our own')
            ap = network.WLAN(network.AP_IF) # create access-point interface
            ap.config(essid=AP_SSID, password=AP_PASSW, authmode=3) # set the SSID of the access point
            ap.config(max_clients=3) # set how many clients can connect to the network
            ap.active(True)         # activate the interface
            time.sleep(5)
            print('New SSID AP created: ', AP_SSID, 'Config:', ap.ifconfig())        
    except OSError as e:
        print("exception", str(e))
