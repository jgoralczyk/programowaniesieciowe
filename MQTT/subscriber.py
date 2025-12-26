import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc, properties):
    if rc == 0:
        print("Połączono")
        client.subscribe("uken/jg/test")
    else:
        print("Połączenie nieudane: {rc}")
        
def on_message(client,userdata,msg):
    print(f"Otrzymano wiadomosc na temacie {msg.topic}: {msg.payload.decode()}")
    
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

print("Czekam na wiadomości...")
client.loop_forever()