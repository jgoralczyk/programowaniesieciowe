import socket

HOST = ''
PORT = 9876
BUF_SIZ = 1024
client_list = []

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as server:
    server.bind((HOST,PORT))
    
    server.listen(5)
    
    conection_socket, client_address = server.accept()  
    
    with conection_socket:
        print(f'połączono z client address: {client_address}')
    
        while True:
            data = conection_socket.recv(BUF_SIZ)
            
            if not data:
                print(f"Klient {client_address} zamknął połączenie")
                break
        
            message = data.decode('utf-8')
            
            print(f"Otrzymano wiadomość od {client_address} : {message}")
            
            response = f"Serwer TCP otrzymał wiadomość od {client_address}"
            
            conection_socket.send(response.encode('utf-8'))

print("Serwer zakończył działanie")
