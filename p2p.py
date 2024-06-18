import socket
import threading
import os
import tempfile
import shutil
from BlockCreator import write_block_to_file
from BlockReader import read_blocks_from_file
from Block_Initializer import InitializeBlock_data
from Transaction_Creator import creer_transaction
from Interfaces.InventoryUtility import extract_ip_address, get_last_block_number, read_and_extract_first_element, read_first_three_lines, write_lines_to_file,supprimer_lignes_vides
from Transaction_Creator import get_Inventory


SUPERADMIN="192.168.1.161"#lire_premiere_ligne("peer_addresses.txt")
PEER_PORT=8005
IDUSER=read_and_extract_first_element("..\credentials.txt")
class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.adresses_file = "peer_addresses.txt"
        self.blockchain_file = "../Blockchain.txt"
        self.peer_addresses = self.read_peer_addresses()
        self.inventaire = []  # Initialiser l'inventaire de l'utilisateur

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
            elif file_type == "blockchaintemp":
                prefix = b"BCT:"

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
        elif received_data.startswith(b"BCT:"):
            self.save_blockchain_file_temp(received_data[len(b"BCT:"):], peer_ip)
        elif received_data.startswith(b"BC:"):
            self.save_blockchain_file(received_data[len(b"BC:"):], peer_ip)
        elif received_data == b"REQUEST_BLOCKCHAIN":
            if os.path.exists(self.blockchain_file):
                self.send_file(peer_ip, self.port, self.blockchain_file, "blockchain")  # Send blockchain file
            else:
                print(f"No blockchain file found to send to {peer_ip}")

        elif b"start"in received_data:
                decoded_data = received_data.decode('utf-8')
                print(decoded_data)
                decoded_data=decoded_data.split("start")[1]
                print(decoded_data)
                write_lines_to_file(decoded_data,"../Mempool.txt")
                supprimer_lignes_vides("../Mempool.txt")
                block=InitializeBlock_data()
                write_block_to_file(block, "../Blockchain.txt", 4, "../Mempool.txt", 1,IDUSER)
                self.send_file(peer_ip, self.port, self.blockchain_file, "blockchain")
                


        elif b"Objet" in received_data :
            decoded_data = received_data.decode('utf-8')
            write_lines_to_file(decoded_data,"../Mempool.txt")

        elif b"Mine"in received_data:
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            print(local_ip)
            if local_ip == SUPERADMIN:
                message=read_first_three_lines("../Mempool.txt")
                decoded_data = received_data.decode('utf-8')
                ip_miner=extract_ip_address(decoded_data)
                self.send_message(ip_miner, 8005, "start"+message)
                
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

    def save_blockchain_file_temp(self,file_data, peer_ip):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(file_data)
            temp_file_name = temp_file.name
        try:
            if get_last_block_number("blockchain_temp.txt") > get_last_block_number("blockchain.txt"):
                shutil.copy(temp_file_name, "blockhain_temp.txt")
            # If needed, implement additional handling for new blockchain data here
        finally:
            os.remove(temp_file_name)
        print(f"Blockchain file received from {peer_ip} and saved as blockhain_temp.txt")

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

    def create_and_send_transaction(self,idn,objet):
        objet_echange = objet
        print(objet_echange)
        destination = idn
        print(destination)
        print("Entrez le destinataire: ")
        peer_port = int(8005)
        file_path = '../blockchain.txt'

        # Lecture des blocs depuis le fichier
        blocks = read_blocks_from_file(file_path)
        actual_inventory=get_Inventory(blocks,destination)
        print(actual_inventory)
        my_inventory = get_Inventory(blocks,read_and_extract_first_element("../credentials.txt"))
        print(my_inventory)
        transaction = creer_transaction(read_and_extract_first_element("../credentials.txt"), destination, objet_echange, my_inventory, actual_inventory)
        print(transaction)
        self.send_message(SUPERADMIN, peer_port, transaction)
        print(f"Transaction envoyée à {SUPERADMIN}:{peer_port}")

    def request(node):
        if not os.path.exists(node.blockchain_file):
            for destination in node.peer_addresses:
                node.request_blockchain(destination, node.port)
            print("Blockchain request sent to all peers.")
        else:
            print("Blockchain file already exists.")

    def mine_blockchain(node):
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        node.send_message(SUPERADMIN, PEER_PORT, str(local_ip) + ",Mine")
