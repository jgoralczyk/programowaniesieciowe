import socket


SERVER_HOST = 'localhost'
SERVER_PORT = 9876
BUFFER_SIZE = 1024

MESSAGE = "Cześć, serwerze UDP!"

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    
    server_address = (SERVER_HOST, SERVER_PORT)
    
    try:
        message_bytes = MESSAGE.encode('utf-8')
        
        client_socket.sendto(message_bytes, server_address)
        print(f"Wysłano do serwera: {MESSAGE}")
        
        response_bytes, _ = client_socket.recvfrom(BUFFER_SIZE)
        
        response = response_bytes.decode('utf-8')
        print(f"odpowiedź serwera: {response}")
    
    except Exception as e:
        print(f"Błąd komunikacji z serwerem: {e}")