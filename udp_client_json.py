import socket
import json
import time

HOST = ''
PORT = 2137
BUFSIZ = 1024
ADDR = (HOST, PORT)


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    MESSAGE = "Prosze o dane json"
    server_address = (HOST, PORT)


    try:
        message_bytes = MESSAGE.encode('utf-8')
        client_socket.sendto(message_bytes,server_address)
        print(f"Wysłano {MESSAGE}")

        response_bytes, _ = client_socket.recvfrom(BUFSIZ)

        response_json_string = response_bytes.decode('utf-8')

        data_received = json.loads(response_json_string)

        print("Odebrano json:\n")
        print(data_received)

        print(f"Status od serwera: {data_received['status']}")
        print(f"Serwer otrzymał: {data_received['server_time']}")
        
        data_received['status'] = 'back'
        
        data_send = (json.dumps(data_received)).encode('utf-8')
        
        client_socket.sendto(data_send, server_address)
        

    except Exception as e:
        print(f"Bład komunikacji z serwerem: {e}")

