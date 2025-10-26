import socket


HOST = '' # pusty string, aby nasłuchiwał na wszysystkich inte
PORT = 9876
BUFFER_SIZE = 1024

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))
    print(f'Serwer UDP nasłuchuje na porcie {PORT}...')
    
    while True:
        try:
            message_bytes, client_address = server_socket.recvfrom(BUFFER_SIZE)
            
            message = message_bytes.decode('utf-8')
            print(f"Otrzymano do {client_address}: {message}")
            
            response = f"Serwer otrzymał: {message}"
            
            response_bytes = response.encode('utf-8')
            
            server_socket.sendto(response_bytes, client_address)
            
        except Exception as e:
            print(f"Wystąpił błąd: {e}")
