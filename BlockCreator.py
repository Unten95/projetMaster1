import os
import random

from BlockReader import read_blocks_from_file
from BlockchainVerif import verify_transactions
from Calcul_hash import calculate_block_hash
from Create_transaction import blocks
from Interfaces.InventoryUtility import enlever_transaction
from Transaction_Creator import get_Inventory


def mine_block(block, difficulty):
    nonce = 0
    prefix = '0' * difficulty
    block['current block hash'] = calculate_block_hash(block)

    while block['current block hash'][:difficulty] != prefix:
        nonce = random.randint(0, 2**32 - 1)
        block['nonce'] = str(nonce)
        block['current block hash'] = calculate_block_hash(block)

    return block


def write_block_to_file(block_data, file_path, difficulty, memory_pool_file, max_transactions, id_mine):
    if block_data['block number'] != 1:
        previous_block_data = read_blocks_from_file(file_path)[-1]
        previous_block_hash = previous_block_data['current block hash']
        block_data['previous block hash'] = previous_block_hash
    else:
        print("This is the first block. Using empty hash for previous block.")
        block_data['previous block hash'] = '0'

    transactions = read_memory_pool(memory_pool_file, max_transactions)
    # Charger tous les blocs actuels pour la validation
    current_blocks = read_blocks_from_file(file_path)

    print(current_blocks)
    # Validation de toutes les transactions
    #print("test" ,transactions)
    for tx in transactions:
        if verify_transactions(current_blocks, tx):
            print("Transactions valides")
        else:
            print(tx)
            print("Erreur de transaction")
            enlever_transaction("../Mempool.txt", tx)
            return

    tx = transactions[0]
    print(tx)
    parts = tx.split(',')
    Ajout_sender_id, Ajout_receiver_id, Ajout_exchanged_item, Ajout_sender_inventory_str, Ajout_receiver_inventory_str = parts

    if Ajout_sender_id == id_mine :
        print("test 1")
        possible_rewards = ["Objet1", "Objet2", "Objet3", "Objet4", "Objet5", "Objet6", "Objet7", "Objet8",
                            "Objet9", "Objet10"]
        reward = random.choice(possible_rewards)
        # reward_transaction = f"idNULL,{id_mine},{reward},[],[{id_mine}|{reward}]"
        inventory = Ajout_sender_inventory_str.strip('[]').split('|')

        if inventory is None:
            inventory = []

        inventory_str = '|'.join(inventory + [reward])
        reward_transaction = f"idNULL,{id_mine},{reward},[],[{inventory_str}]"
        transactions.append(reward_transaction)

    elif Ajout_receiver_id == id_mine :
        print("test 2")
        possible_rewards = ["Objet1", "Objet2", "Objet3", "Objet4", "Objet5", "Objet6", "Objet7", "Objet8",
                            "Objet9", "Objet10"]
        reward = random.choice(possible_rewards)
        # reward_transaction = f"idNULL,{id_mine},{reward},[],[{id_mine}|{reward}]"
        inventory = Ajout_receiver_inventory_str.strip('[]').split('|')

        if inventory is None:
            inventory = []

        inventory_str = '|'.join(inventory + [reward])
        reward_transaction = f"idNULL,{id_mine},{reward},[],[{inventory_str}]"
        transactions.append(reward_transaction)

    else:
        possible_rewards = ["Objet1", "Objet2", "Objet3", "Objet4", "Objet5", "Objet6", "Objet7", "Objet8",
                            "Objet9", "Objet10"]
        reward = random.choice(possible_rewards)
        # reward_transaction = f"idNULL,{id_mine},{reward},[],[{id_mine}|{reward}]"
        inventory = get_Inventory(blocks, id_mine)

        if inventory is None:
            inventory = []

        inventory_str = '|'.join(inventory + [reward])
        reward_transaction = f"idNULL,{id_mine},{reward},[],[{inventory_str}]"
        transactions.append(reward_transaction)


    print(transactions)

    block_data['transactions'] = transactions
    print(block_data['block number'])


    mined_block = mine_block(block_data, difficulty)

    with open(file_path, 'a') as file:
        file.write("#blockStart\n")
        file.write(f"Block Number: {mined_block['block number']};\n")
        file.write("Transactions:;\n")
        for transaction in mined_block['transactions']:
            file.write(f"{transaction};\n")
        file.write(f"Nonce: {mined_block['nonce']};\n")
        file.write(f"Previous Block Hash: {mined_block['previous block hash']}\n")
        file.write(f"Current Block Hash: {mined_block['current block hash']}\n")
        file.write("#blockEnd\n")

    remove_transactions_from_memory_pool("Mempool.txt", mined_block['transactions'])



def read_memory_pool(memory_pool_file, max_transactions):
    transactions = []
    if os.path.exists(memory_pool_file):
        with open(memory_pool_file, 'r') as file:
            transactions = file.readlines()
    return [transaction.strip() for transaction in transactions[:max_transactions]]


def remove_transactions_from_memory_pool(memory_pool_file, transactions):
    if os.path.exists(memory_pool_file):
        with open(memory_pool_file, 'r') as file:
            lines = file.readlines()

        with open(memory_pool_file, 'w') as file:
            for line in lines:
                if line.strip() not in transactions:
                    file.write(line)

"""
# Define the difficulty (number of leading zeros required)
difficulty = 4  # Adjust this value based on your requirements

max_transactions = 1

id_mine = "idTest"

# Memory pool file path
memory_pool_file = 'MemPool.txt'


# Example block data
block_data1 = {
    'block number': 1,
    'nonce': '123456',  # Replace with actual nonce value
    'current block hash': '',  # Empty for now
    'previous block hash': ''  # Empty for the first block
}

block_data2 = {
    'block number': 2,
    'nonce': '789012',  # Replace with actual nonce value
    'current block hash': '',  # Empty for now
    'previous block hash': ''  # Provide the hash of the previous block
}

block_data3 = {
    'block number': 3,
    'nonce': '789012',  # Replace with actual nonce value
    'current block hash': '',  # Empty for now
    'previous block hash': ''  # Provide the hash of the previous block
}

block_data4 = {
    'block number': 4,
    'nonce': '789012',  # Replace with actual nonce value
    'current block hash': '',  # Empty for now
    'previous block hash': ''  # Provide the hash of the previous block
}

# Write block data to file
write_block_to_file(block_data1, 'blockchain.txt', difficulty, memory_pool_file, max_transactions, id_mine)
write_block_to_file(block_data2, 'blockchain.txt', difficulty, memory_pool_file, max_transactions, id_mine)
write_block_to_file(block_data3, 'blockchain.txt', difficulty, memory_pool_file, max_transactions, id_mine)
write_block_to_file(block_data4, 'blockchain.txt', difficulty, memory_pool_file, max_transactions, id_mine)
"""