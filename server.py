import fileopr
import appconstants
    
def start_server():
    server_mode = 'http'
    status = False
    sm_config = fileopr.read_json_from_file(appconstants.SERVER_MODE_CONFIG_FILE_PATH)
    if sm_config:
        print("We have server mode set up file...", sm_config)
        server_mode = sm_config['server_mode']
    
    print('[server]: Server Mode:', server_mode)
    
    if server_mode == 'http':
        from web import start_web_server
        status = start_web_server()
    else:
        from mqtt import start_mqtt_server
        status = start_mqtt_server()
    return status