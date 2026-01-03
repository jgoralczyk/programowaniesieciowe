import pika, time


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable= True)

def callback(ch,method,properties, body):
    print(f" [X] Otrzymano {body.decode()}")
    time.sleep(body.count(b'.'))
    print("[X] Gotowe")
    
    #reczne potwierdzenie odebrania
    ch.basic_ack(delivery_tag=method.delivery_tag)

#nie wysylaj nowej wiadomosci dopóki worker nie skonczy jednej
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()