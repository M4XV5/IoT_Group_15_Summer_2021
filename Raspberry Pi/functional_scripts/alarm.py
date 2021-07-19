#!/usr/bin/python3.7
import wiringpi as wp
import time
import threading
import paho.mqtt.client as mqtt

# compare bool
oldval = 1

# mqtt connection setup
topic = "iot/actuators/alarm"
topic2 = "iot/pddl/alarm"
host = "1.1.1.1"

# choose pin numbering scheme, see witingpi doc
wp.wiringPiSetupGpio()

# set pin
PIN = 22
wp.softToneCreate(PIN)

# set frequencies
a = 1500
b = 2500

# array for speaker to play
alarm = [a, a, a, 0, b, b, b, 0]
def on_message(client, userdata, message):
    global oldval
    
    try:
        active = message.payload.decode()
    except:
        print('Error: Message type not supported!')
        active = "False"
        
    if active == "True" and oldval == 0:
        oldval = 1
        client.publish(topic2, "(is-on alarm1)", 2)
        
    if active == "False" and oldval == 1:
        oldval = 0
        client.publish(topic2, "(not(is-on alarm1))", 2)
    
def on_connect(client, userdata, flags, rc):
    print("connected with result code {rc}".format(rc=str(rc)))
    
def on_disconnect(client, userdata, rc):
    print("Disconnect, reason: " + str(rc))
    print("Disconnect, reason: " + str(client))

def fred():
    global oldval

    while True:        
        if oldval == 1:
            for i in range(len(alarm)):
                wp.softToneWrite(PIN, alarm[i])
                time.sleep(0.1)         

# threading
t = threading.Thread(target=fred)
t.start()
        
client = mqtt.Client('Alarm')
client.on_message = on_message
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect(host, 1883, 60)
client.subscribe(topic, qos=2)
client.loop_forever()