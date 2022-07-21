import machine
from MicroWebSrv2 import *
import json
import fileopr
import mqtt
import appconstants
import gc


# ----------------------Web Routes Start --------------------------------------------------
@WebRoute(GET, '/device-info')
def RequestJSONGet(microWebSrv2, request) :
    request.Response.ReturnOkJSON({
        'ClientAddr' : request.UserAddress,
        'Accept'     : request.Accept,
        'UserAgent'  : request.UserAgent,
        'MACHINE_ID' : appconstants.MACHINE_ID
    })
    

@WebRoute(POST, '/server-operation')
def RequestServerOperation(microWebSrv2, request) :
    data = request.GetPostedJSONObject()
    print('Posted Data:', data)
    success = False
    if data["token"] == 'ESP32-DP-STOP-2022':
        if data["operation"] == 'restart':
            machine.reset()
            success = True
        else:
            print('Operation Not Supported')
    request.Response.ReturnOkJSON({
        'data': {
                    'status': success
                }
    })


@WebRoute(POST, '/set-up-ssid')
def RequestServerOperation(microWebSrv2, request) :
    data = request.GetPostedJSONObject()
    print('Posted Data:', data)
    success = False
    msg = 'Done!'
    if not data["ssid"] or not data["passwd"]:
        msg = 'BAD_REQUEST'
    else:
        print('Write New SSID config in file...')
        fileopr.write_to_file(appconstants.WIFI_CONFIG_FILE_PATH, json.dumps(data))
    request.Response.ReturnOkJSON({
        'data': {
                'status': success,
                'message': msg
            }
    })

@WebRoute(GET, '/get-ssid')
def RequestServerOperation(microWebSrv2, request) :
    print('Read from SSID config in file...')
    cred_in_json = fileopr.read_from_file(appconstants.WIFI_CONFIG_FILE_PATH)
    if cred_in_json:
        request.Response.ReturnOkJSON({
            'data': json.loads(cred_in_json),
            'message': 'File Read Success'
        })
    else:
        print('File Reading failed...')
        request.Response.ReturnOkJSON({
            'data': None,
            'message': 'File reading failed.'
        })
        
@WebRoute(GET, '/remove-ssid')
def RequestServerOperation(microWebSrv2, request) :
    print('Removing SSID config file...')
    cred_in_json = fileopr.delete_file(appconstants.WIFI_CONFIG_FILE_PATH)
    request.Response.ReturnOkJSON({
        'data': None,
        'message': 'File Delete Success'
    })
        
        
@WebRoute(POST, '/set-up-mqtt')
def RequestServerOperation(microWebSrv2, request) :
    data = request.GetPostedJSONObject()
    print('Posted Data:', data)
    success = False
    msg = 'Done!'
    if not data["host"] or not data["port"] or not data["user"] or not data["passwd"]:
        msg = 'BAD_REQUEST'
    else:
        print('Write New MQTT config in file...')
        fileopr.write_to_file(appconstants.MQTT_CONFIG_FILE_PATH, json.dumps(data))
        success = True
    request.Response.ReturnOkJSON({
        'data': {
                'status': success,
                'message': msg
            }
    })

@WebRoute(GET, '/get-mqtt-config')
def RequestServerOperation(microWebSrv2, request) :
    print('Read from MQTT config in file...')
    cred_in_json = fileopr.read_from_file(appconstants.MQTT_CONFIG_FILE_PATH)
    if cred_in_json:
        request.Response.ReturnOkJSON({
            'data': json.loads(cred_in_json),
            'message': 'File Read Success'
        })
    else:
        print('File Reading failed...')
        request.Response.ReturnOkJSON({
            'data': None,
            'message': 'File reading failed.'
        })
        
@WebRoute(GET, '/remove-mqtt-config')
def RequestServerOperation(microWebSrv2, request) :
    print('Removing SSID config file...')
    cred_in_json = fileopr.delete_file(appconstants.MQTT_CONFIG_FILE_PATH)
    request.Response.ReturnOkJSON({
        'data': None,
        'message': 'File Delete Success'
    })
        
        
@WebRoute(GET, '/promote-to-mqtt')
def RequestServerOperation(microWebSrv2, request) :
    print('Promoting to MQTT.., Checking neccessary requirements')
    global ms2
    client = mqtt.connect_broker()
    if client:
        print('Started MQTT and stopped mws2 http server')
        mode = {'server_mode': 'mqtt'}
        fileopr.write_to_file(appconstants.SERVER_MODE_CONFIG_FILE_PATH, json.dumps(mode))
        request.Response.ReturnOkJSON({
            'data': None,
            'message': 'MQTT Promotion Success'
        })
        machine.reset()
    else:
        request.Response.ReturnOkJSON({
            'data': None,
            'message': 'MQTT Promotion Failed.'
        })
    
# ----------------------Web Routes End --------------------------------------------------

def start_web_server():
    try:  
        gc.collect()
        mws2 = MicroWebSrv2()
        mws2.SetEmbeddedConfig()
        mws2.ConnQueueCapacity = 2
        mws2.BufferSlotsCount = 8
        mws2.RootPath = 'www'
        mws2.NotFoundURL = '/'
        mws2.RequestsTimeoutSec = 10
        gc.collect()
        mws2.StartManaged()
        print('Started Web Server...')
        return True
    except OSError as e:
        print('Some Error In Starting Web Server:', e)
        return False

