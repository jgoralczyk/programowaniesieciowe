import socket
import threading

HOST = ''
PORT = 9876
BUF_SIZ = 1024

client_list = []
#Chronimy liste bo wiele wątków chcę ją uzywać
client_lock = threading.Lock()

def handle_client(connection_socket: socket, client_address):
    """
    Funkcja w osobynm wątku dla kazdego połączenia klienckiego
    """
    print(f"[Nowe Połączenie] Dołączył {client_address}")
    
    with client_lock:
        client_list.append(connection_socket)
        
    try: 
        while True:
            
            #czekamy na wiadomość od tego klienta
            data = connection_socket.recv(BUF_SIZ)
            
            if not data:
                print(f"[Rozłączenie] Klient {client_address} odszedł")
                break
            
            #wiadomość do wszystkich
            message = f"[{client_address}]: {data.decode('utf-8')}"
            print(f"Rozgłąszam od {client_address}: {data.decode('utf-8')}")
            
            #Wywołanie broadcastu
            broadcast(message.encode('utf-8'), connection_socket)
    
    except socket.error as e:
        print(f"[Błąd] klient {client_address} rozłączył się niespodziewanie: {e}")
        
    finally:
        # Niezaleznie czy break czy except musimy posprzątać po kliencie
        with client_lock:
            if connection_socket in client_list:
                client_list.remove(connection_socket)
        
        connection_socket.close()
        
def broadcast(message_bytes, sender_socket):
    """
    Wysyła wiadomości do wszystkich klientów na liście poza nadawcą
    """
    
    with client_lock:
        clients_to_remove = []
        
        for client_socket in client_list:
            if client_socket != sender_socket:
                try:
                    #wysyłamy wiadomość
                    client_socket.send(message_bytes)
                except socket.error:
                    #Klient prawdopodobnie umarł, nie mozemy go usunac w trakcie iteracji
                    #więc dodajemy do klientów do usunięcia
                    print(f"[BROADCAST Error] nie Mozna wysłać do klienta {client_socket}, oznaczam do usunięcia")
                    clients_to_remove.append(client_socket)
        
        for dead_socket in clients_to_remove:
            client_list.remove(dead_socket)
            dead_socket.close()


# Główny wątek
def start_server():
    print("[START Serwera] Tworze gniazdo do nasłuchu...")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listen_socket:
        listen_socket.bind((HOST,PORT))
        listen_socket.listen(5)
        print(f"[Nasłuchiwanie] Serwer czeka na klientów na porcie {PORT}")
        
        # główna pętla, bramkarz dupczyciel
        while True:
            #czekanie na gościa
            connection_socket, client_address = listen_socket.accept()
            
            #Nowy klient tworzymy dla niego wątek
            client_thread = threading.Thread(
                target= handle_client,
                args=(connection_socket,client_address)
            )
            
            client_thread.start()

if __name__ == "__main__":
    start_server()