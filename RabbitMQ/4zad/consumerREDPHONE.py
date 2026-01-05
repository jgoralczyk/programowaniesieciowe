import pika
import json
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RedPhone")

class RedPhone:
    def __init__(self,host):
        self.exchange_name = 'crypto.topic.exchange'
        self.processed_message = set()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        
        self.channel.exchange_declare(exchange='crypto_dlx', exchange_type='fanout')
        self.channel.queue_declare(queue='failed_crypto_alerts',durable=True)
        self.channel.queue_bind(queue='failed_crypto_alerts', exchange='crypto_dlx')
        
        args = {
        'x-dead-letter-exchange': 'crypto_dlx'
        }
        
        self.channel.queue_declare(queue='red_phone_queue',arguments=args,durable=True)
        self.channel.exchange_declare(exchange='crypto.topic.exchange', exchange_type='topic')
        self.channel.queue_bind(exchange='crypto.topic.exchange', queue='red_phone_queue',routing_key='*.critical.*')
    
    
    def callback(self,ch,method,properties,body):
        try:
            data = json.loads(body)
            msg_id = data.get('message_id')
            
            if msg_id in self.processed_message:
                logger.error(f"[!] Ta wiadomość juz była: {msg_id}")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
            
            logger.info(f"[^] Przetwarzanie alertu krytycznego: {data['currency']}")
            
            # SYmulacja bledu
            if data['currency'] == 'SOL':
                raise ValueError("Błąd krytyczny bazdy danych przy SOLANA")
            
            self.processed_message.add(msg_id)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        except Exception as e:
            logger.error(f"[X] Błąd: {e} Przenoszenie do DLQ")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def run(self):
        self.channel.basic_consume(queue='red_phone_queue', on_message_callback=self.callback)
        self.channel.start_consuming()

if __name__ == "__main__":
    RedPhone('localhost').run()
        
        