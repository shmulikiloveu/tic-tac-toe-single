import time
import socket
import pyautogui
from io import BytesIO


def start_client():
    global client_socket
    server_ip = "127.0.0.1"
    server_port = 22010

    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_ip, server_port))

            while True:
                screenshot = pyautogui.screenshot()
                buffer = BytesIO()
                screenshot.save(buffer, format="PNG")
                screenshot_bytes = buffer.getvalue()

                image_size = len(screenshot_bytes)
                client_socket.sendall(f"{image_size:08d}".encode())

                client_socket.sendall(screenshot_bytes)

                time.sleep(10)  # Wait 10 seconds before sending the next screenshot

        except Exception as e:
            print(f"Error in client: {e}")
        finally:
            client_socket.close()


start_client()
