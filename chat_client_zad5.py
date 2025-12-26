import socket
import threading

HOST = ''
PORT = 9888
BUFFER_SIZE = 1024

def receive_message(sock: socket):
    while True:
        try:
            data_bytes, _ = sock.recvfrom(BUFFER_SIZE)
            message = data_bytes.decode('utf-8')
            
            # \r czyści bieżącą linię (usuwa "Ty: ")
            # end="" zapobiega nowej linii po komunikacie
            print(f"\rOtrzymano: {message}\nTy:", end="")
            
        except Exception as e:
            print(f"Wyjebało błąd odbioru {e}")
            break

def send_message(sock, server_addr):
    
    try:
        sock.sendto(b"", server_addr)
    except Exception as e:
        print("Brak połączenia z serwerem: {e}")
        
    print("Połączono z serwerem, exit = wyjscie")
    
    while True:
        message = input("Ty: ")
        if message.lower() == 'exit':
            break
        
        message_bytes= message.encode("utf-8")
        sock.sendto(message_bytes, server_addr)
        

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    server_address = (HOST, PORT)
    
    
    # Tworzy nowy wątek, który uruchomi funkcję 'receive_messages'
    # daemon=True - wątek zamyka się auto gdy główny wątek te się zakońćzy
    receiver_thread = threading.Thread(target=receive_message, args= (client_socket,), daemon=True)
    
    # uruchamianie wątku odbiorczego w tle
    receiver_thread.start()
    
    send_message(client_socket, server_address)

print("Rozłączenie")