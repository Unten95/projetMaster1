# Define the difficulty (number of leading zeros required)
from BlockCreator import write_block_to_file
from Interfaces.InventoryUtility import get_last_block_number, read_and_extract_first_element

def InitializeBlock_data():
    difficulty = 4 # Adjust this value based on your requirements

    max_transactions = 2

    id_mine = read_and_extract_first_element("credential.txt")

    # Memory pool file path
    memory_pool_file = 'MemPool.txt'

    block_data_number= get_last_block_number("blockchain.txt")

    # Example block data
    block_data1 = {
        'block number': block_data_number,
        'nonce': '123456',  # Replace with actual nonce value
        'current block hash': '',  # Empty for now
        'previous block hash': ''  # Empty for the first block
    }

    return block_data1

#write_block_to_file(block_data1, 'blockchain.txt', difficulty, memory_pool_file, max_transactions, id_mine)
