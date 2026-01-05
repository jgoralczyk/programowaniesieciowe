import pika
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_worker_with_dlx():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # 1. KONFIGURACJA DEAD LETTER EXCHANGE
    # To tutaj trafiają "zepsute" wiadomości
    channel.exchange_declare(exchange='dlx_exchange', exchange_type='fanout')
    channel.queue_declare(queue='dead_letters', durable=True)
    channel.queue_bind(exchange='dlx_exchange', queue='dead_letters')

    # 2. KONFIGURACJA GŁÓWNEJ KOLEJKI Z PARAMETREM DLX
    # Używamy argumentów, aby powiązać tę kolejkę z naszym bezpiecznikiem
    args = {
        'x-dead-letter-exchange': 'dlx_exchange',
        # Opcjonalnie: można też zmienić routing_key dla DLX
        # 'x-dead-letter-routing-key': 'failed_tasks' 
    }

    channel.queue_declare(queue='main_tasks', durable=True, arguments=args)
    channel.exchange_declare(exchange='main_exchange', exchange_type='direct')
    channel.queue_bind(exchange='main_exchange', queue='main_tasks', routing_key='task')

    def callback(ch, method, properties, body):
        message = body.decode()
        
        # SYMULACJA BŁĘDU: Jeśli wiadomość zawiera słowo "fail", odrzucamy ją
        if "fail" in message.lower():
            logger.error(f" [!] Wykryto błąd w wiadomości: {message}. Przenoszę do DLX.")
            # requeue=False jest kluczowe! Mówi: "Nie próbuj ponownie, wyślij do DLX"
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        else:
            logger.info(f" [v] Poprawnie przetworzono: {message}")
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='main_tasks', on_message_callback=callback)

    logger.info(' [*] Worker z DLX gotowy. Czekam na zadania...')
    channel.start_consuming()

if __name__ == "__main__":
    run_worker_with_dlx()