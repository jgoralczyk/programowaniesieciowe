import pika

#Łączenie z brokerem
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

#Deklaracja kolejki (tworzenie jezeli nie istnieje)
channel.queue_declare(queue='hello')

#Wysłanie wiadomości
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Witaj Świecie!')

print(" [x] Wysłano 'Witaj Świecie!'")
connection.close()