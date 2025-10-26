import socket
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 9876
BUFFEER_SIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    
    server_address = (SERVER_HOST, SERVER_PORT)
    counter = 0
    
    while True:
        try:
            message = f"Wiadomość numer {counter}"
            
            message_bytes = message.encode('utf-8')
            
            print(f"Wysyłam: {message}")
            client_socket.sendto(message_bytes, server_address)
            
            # Odbieranie
            response_bytes, _ = client_socket.recvfrom(BUFFEER_SIZE)
            respone = response_bytes.decode('utf-8')
            print(f"Odpowiedź: {respone}\n")
            
            counter += 1
            
            time.sleep(1)
        
        
        
        except KeyboardInterrupt:
            print("Zatrzymywanie klienta")
            break
        except Exception as e:
            print(f"Złapałem błąd: {e}")
            time.sleep(2)