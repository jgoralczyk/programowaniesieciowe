import pika
import sys
import json
import logging

processed_message = set()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def crypto_consumer():
    if len(sys.argv) < 3:
        print("Użycie: python3 crypto_consumer.py [NAZWA_SERWISU] [MASKA_ROUTINGU]")
        print("Przykłady:")
        print("  python3 crypto_consumer.py Auditor '#' ")
        print("  python3 crypto_consumer.py US_Support '*.*.us' ")
        print("  python3 crypto_consumer.py Red_Phone '*.critical.*' ")
        sys.exit(1)

    service_name = sys.argv[1]
    binding_key = sys.argv[2]

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    exchange_name = 'crypto.topic.exchange'
    
    channel.exchange_declare(exchange='dlx_exchange', exchange_type='fanout')
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic')
    
    args = {
        'x-dead-letter-exchange': 'dlx_exchange',
        # Opcjonalnie: można też zmienić routing_key dla DLX
        # 'x-dead-letter-routing-key': 'failed_tasks' 
    }


    result = channel.queue_declare(queue='', exclusive=True, arguments=args)
    queue_name = result.method.queue

    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=binding_key)

    

    logging.info(f" [*] Serwis [{service_name}] uruchomiony. Słucham maski: {binding_key}")
    

    def callback(ch, method, properties, body):
        global processed_message
        try:
            data = json.loads(body)
            msg_id = data.get('message_id')
            
            if msg_id in processed_message:
                logging.warning(f"[!] Pominięcie: Wiadomość {msg_id} była juz przetworzona, przez ten worker")
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
            
            print(f"\n--- ODEBRANO PRZEZ {service_name} ---")
            print(f"Klucz: {method.routing_key}")
            print(f"Treść: {data}")
            print("-" * 30)
            
            processed_message.add(msg_id)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logging.error(f"Błąd, wysyłam do DLX: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
    channel.start_consuming()

if __name__ == "__main__":
    crypto_consumer()