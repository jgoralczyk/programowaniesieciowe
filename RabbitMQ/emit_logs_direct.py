import pika, sys

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


# fanout to jak streaming
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

message = ' '.join(sys.argv[1:]) or "info: Hello World"
channel.basic_publish(exchange='direct_logs', routing_key='info', body=message)

print(f" [x] Wysłano {message}")
connection.close()

