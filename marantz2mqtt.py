import os
import paho.mqtt.client as mqtt
import serial
import time

# Load environment variables (with fallbacks)
MQTT_HOST = os.getenv("MQTT_HOST", "")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_USER = os.getenv("MQTT_USER", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

# Use docker-compose to remap serial port as needed
SERIAL_PORT = "/dev/ttyUSB0"
SERIAL_BAUDRATE = int(os.getenv("SERIAL_BAUDRATE", "9600"))

# Initialize the serial port
ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("in_marantz")

def on_message(client, userdata, msg):
    # Send received MQTT payload to the serial port
    ser.write(msg.payload)
    resp = ser.read(16)
    print(resp)

    mesg = resp.decode("utf-8", errors="ignore")
    print(mesg)

    # Example message routing logic (as in original script)
    if mesg[1:4] == "SRC":
        client.publish("out_marantz/SRC", resp, qos=0, retain=True)
    elif mesg[1:4] == "NGT":
        client.publish("out_marantz/NGT", resp, qos=0, retain=True)
    elif mesg[1:4] == "SUR":
        client.publish("out_marantz/SUR", resp, qos=0, retain=True)
    elif mesg[1:4] == "INP":
        client.publish("out_marantz/INP", resp, qos=0, retain=True)
    elif mesg[1:4] == "VOL":
        client.publish("out_marantz/VOL", mesg[5:8], qos=0, retain=True)
    else:
        client.publish("out_marantz", resp, qos=0, retain=True)

# Create the MQTT client and connect using env variables
client = mqtt.Client()
client.username_pw_set(username=MQTT_USER, password=MQTT_PASSWORD)
client.connect(MQTT_HOST, MQTT_PORT, 60)

client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()
