import socket

class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        print(f"[*] Connecté au serveur {self.host}:{self.port}")

    def send_message(self, message):
        self.client_socket.send(message.encode('utf-8'))

    def close_connection(self):
        self.client_socket.close()

if __name__ == "__main__":
    client = Client('localhost', 12345)

    while True:
        message = input("Envoyer un message (ou 'exit' pour quitter) : ")
        if message.lower() == 'exit':
            break
        client.send_message(message)

    client.close_connection()
