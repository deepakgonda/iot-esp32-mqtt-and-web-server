import machine
from microWebSrv import MicroWebSrv
import json
import fileopr
import appconstants
import gc


# ----------------------Web Routes Start --------------------------------------------------
@MicroWebSrv.route('/device-info', 'GET')
def RequestJSONGet(httpClient, httpResponse) :
    httpResponse.WriteResponseJSONOk({
        'ClientAddr' : httpClient.GetIPAddr(),
        'MACHINE_ID' : appconstants.MACHINE_ID
    })
    

@MicroWebSrv.route('/server-operation', 'POST')
def RequestServerOperation(httpClient, httpResponse) :
    data = httpClient.ReadRequestContentAsJSON()
    print('Posted Data:', data)
    success = False
    if data["token"] == 'ESP32-DP-STOP-2022':
        if data["operation"] == 'restart':
            machine.reset()
            success = True
        else:
            print('Operation Not Supported')
    httpResponse.WriteResponseJSONOk({
        'data': {
                    'status': success
                }
    })


@MicroWebSrv.route('/set-up-ssid', 'POST')
def RequestServerOperation(httpClient, httpResponse) :
    data = httpClient.ReadRequestContentAsJSON()
    print('Posted Data:', data)
    success = False
    msg = 'Done!'
    if not data["ssid"] or not data["passwd"]:
        msg = 'BAD_REQUEST'
    else:
        print('Write New SSID config in file...')
        fileopr.write_to_file(appconstants.WIFI_CONFIG_FILE_PATH, json.dumps(data))
        success = True
    httpResponse.WriteResponseJSONOk({
        'data': {
                'status': success,
                'message': msg
            }
    })

@MicroWebSrv.route('/get-ssid', 'GET')
def RequestServerOperation(httpClient, httpResponse) :
    print('Read from SSID config in file...')
    cred_in_json = fileopr.read_json_from_file(appconstants.WIFI_CONFIG_FILE_PATH)
    if cred_in_json:
        httpResponse.WriteResponseJSONOk({
            'data': cred_in_json,
            'message': 'File Read Success'
        })
    else:
        print('File Reading failed...')
        httpResponse.WriteResponseJSONOk({
            'data': None,
            'message': 'File reading failed.'
        })
        
@MicroWebSrv.route('/remove-ssid', 'GET')
def RequestServerOperation(httpClient, httpResponse) :
    print('Removing SSID config file...')
    cred_in_json = fileopr.delete_file(appconstants.WIFI_CONFIG_FILE_PATH)
    httpResponse.WriteResponseJSONOk({
        'data': None,
        'message': 'File Delete Success'
    })
        
        
@MicroWebSrv.route('/set-up-mqtt','POST')
def RequestServerOperation(httpClient, httpResponse) :
    data = httpClient.ReadRequestContentAsJSON()
    print('Posted Data:', data)
    success = False
    msg = 'Done!'
    if not data["host"] or not data["port"] or not data["user"] or not data["passwd"]:
        msg = 'BAD_REQUEST'
    else:
        print('Write New MQTT config in file...')
        fileopr.write_to_file(appconstants.MQTT_CONFIG_FILE_PATH, json.dumps(data))
        success = True
    httpResponse.WriteResponseJSONOk({
        'data': {
                'status': success,
                'message': msg
            }
    })

@MicroWebSrv.route('/get-mqtt-config', 'GET')
def RequestServerOperation(httpClient, httpResponse) :
    print('Read from MQTT config in file...')
    cred_in_json = fileopr.read_json_from_file(appconstants.MQTT_CONFIG_FILE_PATH)
    if cred_in_json:
        httpResponse.WriteResponseJSONOk({
            'data': cred_in_json,
            'message': 'File Read Success'
        })
    else:
        print('File Reading failed...')
        httpResponse.WriteResponseJSONOk({
            'data': None,
            'message': 'File reading failed.'
        })
        
@MicroWebSrv.route('/remove-mqtt-config', 'GET')
def RequestServerOperation(httpClient, httpResponse) :
    print('Removing SSID config file...')
    cred_in_json = fileopr.delete_file(appconstants.MQTT_CONFIG_FILE_PATH)
    httpResponse.WriteResponseJSONOk({
        'data': None,
        'message': 'File Delete Success'
    })
        
        
@MicroWebSrv.route('/promote-to-mqtt', 'GET')
def RequestServerOperation(httpClient, httpResponse) :
    print('Promoting to MQTT.., Checking neccessary requirements')
    global ms2
    success = False
    from mqtt import connect_broker
    client = connect_broker()
    if client:
        print('Started MQTT and stopped mws2 http server')
        mode = {'server_mode': 'mqtt'}
        fileopr.write_to_file(appconstants.SERVER_MODE_CONFIG_FILE_PATH, json.dumps(mode))
        success = True
        httpResponse.WriteResponseJSONOk({
            'data': None,
            'status': success,
            'message': 'MQTT Promotion Success. Please restart machine'
        })
    else:
        httpResponse.WriteResponseJSONOk({
            'data': None,
            'status': success,
            'message': 'MQTT Promotion Failed.'
        })
    
# ----------------------Web Routes End --------------------------------------------------



def start_web_server():
    try:  
        gc.collect()
        mws = MicroWebSrv(webPath='www/')      # TCP port 80 and files in /flash/www
        mws.SetNotFoundPageUrl("/index.html")
        mws.Start(threaded=True) # Starts server in a new thread
        print('Started Web Server...')
        return True
    except OSError as e:
        print('Some Error In Starting Web Server:', e)
        return False

