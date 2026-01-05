import pika
import logging
import json

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RabbitMQProducer:
    def __init__(self, host='localhost'):
        self.host = host
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        """Ustanawia połączenie i kanał."""
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
            self.channel = self.connection.channel()
            logger.info("Połączono z RabbitMQ")
        except Exception as e:
            logger.error(f"Nie udało się połączyć: {e}")
            raise

    def setup_exchange(self, name, type='direct'):
        """Deklaruje exchange przed wysyłką."""
        self.channel.exchange_declare(exchange=name, exchange_type=type, durable=True)

    def publish(self, exchange, routing_key, message):
        """Wysyła wiadomość (obsługuje słowniki/JSON)."""
        body = json.dumps(message) if isinstance(message, dict) else str(message)
        
        try:
            self.channel.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Wiadomość trwała (persistent)
                    content_type='application/json'
                )
            )
            logger.info(f" Wysłano do [{exchange}] z kluczem [{routing_key}]: {body}")
        except Exception as e:
            logger.error(f"Błąd podczas wysyłania: {e}")

    def close(self):
        if self.connection:
            self.connection.close()


if __name__ == "__main__":
    producer = RabbitMQProducer()
    
    # Obsługa wielu exchange na jednym połączeniu
    producer.setup_exchange('notifications', 'fanout')
    producer.setup_exchange('orders', 'direct')

    producer.publish('notifications', '', "Wiadomość ogólna do wszystkich")
    producer.publish('orders', 'pl', {"id": 123, "status": "opłacone"})
    
    producer.close()