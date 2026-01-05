import pika
import json
import random
import time
import logging
import uuid

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class CryptoProducer:
    def __init__(self, host='localhost'):
        self.exchange_name = 'crypto.topic.exchange'
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()
        
        self.channel.exchange_declare(exchange=self.exchange_name,exchange_type='topic')
        
    def start_emitting(self):
        currencies = ['btc', 'eth', 'sol', 'dot']
        priorities = ['info', 'warning', 'critical']
        regions = ['eu', 'us', 'asia']
        
        logging.info(f"[*] Rozpoczynam nadawanie alertów na {self.exchange_name}")
        
        try:
            while True:
                curr = random.choice(currencies)
                prio = random.choice(priorities)
                reg = random.choice(regions)
                
                routing_key = f"{curr}.{prio}.{reg}"
                
                payload = {
                    "message_id": str(uuid.uuid4()),
                    "timestamp": time.time(),
                    "currency": curr.upper(),
                    "alert_level": prio.upper(),
                    "market_region": reg.upper(),
                    "price_change": round(random.uniform(-5.0,5.0), 2),
                    "volume": random.randint(100,10000)
                }
                
                self.channel.basic_publish(
                    exchange= self.exchange_name,
                    routing_key=routing_key,
                    body=json.dumps(payload),
                    properties=pika.BasicProperties(content_type='application/json')
                )
                
                logging.info(f"[x] Wysłano [{routing_key}]: {payload['price_change']}%")
                time.sleep(2)
        except KeyboardInterrupt:
            self.connection.close()
            
if __name__ == "__main__":
    producer = CryptoProducer()
    producer.start_emitting()


        