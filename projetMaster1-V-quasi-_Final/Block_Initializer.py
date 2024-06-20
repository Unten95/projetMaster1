from Interfaces.InventoryUtility import get_last_block_number


def InitializeBlock_data():

    block_data_number= get_last_block_number("../blockchain.txt")

    # Example block data
    block_data= {
        'block number': block_data_number,
        'nonce': '123456',  # Replace with actual nonce value
        'current block hash': '',  # Empty for now
        'previous block hash': ''  # Empty for the first block
    }

    return block_data

#write_block_to_file(block_data1, 'blockchain.txt', difficulty, memory_pool_file, max_transactions, id_mine)
