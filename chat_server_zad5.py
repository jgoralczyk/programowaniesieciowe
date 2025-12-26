import socket

HOST = ''
PORT = 9888
BUFFER_SIZE = 1024

known_clients = set()

print(f"Nasłuchuje na porcie {PORT}")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))
    
    while True:
        message_bytes, client_address = server_socket.recvfrom(BUFFER_SIZE)
        
        if client_address not in known_clients:
            known_clients.add(client_address)
            print(f"Nowy klient: {client_address}")
            
        if message_bytes:
            print(f"Wysyłam z {client_address} do {len(known_clients) - 1}")
            
        for client in known_clients:
            
            if client != client_address:
                server_socket.sendto(message_bytes, client)
                
