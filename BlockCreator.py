import os
import random

from BlockReader import read_blocks_from_file
from BlockchainVerif import verify_transactions
from Calcul_hash import calculate_block_hash


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
        block_data['previous block hash'] = ''

    transactions = read_memory_pool(memory_pool_file, max_transactions)
    # Charger tous les blocs actuels pour la validation
    current_blocks = read_blocks_from_file(file_path)

    # Validation de toutes les transactions
    print("test" ,transactions)
    for tx in transactions:
        if verify_transactions(current_blocks, tx):
            print("Transactions valides")
        else:
            print(tx)
            print("Erreur de transaction")
            return




    reward_transaction = f"ExpediteurNULL,{id_mine},Recompense,[],[Recompense]"
    transactions.append(reward_transaction)

    block_data['transactions'] = transactions



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

    remove_transactions_from_memory_pool(memory_pool_file, mined_block['transactions'])



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