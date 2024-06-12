import socket
import threading
import time
import os

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
        self.socket.listen(60)
        print(f"Listening for connections on {self.host}:{self.port}")

        while True:
            connection, address = self.socket.accept()
            self.connections.append(connection)
            print(f"Accepted connection from {address}")
            # Affichage de l'alerte pour le nouvel utilisateur
            print(f"A new user has joined the network: {address}")
            threading.Thread(target=self.handle_client, args=(connection, address)).start()

    def send_message(self, peer_host, peer_port, message):
        try:
            if peer_host == "broadcast":
                for connection in self.connections:
                    connection.sendall(message.encode())
                print("Message broadcasted successfully.")
            else:
                connection = socket.create_connection((peer_host, peer_port))
                connection.sendall(message.encode())
                print(f"Message sent to {peer_host}:{peer_port}")
                connection.close()
        except socket.error as e:
            print(f"Failed to send message to {peer_host}:{peer_port}. Error: {e}")

    def send_file(self, peer_host, peer_port, file_path):
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()

            if peer_host == "broadcast":
                for connection in self.connections:
                    connection.sendall(b"FILE:" + file_data)  # Marquage des données comme étant un fichier
                print("File broadcasted successfully.")
            else:
                connection = socket.create_connection((peer_host, peer_port))
                connection.sendall(b"FILE:" + file_data)  # Marquage des données comme étant un fichier
                print(f"File sent to {peer_host}:{peer_port}")
                connection.close()
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except socket.error as e:
            print(f"Failed to send file to {peer_host}:{peer_port}. Error: {e}")

    def handle_client(self, connection, address):
        received_data = b""
        while True:
            try:
                data_chunk = connection.recv(1024)
                if not data_chunk:
                    break
                received_data += data_chunk
            except socket.error:
                break

        if received_data.startswith(b"FILE:"):
            file_data = received_data[len(b"FILE:"):]
            file_path = f"received_file_{time.time()}.txt"  # Nom du fichier avec horodatage actuel
            with open(file_path, 'wb') as file:
                file.write(file_data)
                print(f"File received from {address} and saved as {file_path}")
        else:
            received_message = received_data.decode()
            print(f"Message received from {address}: {received_message}")

        print(f"Connection from {address} closed.")
        self.connections.remove(connection)
        connection.close()

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

    def get_connected_peers(self):
        connected_peers = []
        for connection in self.connections:
            peer_host, _ = connection.getpeername()
            connected_peers.append(peer_host)
        return connected_peers


def send_option(node):
    while True:
        print("Choose an option:")
        print("1. Send a message")
        print("2. Send a file")

        option = input("Enter the number of your choice: ")

        if option == "1":
            print("Choose sending method:")
            print("1. Send in private")
            print("2. Send to all")

            send_method = input("Enter the number of your choice: ")

            if send_method == "1":
                message = input("Enter message: ")
                destination = input("Enter peer's IP address: ")
                peer_port = int(8005)
                node.send_message(destination, peer_port, message)
            elif send_method == "2":
                destinations = ["172.20.10.9","172.20.10.10","172.20.10.8"]
                content = input("Enter message: ")
                for destination in destinations:
                    peer_port = 8005  # Port par défaut, vous pouvez ajuster si nécessaire
                    node.send_message(destination, peer_port, content)
            else:
                print("Invalid sending method.")

        elif option == "2":
            print("Choose sending method:")
            print("1. Send in private")
            print("2. Send to all")

            send_method = input("Enter the number of your choice: ")

            if send_method == "1":
                file_path = input("Enter file path: ")
                destination = input("Enter peer's IP address: ")
                peer_port = int(8005)
                node.send_file(destination, peer_port, file_path)
            elif send_method == "2":
                destinations = ["172.20.10.9","172.20.10.10","172.20.10.8"]
                content = input("Enter file path: ")
                for destination in destinations:
                    peer_port = 8005  # Port par défaut, vous pouvez ajuster si nécessaire
                    node.send_file(destination, peer_port, content)
            else:
                print("Invalid sending method.")

        else:
            print("Invalid option. Please choose '1' or '2'.")


# Exemple d'utilisation :
if __name__ == "__main__":
    node1 = Peer("0.0.0.0", 8005)
    node1.start()

    # Démarrage du thread pour choisir et envoyer un message ou un fichier
    send_thread = threading.Thread(target=send_option, args=(node1,))
    send_thread.start()
