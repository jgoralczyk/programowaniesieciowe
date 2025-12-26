import socket

HOST = ''
PORT = 9876
BUF_SIZ = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    
    try:
        client_socket.connect((HOST, PORT))
        
        message = f"Wiadomość dla servera"
        
        client_socket.send(message.encode('utf-8'))
        
        data= client_socket.recv(BUF_SIZ)
        
        resposne = data.decode('utf-8')
        
        print(f"Odpowiedź od serwera {resposne}")
        
    except socket.error as e:
        print(f"Błąd połączenia: {e}")
        
print("Klient zakończył działąnie i zamknął połączenie")        
        


