import pika, sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


# fanout to jak streaming
channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World"
channel.basic_publish(exchange='logs', routing_key='', body=message)

print(f" [x] Wysłano {message}")
connection.close()

