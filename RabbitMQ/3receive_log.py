import pika, sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

#deklaracja exchange musi być taka sama jak u nadawacy
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# Kolejka tymczasowa
# exclusive+True usuwa kolejke, po zamknięciu skryptu
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

#Binding "Wszystko co trafi do exchange logs wysyłaj do mojej tymczasowej kolejki"
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] oczekiwanie na logi. exit ctrl + c')

def callback(ch,method,properties, body):
    print(f"[x] Log: {body.decode()}")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
