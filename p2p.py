import socket
import threading
import time

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []

    def connect(self, peer_host, peer_port):
        try:
            connection = socket.create_connection((peer_host, peer_port))
            self.connections.append(connection)
            print(f"Connected to {peer_host}:{peer_port}")
        except socket.error as e:
            print(f"Failed to connect to {peer_host}:{peer_port}. Error: {e}")

    def listen(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(10)
        print(f"Listening for connections on {self.host}:{self.port}")

        while True:
            connection, address = self.socket.accept()
            self.connections.append(connection)
            print(f"Accepted connection from {address}")
            threading.Thread(target=self.handle_client, args=(connection, address)).start()

    def send_data(self, peer_host, peer_port, data):
        try:
            connection = socket.create_connection((peer_host, peer_port))
            connection.sendall(data.encode())
            print(f"Data sent to {peer_host}:{peer_port}")
            time.sleep(0.1)  # Ajout d'un court délai pour permettre la fermeture de la connexion
            connection.close()
        except socket.error as e:
            print(f"Failed to send data to {peer_host}:{peer_port}. Error: {e}")

    def handle_client(self, connection, address):
        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                print(f"Received data from {address}: {data.decode()}")
            except socket.error:
                break

        print(f"Connection from {address} closed.")
        self.connections.remove(connection)
        connection.close()

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

# Fonction pour la saisie du message
def send_message(node):
    while True:
        message = input("Enter message: ")
        if not message:
            continue
        node.send_data("172.20.10.2", 8005, message)
        node.send_data("172.20.10.4", 8005, message)
        #node.send_data("10.77.95.27", 8005, message)

# Exemple d'utilisation :
if __name__ == "__main__":
    node1 = Peer("0.0.0.0", 8005)
    node1.start()

    # Démarrage du thread pour saisir et envoyer des messages
    send_thread = threading.Thread(target=send_message, args=(node1,))
    send_thread.start()