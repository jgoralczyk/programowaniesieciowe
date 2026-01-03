import pika

print("--- Start skryptu ---")

# 1. Połączenie
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    print("--- Połączono z RabbitMQ ---")
except Exception as e:
    print(f"Błąd połączenia: {e}")
    exit()

# 2. Deklaracja kolejki
channel.queue_declare(queue='hello')

# 3. Definicja funkcji zwrotnej
def callback(ch, method, properties, body):
    print(f" [x] Odebrano: {body.decode()}")

# 4. Rejestracja konsumenta
channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)


print(' [*] Czekam na wiadomości. Aby wyjść, naciśnij CTRL+C')

# 5. KLUCZOWY MOMENT - pętla blokująca
channel.start_consuming()

# To się nigdy nie powinno wyświetlić, dopóki nie przerwiesz programu
print("--- Koniec skryptu (To nie powinno się pojawić!) ---")