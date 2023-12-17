import socket
import threading

class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[*] Serveur en écoute sur {self.host}:{self.port}")

    def handle_client(self, client_socket, addr):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            print(f"Reçu de {addr[0]}:{addr[1]} : {message}")

        client_socket.close()
        print(f"[*] Connexion fermée avec {addr[0]}:{addr[1]}")

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"[*] Connexion acceptée de {addr[0]}:{addr[1]}")

            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, addr))
            client_handler.start()

if __name__ == "__main__":
    server = Server('localhost', 12345)
    server.start()
