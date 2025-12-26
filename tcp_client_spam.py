import socket
import time

SERVER_HOST = 'localhost'
SERVER_PORT = 9876
BUFFER_SIZE = 1024

print("Tworzę gniazdo klienta TCP...")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    
    server_address = (SERVER_HOST, SERVER_PORT)
    
    try:
        # 1. Łączymy się (tak jak poprzednio)
        print(f"Łączę się z serwerem {server_address}...")
        client_socket.connect(server_address)
        print("Połączono! Rozpoczynam wysyłanie w pętli (co 2 sek)...")

        counter = 0
        
        # 2. Pętla do wysyłania wiadomości
        while True:
            message = f"Ping #{counter}"
            
            # 3. Wysyłamy wiadomość
            client_socket.send(message.encode('utf-8'))
            print(f"Wysłano: {message}")
            
            # 4. Czekamy na echo
            response_data = client_socket.recv(BUFFER_SIZE)
            
            # 5. Jeśli recv() zwróci b'' TO serwer się grzecznie rozłączył
            if not response_data:
                print("Serwer grzecznie zamknął połączenie.")
                break
                
            print(f"Odebrano: {response_data.decode('utf-8')}")
            
            counter += 1
            time.sleep(2) # Czekamy 2 sekundy

    except socket.error as e:
        # 6. TUTAJ ZNAJDZIEMY SIĘ PO KATASTROFIE!
        # To jest "catch-all" dla błędów gniazda.
        print(f"\n*** WYSTĄPIŁ BŁĄD POŁĄCZENIA ***")
        print(f"Szczegóły błędu: {e}")
        
    except KeyboardInterrupt:
        # Na wypadek, gdybyśmy sami chcieli zamknąć klienta (Ctrl+C)
        print("\nZamykanie klienta...")

print("Klient zakończył działanie.")