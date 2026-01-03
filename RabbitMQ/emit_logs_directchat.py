import pika
import sys

# 1. Połączenie
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# 2. Deklaracja Exchange typu 'direct'
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# 3. Pobranie poziomu ważności (routing key) i treści z argumentów konsoli
# Składnia: python emit_log_direct.py [info|warning|error] [wiadomość]
severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or 'Hello World!'

# 4. Wysyłka z konkretnym routing_key
channel.basic_publish(
    exchange='direct_logs',
    routing_key=severity,
    body=message)

print(f" [x] Wysłano [{severity}]: '{message}'")

connection.close()