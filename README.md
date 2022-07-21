# Micropython Based Project for ESP32


### Description of Project
- This project enables ESP32 device to first create its own wifi access point names "ESP32-Server" with password set to "password".
- Then user can open IP Address 192.168.4.1 which will present user with web page.
- User can then set up his own Wifi Network credentials and MQTT credentials using web app.
- Once the setup is complete user can restart the device which will bring it to MQTT mode and will then publish DHT22 sensor data to MQTT Broker. 

### Credits
[MicroWebSrv](https://github.com/jczic/MicroWebSrv) is used for serving web requests.
[RuiSantosdotme ESP-MicroPython MQTT](https://raw.githubusercontent.com/RuiSantosdotme/ESP-MicroPython/master/code/MQTT/umqttsimple.py) package is used for publishing data to MQTT Broker.


### How to setup your own MQTT broker on Ubuntu/Debian

```bash
# To update repository
sudo apt get update
```

```bash
# To install MQTT Broker
sudo apt install mosquitto mosquitto-clients
```

```bash
# To create a user name "esp" , it will ask for password in prompt
sudo mosquitto_passwd -c /etc/mosquitto/passwd esp
```


```bash
# To change MQTT default config so that only authenticated clients can connect
sudo nano /etc/mosquitto/conf.d/default.conf

# Above command will open nano editior, copy following lines and save it.
listener 1883
allow_anonymous false
password_file /etc/mosquitto/passwd
```


```bash
# Restart MQTT Broker
sudo systemctl restart mosquitto
```

```bash
# To test , in one window run this command which will  subcribe for topic name "test-topic"
mosquitto_sub -h localhost -u esp -P password -t test-topic

# In another window open, run following command to publish message 
mosquitto_pub -h localhost -u esp -P password  -t test-topic -m "hello world"
```
