import pika
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MultiWorker:
    def __init__(self, host='localhost'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        # Ograniczenie: nie dawaj workerowi więcej niż 1 zadanie na raz (Quality of Service)
        self.channel.basic_qos(prefetch_count=1)

    def callback_orders(self, ch, method, properties, body):
        logger.info(f" [SKLEP] Przetwarzam zamówienie: {body.decode()}")
        # Potwierdzenie przetworzenia
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def callback_logs(self, ch, method, properties, body):
        logger.info(f" [LOGI] Zapisuję log systemowy: {body.decode()}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def setup(self):
        # 1. Konfiguracja Kolejki Zamówień (Direct)
        self.channel.exchange_declare(exchange='orders', exchange_type='direct', durable=True)
        self.channel.queue_declare(queue='q_orders', durable=True)
        self.channel.queue_bind(exchange='orders', queue='q_orders', routing_key='pl')
        
        # 2. Konfiguracja Kolejki Powiadomień (Fanout)
        self.channel.exchange_declare(exchange='notifications', exchange_type='fanout', durable=True)
        self.channel.queue_declare(queue='q_notifications', exclusive=True)
        self.channel.queue_bind(exchange='notifications', queue='q_notifications')

        # REJESTRACJA KONSUMENTÓW
        self.channel.basic_consume(queue='q_orders', on_message_callback=self.callback_orders)
        self.channel.basic_consume(queue='q_notifications', on_message_callback=self.callback_logs)

    def run(self):
        logger.info(' [*] Worker uruchomiony. Nasłuchuję na wielu kolejkach...')
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            logger.info("Zamykanie workera...")
            self.connection.close()

if __name__ == "__main__":
    worker = MultiWorker()
    worker.setup()
    worker.run()