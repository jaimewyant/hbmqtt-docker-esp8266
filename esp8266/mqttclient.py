import network
import ubinascii
import gc
import machine
import ssl
import time
from umqttsimple import MQTTClient

gc.collect()

# Fill these in appropriately and the script should work.
NETWORK_ESSID = 'YOUR-ESSID'
NETWORK_PASSWD = 'YOUR-PASSWD'

CLIENT_CERT_DER = './client.crt.der'
CLIENT_KEY_DER = './client.key.der'
MQTT_SERVER_IP = '192.168.0.124'
MQTT_USERNAME = 'iot'
MQTT_PASSWORD = 'password'

def connect_to_network():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(NETWORK_ESSID, NETWORK_PASSWD)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


def sub_cb(topic, msg):
    print((topic, msg))


def connect_and_subscribe():
  with open(CLIENT_CERT_DER) as fo:
    cert_data = fo.read()

  with open(CLIENT_KEY_DER) as fo:
    key_data = fo.read()

  ssl_params={
    'cert': cert_data,
    'key': key_data,
    'server_side': False
  }

  client = MQTTClient(ubinascii.hexlify(machine.unique_id()),
                      MQTT_SERVER_IP, user=MQTT_USERNAME,
                      password=MQTT_PASSWORD, ssl=True,
                      ssl_params=ssl_params)
  client.set_callback(sub_cb)
  print('Connecting to', MQTT_SERVER_IP)
  print('Sit tight, the handshake is slow...  Seriously, be patient...')
  client.connect()
  client.subscribe('$SYS/broker/uptime')
  print('CONNECTED!')
  return client


def main():
  connect_to_network()
  client = connect_and_subscribe()

  while True:
    try:
      client.check_msg()
    except OSError as e:
      # restart_and_reconnect()
      print('error, im out', str(e))


main()
