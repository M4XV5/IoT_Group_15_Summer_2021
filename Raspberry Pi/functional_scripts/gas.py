#!/usr/bin/python3.7
import time
import paho.mqtt.client as mqtt
from datetime import datetime

# ADC
from MCP3008 import MCP3008

# mqtt
topic = "iot/sensors/gas"
topic2 = "iot/pddl/gasStatus"
host = "1.1.1.1"
localhost = "127.0.0.1"

# compare bool
oldval = -1

# time interval
interval = 1

#threshold
threshold = 2500

adc = MCP3008()
#value = adc.read( channel = 2 )
#print("applied voltage: %.2f" % (value / 1023.0 * 3.3) )

# mqtt
def on_connect(client, userdata, flags, rc):
    print("connected with result code {0}".format(str(rc)))

def on_disconnect(client, userdata, rc):
    print("Disconnect, reason: " + str(rc))
    print("Disconnect, reason: " + str(client))
    
def gas_send():
    global oldval
    gasval = adc.read(channel = 2)
    if gasval >= threshold and oldval == 0:
        oldval = 1
        client.publish(topic2, "(is-true gascrit1)", 2)
    elif gasval < threshold and oldval == 1: 
        oldval = 0
        client.publish(topic2, "(not(is-true gascrit1))", 2)
    elif oldval == -1:
        oldval = 0
        client.publish(topic2, "(not(is-true gascrit1))", 2)
    
client = mqtt.Client('Gas Sensor')
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(host, 1883, 60)
client.loop_start()



while True:
    
    gas_send()
    
    time.sleep(interval);