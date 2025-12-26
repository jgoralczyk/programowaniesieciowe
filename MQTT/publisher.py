import paho.mqtt.client as mqtt
import time

#config
BROKER = "test.mosquitto.org"
TOPIC = "uken/jg/test"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

print(f"Łączenie z borkerem {BROKER}")
client.connect(BROKER, 1883, 60)

message = "Wiadomość z Pythona!"
client.publish(TOPIC, message)
print(f"Wysłano: '{message}' na temat: {TOPIC}")

client.disconnect()
