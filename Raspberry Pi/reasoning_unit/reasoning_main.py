#!/usr/bin/python3.7
import paho.mqtt.client as mqtt
import subprocess
import toProblem
import parsePlan
import sys
import random

# init
fanStatus = "(not(is-on fan1))"
alarmStatus = "(not(is-on alarm1))"
roomlightStatus = "(not(is-on roomled1))"
doorlightStatus = "(not(is-on doorled1))"
emerlightStatus = "(not(is-on emerled1))"
gasStatus = "(not(is-true gascrit1))"
tempStatus = "(not(is-true tempcrit1))"
btndoorStatus = "(not(is-on btndoor1))"
btnemerStatus = "(not(is-on btnemer1))"
# ---- light init depending on brightness ----
# at daytime use this
#lightStatus = "(not(is-true lightcrit1))"
# --------------------------------------------
# at nighttime use this
lightStatus = "(is-true lightcrit1)"
# --------------------------------------------

# mqtt
host = "1.1.1.1"
localhost = "127.0.0.1"
pddl_topic = "iot/pddl/+"

# telegram
emergency_on_msg = "🚨 Emergency at the Laboratory!"
emergency_off_msg = "✅ Emergency contained, everything okay!"
dummyWorkers = ['Noam Chomsky','Ada Lovelace','Alan Turing','Grace Hopper']
# emergency bool
emergencyBool = 0

# instruction topics
fantopic = "iot/actuators/fan"
alarmtopic = "iot/actuators/alarm"
roomlighttopic = "iot/actuators/roomlight"
doorlighttopic = "iot/actuators/doorlight"
emerlighttopic = "iot/actuators/emerlight"
telegramtopic = "iot/telegram"

def on_connect(client, userdata, flags, rc):
        print("connected with result code {0}".format(str(rc)))
        client.publish(fantopic, "False", 2)
        client.publish(alarmtopic, "False", 2)
        client.publish(roomlighttopic, "False", 2)
        client.publish(doorlighttopic, "False", 2)
        client.publish(emerlighttopic, "False", 2)
        

def on_disconnect(client, userdata, rc):
    print("Disconnect, reason: " + str(rc))
    print("Disconnect, reason: " + str(client))
    

def on_message(client, userdata, message):
    #print("\nMessage on topic: '{topic}' with payload:\n{payload}\n".format(topic=message.topic,payload=message.payload.decode()))
    try:
        # read message with values, create problem file in pddl
        varWriter(message)
        toProblem.make_problem(fanStatus, alarmStatus, roomlightStatus, doorlightStatus, emerlightStatus, gasStatus, tempStatus, lightStatus, btndoorStatus, btnemerStatus)
        print("problemvars:\n",fanStatus,"\n",alarmStatus,"\n",roomlightStatus,"\n",doorlightStatus,"\n",emerlightStatus,"\n",
        gasStatus,"\n",tempStatus,"\n",lightStatus,"\n",btndoorStatus,"\n",btnemerStatus,"\n")
        # feed pddl problem to ai planner, create plan
        # parse plan into mqtt messages
        planToMQTT(planCreator())
    except:
        print("Unexpected error in reasoning onMessage:", sys.exc_info()[0])
        

def varWriter(message):

    global fanStatus, alarmStatus, roomlightStatus, doorlightStatus, emerlightStatus, gasStatus, tempStatus, lightStatus, btndoorStatus, btnemerStatus

    if message.topic == "iot/pddl/fan":
        fanStatus = message.payload.decode()
    if message.topic == "iot/pddl/alarm":
        alarmStatus = message.payload.decode()
    if message.topic == "iot/pddl/roomlight":
        roomlightStatus = message.payload.decode()
    if message.topic == "iot/pddl/doorlight":
        doorlightStatus = message.payload.decode()
    if message.topic == "iot/pddl/emerlight":
        emerlightStatus = message.payload.decode()
    if message.topic == "iot/pddl/gasStatus":
        gasStatus = message.payload.decode()
    if message.topic == "iot/pddl/tempStatus":
        tempStatus = message.payload.decode()
    if message.topic == "iot/pddl/lightStatus":
        lightStatus = message.payload.decode()
    if message.topic == "iot/pddl/btndoorStatus":
        btndoorStatus = message.payload.decode()
    if message.topic == "iot/pddl/btnemerStatus":
        btnemerStatus = message.payload.decode()
        

def planCreator():
    plan = subprocess.run(["./ff", "-o", "domain_lab.pddl", "-f", "problem_lab_gen.pddl"], stdout=subprocess.PIPE).stdout.decode('utf-8')
    
    return plan


def planToMQTT(plan):    

    # emergency bool
    global emergencyBool

    # list of actions to perform from plan
    steps = parsePlan.readPlan(plan)

    # randomized worker that enters the lab        
    entrymsg_names = "ℹ️ {worker} entered the Lab!".format(worker=random.choice(dummyWorkers))

    for step in steps:
        if step == "LIGHT-ON":
            client.publish(roomlighttopic, "True", 2)

        if step == "LIGHT-NEUTRAL-OFF":
            client.publish(roomlighttopic, "False", 2)

        if step == "EMERGENCY-ON":
            emergencyBool = 1
            client.publish(alarmtopic, "True", 2)
            client.publish(emerlighttopic, "True", 2)
            client.publish(telegramtopic, emergency_on_msg , 2)

        if step == "EMERGENCY-NEUTRAL-OFF":            
            client.publish(alarmtopic, "False", 2)
            client.publish(emerlighttopic, "False", 2)

            if emergencyBool == 1:
                client.publish(telegramtopic, emergency_off_msg , 2)
                emergencyBool = 0

        if step == "FAN-ON":
            client.publish(fantopic, "True", 2)

        if step == "FAN-NEUTRAL-OFF":
            client.publish(fantopic, "False", 2)

        if step == "DOOR-OPEN":
            client.publish(doorlighttopic, "True", 2)
            client.publish(telegramtopic, entrymsg_names, 2)

        if step == "DOOR-NEUTRAL-CLOSE":
            client.publish(doorlighttopic, "False", 2)
        

client = mqtt.Client('Reasoning Main')
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect(host, 1883, 60)
client.subscribe(pddl_topic, 2)
client.loop_forever()