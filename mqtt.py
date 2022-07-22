from umqttsimple import MQTTClient
import json
import fileopr
import gc
import appconstants
MACHINE_ID = appconstants.MACHINE_ID
MQTT_CONFIG_FILE_PATH = appconstants.MQTT_CONFIG_FILE_PATH

MQTT_CLIENT = None
default_sub_topic = b'perform_work'

conn_status = False
connect_retry = 3
retry_reset_counter = 0

def sub_callback(topic, msg):
    print('MQTT Sub Incoming:',(topic, msg))
    topic = topic.decode('utf-8')
    msg = msg.decode('utf-8')
    print("MQTT Sub Incoming: Decoded: Topic:", topic)
    print("MQTT Sub Incoming: Decoded: Msg:", msg)  
    

def connect_broker():
    global MQTT_CONFIG_FILE_PATH, MQTT_CLIENT, MACHINE_ID, conn_status, connect_retry, retry_reset_counter
    print('Connect MQTT Broker..., MQTT_CLIENT:', MQTT_CLIENT)
    try:
        if connect_retry <= 0 and retry_reset_counter < 10:
            retry_reset_counter += 1
            print('MQTT Connect retries exhausted. Will not try anymore.')
            return None
        if conn_status and MQTT_CLIENT:
            print('We already have MQTT client object, returning...')
            return MQTT_CLIENT
        else:
            print('Read from MQTT config from file...')
            mqtt_config = fileopr.read_from_file(MQTT_CONFIG_FILE_PATH)
            if mqtt_config:
                mqtt_config = json.loads(mqtt_config)
                print('MQTT config exists: ', mqtt_config)
                MQTT_CLIENT = MQTTClient(MACHINE_ID, mqtt_config['host'], mqtt_config['port'], mqtt_config['user'], mqtt_config['passwd'])
                MQTT_CLIENT.set_callback(sub_callback)
                MQTT_CLIENT.connect()
                MQTT_CLIENT.subscribe(default_sub_topic)  # subscribe to default topic
                conn_status = True
                print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_config['host'], default_sub_topic))
                return MQTT_CLIENT
            else:
                return None
    except OSError as e:
        connect_retry -=1
        print('Some Error Occured in connecting to MQTT Server:', e)
        print('Connect Retries Remaining:', connect_retry)
        return None

def subscribe_topic(topic):
    client = connect_broker()
    client.subscribe(topic)
    print('MQTT broker, Subscribed to %s topic' % (topic))

def reset_connection():
    global MQTT_CLIENT, conn_status, connect_retry
    MQTT_CLIENT = None
    conn_status = False
    connect_retry = 3


def start_mqtt_server():
    try:  
        gc.collect()
        client = connect_broker()
        if(client):
            print('Started MQTT Server')
            return True
        else:
            print('Unable to connect to MQTT Broker')
            return False
    except OSError as e:
        print('Some OS Error:', e)
        return False



# Put following code in some interrupt to monitor incoming messages for mqtt
# while True:
#     client.check_msg()