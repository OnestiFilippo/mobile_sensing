import paho.mqtt.client as mqtt
import json


def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("records")

def on_message(client, userdata, msg):
  print("Received message on topic '"+msg.topic+"'")
  if Operation._write_file(msg.payload):
    print("Record saved")
  else:
    print("Error saving record")

class Operation():
  def _write_file(msg):
    try:
      jdata = json.loads(msg)
      print("Received record with "+str(len(jdata)-1)+" readings named "+jdata[-1]["name"])
      filename = jdata[-1]["name"]
      jdata.pop()
      f = open("html/records/"+filename, "w")
      f.write(str(json.dumps(jdata, sort_keys=True, indent=4)))
      f.close()
      return True
    except Exception as e:
      return False

def main():
  client = mqtt.Client()
  client.connect("192.168.1.55",1883,60)

  client.on_connect = on_connect
  client.on_message = on_message

  client.loop_forever()

if __name__ == "__main__":
    main()
