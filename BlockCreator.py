import hashlib
import os
import random

from BlockReader import read_blocks_from_file


def calculate_block_hash(block_data):
    block_string = ""
    for key in sorted(block_data.keys()):
        if key != 'current block hash':
            block_string += "{}:{};".format(key, block_data[key])
    return hashlib.sha256(block_string.encode()).hexdigest()


def mine_block(block, difficulty):
    # Initialize nonce
    nonce = 0

    # Construct the prefix for the target hash based on the difficulty
    prefix = '0' * difficulty

    # Calculate the initial block hash
    block['current block hash'] = calculate_block_hash(block)

    # Keep mining until a valid nonce is found
    while block['current block hash'][:difficulty] != prefix:
        # Increment nonce
        nonce = random.randint(0, 2**32 - 1)

        # Update the nonce in the block
        block['nonce'] = str(nonce)

        # Recalculate the block hash
        block['current block hash'] = calculate_block_hash(block)

    return block


def write_block_to_file(block_data, file_path, difficulty, memory_pool_file, max_transactions, id_mine):
    # Add previous block hash line
    if block_data['block number'] != 1:
        previous_block_data = read_blocks_from_file(file_path)[-1]
        previous_block_hash = previous_block_data['current block hash']
        block_data['previous block hash'] = previous_block_hash
    else:
        print("This is the first block. Using empty hash for previous block.")
        block_data['previous block hash'] = ''

    # Get transactions from the memory pool
    transactions = read_memory_pool(memory_pool_file, max_transactions)

    # Add the reward transaction
    reward_transaction = "ExpediteurNULL,{},{},[{}]".format(id_mine, "Recompense", "Recompense")
    transactions.append(reward_transaction)

    # Mine the block
    block_data['transactions'] = transactions
    mined_block = mine_block(block_data, difficulty)

    with open(file_path, 'a') as file:
        file.write("#blockStart\n")
        file.write("Block Number: {};\n".format(mined_block['block number']))
        file.write("Transactions:;\n")
        for transaction in mined_block['transactions']:
            file.write("{};\n".format(transaction))
        file.write("Nonce: {};\n".format(mined_block['nonce']))
        file.write("Previous Block Hash: {}\n".format(mined_block['previous block hash']))

        # Write the current block hash as the last line
        file.write("Current Block Hash: {}\n".format(mined_block['current block hash']))

        file.write("#blockEnd\n")

    # Remove transactions from the memory pool
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


# Define the difficulty (number of leading zeros required)
difficulty = 4  # Adjust this value based on your requirements

max_transactions = 3

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
