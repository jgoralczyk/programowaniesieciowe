import socket
import threading
import sys
import os

def receive_message(sock):
    """
    FUnkcja działa w wątku w tle i odbiera wiadomości
    """
    
    while True:
        try:
            data_bytes = sock.recv(1024)
            
            if not data_bytes:
                #Serwer grzecznie zamknął połączenie (np. serwer się wyłączył)
                print("\n[ROZŁĄCZONO] Serwer zamknął połączenie.")
                print("Naciśnij Enter, aby wyjść...")
                sock.close()
                os._exit(0) # Wymusza zamknięcie całego programu (obu wątków)
                
            message = data_bytes.decode('utf-8')
            
            print(f"\r{message}\nTy:", end="")
            
        except socket.error as e:
            print(f"[BłĄD] Utracono połączenie z serwerem: {e}")
            sock.close()
            os._exit(0)
            
def send_message(sock):
    """ 
    Ta funkcja działa w głównym wątku i tylko wysyła wiadomości
    """
    
    while True:
        try:
            
            message = input("Ty: ")
            if message.lower() == 'exit':
                print("Rozłączanie...")
                break
            
            sock.send(message.encode("utf-8"))
            
        except (socket.error, EOFError, KeyboardInterrupt):
            print("\nZamykanie klienta...")
            break
        
    sock.close()
    
#Główna część programu
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        
        server_address = ('localhost', 9876)
        print(f"łączenie z serwerem {server_address}...")
        client_socket.connect(server_address)
        print("Połączono z serwerem, wpisz exit aby wyjść")
        
        receiver_thread = threading.Thread(
            target=receive_message,
            args=(client_socket,),
            daemon=True #wątek umrze z głównym programem
        )
        
        #uruchamianie wątku
        receiver_thread.start()
        
        #Główny wątek wysyła
        send_message(client_socket)

except socket.error as e:
    print(f"[BŁĄD] Nie można połączyć się z serwerem: {e}")
except KeyboardInterrupt:
    print("\nWyjście z programu.")
finally:
    print("Zakończono.")
        