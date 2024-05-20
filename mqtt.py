import paho.mqtt.client as mqtt
import json

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("records")

def on_message(client, userdata, msg):
  jdata = json.loads(msg.payload.decode())
  print("Received record with "+str(len(jdata)-1)+" readings")
  try:
    filename = jdata[-1]["name"]
    jdata.pop()
    f = open("html/records/"+filename, "w")
    f.write(str(json.dumps(jdata, sort_keys=True, indent=4)))
    f.close()
  except Exception as e:
    print("Error "+str(e))
    exit(1)

client = mqtt.Client()
client.connect("192.168.1.55",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
