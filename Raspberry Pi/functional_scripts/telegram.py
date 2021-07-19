#!/usr/bin/python3.7
import requests
import json
import paho.mqtt.client as mqtt

# time interval
interval = 10

# mqtt
topic = "iot/telegram"
host = "1.1.1.1"
localhost = "127.0.0.1"

# mqtt
def on_message(client, userdata, message):
    try:
        msg = message.payload.decode()
        send_message(msg)
    except:
        print('Telegram: Could not decode message.')

# telegram
def send_message(msg):
    # Bot Auth Token
    token = '{BOT TOKEN}'
    sendUrl = f'https://api.telegram.org/bot{token}/sendMessage'
    # IoT Group chat ID
    chat_id = '{CHAT ID}'
    try:
        message = msg
    except:
        print('Messaging failed.')
    data = {'chat_id': {chat_id}, 'text': {message.format(msg)}}
    requests.post(sendUrl, data).json()

# mqtt
def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(str(rc)))

def on_disconnect(client, userdata, rc):
    print("Disconnect, reason: " + str(rc))
    print("Disconnect, reason: " + str(client))

if __name__ == '__main__':
    client = mqtt.Client('Telegram')
    client.on_message = on_message
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(host, 1883, 60)
    client.subscribe(topic, 2)
    client.loop_forever()