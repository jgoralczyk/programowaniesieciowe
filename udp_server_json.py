import socket
import json
import time

HOST = ''
PORT = 9876
BUFSIZ = 1024
ADDR = (HOST, PORT)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as socket:
    socket.bind(ADDR)

    while True:
        message_bytes, client_address = socket.recvfrom(BUFSIZ)
        message = message_bytes.decode('utf-8')
        print(f'Received from {client_address}: {message}')

        data_to_send = {
            "status": "OK",
            "received_message": message,
            "server_timestamp": time.time(),
            "client_address": client_address
        }

        # Serializacja słownika do stringa w formacie JSON json.dumps > dump string
        response_json_string = json.dumps(data_to_send)

        response_bytes = response_json_string.encode('utf-8')

        socket.sendto(response_bytes, client_address)
        