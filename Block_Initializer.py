# Define the difficulty (number of leading zeros required)
from BlockCreator import write_block_to_file


difficulty = 5  # Adjust this value based on your requirements

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