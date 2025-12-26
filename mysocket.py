import socket
import json
import time
import threading


HOST = ''
PORT = 2137
BUF_SIZ = 1024

known_clients = set()

# Zmień:
def mes_receiver(sock: socket):
    while True:
        # Ten wątek robi WSZYSTKO: odbiera, loguje, przetwarza, odpowiada
        data_bytes, client_address = sock.recvfrom(BUF_SIZ) 
        message = data_bytes.decode('utf-8')
        
        if client_address not in known_clients:
            known_clients.add(client_address)
            print(f"LOG - new client {client_address}")
            
        print(f"Otrzymane: {message}")
        
        # ... (reszta Twojego kodu do tworzenia i wysyłania etykiety)
        etykieta = {
            'status': 'OK',
            'host': HOST, # Pamiętaj: to jest HOST serwera
            'port': PORT,
            'server_time': time.time()
        }
        etykieta_jsonstr = (json.dumps(etykieta)).encode("utf-8")
        sock.sendto(etykieta_jsonstr, client_address)

# A wątek główny nie ma już swojej pętli while:
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.bind((HOST, PORT))
    
    reciver_thread = threading.Thread(target= mes_receiver, args= (server,), daemon=True)
    reciver_thread.start()
    
    # Wątek główny czeka na zakończenie (lub Ctrl+C)
    while True:
        time.sleep(1) # Po prostu czeka, aż wątek odbierający wykona swoją pracę