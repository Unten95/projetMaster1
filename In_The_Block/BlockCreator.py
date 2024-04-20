import hashlib

from BlockReader import read_blocks_from_file


def calculate_block_hash(block_data):
    block_string = ""
    for key in sorted(block_data.keys()):
        if key != 'current block hash':
            block_string += "{}:{};".format(key, block_data[key])
    return hashlib.sha256(block_string.encode()).hexdigest()


def mine_block(block, difficulty):
    """
    Mine a block until a valid nonce is found.

    Args:
    - block: Dictionary representing the block to mine.
    - difficulty: Integer representing the number of leading zeros required in the block hash.

    Returns:
    - The mined block with the valid nonce.
    """
    # Initialize nonce
    nonce = 0

    # Construct the prefix for the target hash based on the difficulty
    prefix = '0' * difficulty

    # Calculate the initial block hash
    block['current block hash'] = calculate_block_hash(block)

    # Keep mining until a valid nonce is found
    while block['current block hash'][:difficulty] != prefix:
        # Increment nonce
        nonce += 1

        # Update the nonce in the block
        block['nonce'] = str(nonce)

        # Print the block data for debugging
        #print("Data used for hashing:", block)

        # Recalculate the block hash
        block['current block hash'] = calculate_block_hash(block)

    return block


def write_block_to_file(block_data, file_path, difficulty):
    # Add previous block hash line
    if block_data['block number'] != 1:
        previous_block_data = read_blocks_from_file(file_path)[-1]
        previous_block_hash = previous_block_data['current block hash']
        block_data['previous block hash'] = previous_block_hash
    else:
        print("This is the first block. Using empty hash for previous block.")
        block_data['previous block hash'] = ''

    # Mine the block
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

"""
# Define the difficulty (number of leading zeros required)
difficulty = 5  # Adjust this value based on your requirements

# Example block data
block_data1 = {
    'block number': 1,
    'transactions': ['Tx1'],
    'nonce': '123456',  # Replace with actual nonce value
    'current block hash': '',  # Empty for now
    'previous block hash': ''  # Empty for the first block
}

block_data2 = {
    'block number': 2,
    'transactions': ['Tx2'],
    'nonce': '789012',  # Replace with actual nonce value
    'current block hash': '',  # Empty for now
    'previous block hash': ''  # Provide the hash of the previous block
}

# Write block data to file
write_block_to_file(block_data1, 'blockchain.txt', difficulty)
write_block_to_file(block_data2, 'blockchain.txt', difficulty)
"""