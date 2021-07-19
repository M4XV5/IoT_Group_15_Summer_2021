#!/usr/bin/python3.7
import time
import paho.mqtt.client as mqtt
from datetime import datetime

# import MCP namespace from selfmade class
from MCP3008 import MCP3008

# compare bool
oldval = -1

# time interval
interval = 1

# light threshold
threshold = 2500

topic = "iot/sensors/brightness"
topic2 = "iot/pddl/lightStatus"
host = "1.1.1.1"
localhost = "127.0.0.1"

# mqtt
def on_connect(client, userdata, flags, rc):
    print("connected with result code {0}".format(str(rc)))

def on_disconnect(client, userdata, rc):
    print("Disconnect, reason: " + str(rc))
    print("Disconnect, reason: " + str(client))
    
def brightness_send():    
    global oldval
    brightness = adc.read(channel = 0)
    if brightness >= threshold and oldval == 0:
        oldval = 1
        client.publish(topic2, "(not(is-true lightcrit1))", 2)

    elif brightness < threshold and oldval == 1:
        oldval = 0
        client.publish(topic2, "(is-true lightcrit1)", 2)

    elif oldval == -1:
        if brightness >= threshold:
            oldval = 1
            client.publish(topic2, "(not(is-true lightcrit1))", 2)
            
        if brightness < threshold:
            oldval = 0
            client.publish(topic2, "(is-true lightcrit1)", 2)

        
    
client = mqtt.Client('Brightness Sensor')
client.connect(host, 1883, 60)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.loop_start()

# read analog-digital converter
adc = MCP3008()
#value = adc.read( channel = 0 ) # adjust read channel if needed
#print("Current: %.2f" % (value / 1023.0 * 3.3) )

# monitor adc output
while True:
    
    brightness_send()

    time.sleep(interval)