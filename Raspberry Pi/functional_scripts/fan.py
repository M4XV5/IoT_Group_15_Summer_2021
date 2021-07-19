#!/usr/bin/python3.7
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from datetime import datetime

host = "1.1.1.1"
topic = "iot/actuators/fan"
topic2 = "iot/pddl/fan"

# compare bool
oldval = 1

#fan
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16, GPIO.OUT)
GPIO.output(16, GPIO.LOW)

try:
    def on_connect(client, userdata, flags, rc):
        print("connected with result code {0}".format(str(rc)))

    def on_disconnect(client, userdata, rc):
        print("Disconnect, reason: " + str(rc))
        print("Disconnect, reason: " + str(client))
        
    def on_message(client, userdata, message):
        try:
            active = message.payload.decode()
        except:
            print('Error: Message type not supported!')
            active = "False"
        fanControl(active)
        
    def fanControl(active):
        global oldval

        if active == "True" and oldval == 0:
            oldval = 1
            GPIO.output(16, GPIO.HIGH)
            client.publish(topic2, "(is-on fan1)", 2)
            
        elif active == "False" and oldval == 1:
            oldval = 0
            GPIO.output(16, GPIO.LOW)
            client.publish(topic2, "(not(is-on fan1))", 2)
        
    client = mqtt.Client('Fan')
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(host, 1883, 60)
    client.subscribe(topic, 2)
    client.loop_forever()
    
except KeyboardInterrupt:
    print("\nKeyboardInterrupt")
except:
    print("\nOther error or exception")
finally:
    print("\nCleaning up GPIO pins")
    # cleanup resets all GPIO pins
    GPIO.cleanup()