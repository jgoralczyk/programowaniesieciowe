import socket

HOST = ''
PORT = 9876
BUFFER_SIZE = 1024

print(f"Serwer UDP zad1 nasłuchuje na porcie {PORT}...")

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST,PORT))
    
    while True:
        try:
            message_bytes, client_address = server_socket.recvfrom(BUFFER_SIZE)
        
            message = message_bytes.decode('utf-8')
            print(f'Otrzymano od {client_address}: {message}')
        
            response_message = message[::-1]
        
            #kodowanie odwróconego stringa spowrotem na bajty
            response_bytes = response_message.encode('utf-8')
            
            #odsyłanie do klienta
            server_socket.sendto(response_bytes, client_address)
        except Exception as e:
            print(f"Błąd: {e}")
    