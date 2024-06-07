import socket
import threading
import os
import tempfile
import shutil

from Auth import authenticate_user


class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.adresses_file = "peer_addresses.txt"
        self.blockchain_file = "Blockchain.txt"
        self.peer_addresses = self.read_peer_addresses()

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

    def send_file(self, peer_host, peer_port, file_path, file_type):
        try:
            with open(file_path, 'rb') as file:
                file_data = file.read()

            prefix = b""
            if file_type == "addresses":
                prefix = b"ADDR:"
            elif file_type == "blockchain":
                prefix = b"BC:"

            data_to_send = prefix + file_data

            if peer_host == "broadcast":
                for connection in self.connections:
                    connection.sendall(data_to_send)
                print("File broadcasted successfully.")
            else:
                connection = socket.create_connection((peer_host, peer_port))
                connection.sendall(data_to_send)
                print(f"File sent to {peer_host}:{peer_port}")
                connection.close()
        except FileNotFoundError:
            print(f"File '{file_path}' not found.")
        except socket.error as e:
            print(f"Failed to send file to {peer_host}:{peer_port}. Error: {e}")

    def request_blockchain(self, peer_host, peer_port):
        try:
            connection = socket.create_connection((peer_host, peer_port))
            connection.sendall(b"REQUEST_BLOCKCHAIN")
            print(f"Blockchain request sent to {peer_host}:{peer_port}")
            connection.close()
        except socket.error as e:
            print(f"Failed to request blockchain from {peer_host}:{peer_port}. Error: {e}")

    def handle_client(self, connection, address):
        peer_ip = address[0]

        if peer_ip not in self.peer_addresses:
            with open(self.adresses_file, 'a') as file:
                file.write(peer_ip + '\n')
            self.peer_addresses.append(peer_ip)
            print(f"A new user has joined the network: {peer_ip}")
            self.send_file(peer_ip, self.port, self.adresses_file, "addresses")  # Send peer addresses file

        received_data = b""
        while True:
            try:
                data_chunk = connection.recv(1024)
                if not data_chunk:
                    break
                received_data += data_chunk
            except socket.error:
                break

        if received_data.startswith(b"ADDR:"):
            self.save_addresses_file(received_data[len(b"ADDR:"):], peer_ip)
        elif received_data.startswith(b"BC:"):
            self.save_blockchain_file(received_data[len(b"BC:"):], peer_ip)
        elif received_data == b"REQUEST_BLOCKCHAIN":
            if os.path.exists(self.blockchain_file):
                self.send_file(peer_ip, self.port, self.blockchain_file, "blockchain")  # Send blockchain file
            else:
                print(f"No blockchain file found to send to {peer_ip}")
        else:
            received_message = received_data.decode()
            print(f"Message received from {peer_ip}: {received_message}")

        print(f"Connection from {peer_ip} closed.")
        self.connections.remove(connection)
        connection.close()

    def save_addresses_file(self, file_data, peer_ip):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_data)
            temp_file_name = temp_file.name
        try:
            shutil.copy(temp_file_name, self.adresses_file)
            self.peer_addresses = self.read_peer_addresses()  # Reload addresses after saving
        finally:
            os.remove(temp_file_name)
        print(f"Peer addresses file received from {peer_ip} and saved as {self.adresses_file}")

    def save_blockchain_file(self, file_data, peer_ip):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_data)
            temp_file_name = temp_file.name
        try:
            shutil.copy(temp_file_name, self.blockchain_file)
            # If needed, implement additional handling for new blockchain data here
        finally:
            os.remove(temp_file_name)
        print(f"Blockchain file received from {peer_ip} and saved as {self.blockchain_file}")
        print("Please restart the network to start chatting.")

    def start(self):
        listen_thread = threading.Thread(target=self.listen)
        listen_thread.start()

    def get_connected_peers(self):
        connected_peers = []
        for connection in self.connections:
            peer_host, _ = connection.getpeername()
            connected_peers.append(peer_host)
        return connected_peers

    def read_peer_addresses(self):
        addresses = []
        if os.path.exists(self.adresses_file):
            with open(self.adresses_file, 'r') as file:
                for line in file:
                    address = line.strip()
                    addresses.append(address)
        return addresses


def send_option(node):
    while True:
        print("Choose an option:")
        print("1. Send a message")
        print("2. Send a file")
        print("3. Request blockchain")

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
                content = input("Enter message: ")
                for destination in node.peer_addresses:
                    peer_port = 8005
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
                file_type = input("Enter file type (addresses/blockchain): ")
                node.send_file(destination, peer_port, file_path, file_type)
            elif send_method == "2":
                file_path = input("Enter file path: ")
                file_type = input("Enter file type (addresses/blockchain): ")
                for destination in node.peer_addresses:
                    peer_port = 8005
                    node.send_file(destination, peer_port, file_path, file_type)
            else:
                print("Invalid sending method.")

        elif option == "3":
            if not os.path.exists(node.blockchain_file):
                for destination in node.peer_addresses:
                    node.request_blockchain(destination, node.port)
                print("Blockchain request sent to all peers.")
            else:
                print("Blockchain file already exists.")

        else:
            print("Invalid option. Please choose '1', '2', or '3'.")


if __name__ == "__main__":
    if authenticate_user():  # Ensure the user is authenticated before proceeding
        node1 = Peer("0.0.0.0", 8005)
        node1.start()

        send_thread = threading.Thread(target=send_option, args=(node1,))
        send_thread.start()
    else:
        print("Exiting program.")
