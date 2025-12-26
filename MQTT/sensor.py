import paho.mqtt.client as mqtt
import time
import json
import random

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("test.mosquitto.org", 1883, 60)

while True:
    
    data = {
        "sensor_id": "111",
        "temperature": round(random.uniform(20.0,25.0), 2),
        "humidity": round(random.uniform(40.0, 60.0), 2),
        "timestamp": time.time()
    }
    
    #konwersja dict na string json
    payload = json.dumps(data)
    
    client.publish("uken/jg/sensors", payload, qos=1)
    
    print(f"Wysłano dane: {payload}")
    time.sleep(5)