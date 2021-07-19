#!/usr/bin/python3.7
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import paho.mqtt.client as mqtt
from datetime import datetime

# mqtt
host = "1.1.1.1"
localhost = "127.0.0.1"
topic1 = "iot/sensors/button1"
topic2 = "iot/sensors/button2"
topic11 = "iot/pddl/btndoorStatus"
topic22 = "iot/pddl/btnemerStatus"

#init
# duration open door
interval = 5
# duration alarm min
interval2 = 10
# button init
emerBool = 0
doorBool = 0

# GPIO setup
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin to be an input pin and set initial value to be pulled low (off)
GPIO.setup(38, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, GPIO.HIGH)

try:
    # mqtt
    def on_connect(client, userdata, flags, rc):
        print("connected with result code {0}".format(str(rc)))

    def on_disconnect(client, userdata, rc):
        print("Disconnect, reason: " + str(rc))
        print("Disconnect, reason: " + str(client))
        
    def buttons_send(doorBool, emerBool):
        if GPIO.input(38) == GPIO.HIGH:
            doorBool = 1
            client.publish(topic11, "(is-on btndoor1)", 2)
            time.sleep(interval)
            
        if GPIO.input(35) == GPIO.HIGH:
            emerBool = 1
            client.publish(topic22, "(is-on btnemer1)", 2)
            time.sleep(interval2)     
            
        if ((GPIO.input(38) == GPIO.LOW) and (doorBool == 1)):            
            client.publish(topic11, "(not(is-on btndoor1))", 2)
            doorBool = 0
        
        if ((GPIO.input(35) == GPIO.LOW) and (emerBool == 1)):            
            client.publish(topic22, "(not(is-on btnemer1))", 2)
            emerBool = 0
        
      
    client = mqtt.Client('Buttons')
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(host, 1883, 60)
    client.loop_start()

    while True: # Run forever
        
        buttons_send(doorBool, emerBool)
        
        
    
except KeyboardInterrupt:
    print("\nKeyboardInterrupt")
except:
    print("\nOther error or exception")
finally:
    print("\nCleaning up GPIO pins")
    # cleanup resets all GPIO pins  
    GPIO.cleanup()