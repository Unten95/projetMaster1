from BlockCreator import calculate_block_hash
from BlockReader import read_blocks_from_file

def is_valid_block(block, previous_block):
    # Calculate block hash
    block_hash = calculate_block_hash(block)
    #print(block)
    #print(block_hash)
    #print(block.get('current block hash'))
    # Check if block hash is correct
    if block_hash != block.get('current block hash'):
        #print(block_hash)
        #print(block.get('current block hash'))
        return False

    # Check if previous block hash matches
    if previous_block is not None and block.get('previous block hash') != previous_block.get('current block hash'):
        return False

    return True


def is_valid_chain(blocks):
    # Initialize previous block as None for the first block
    previous_block = None

    # Iterate through blocks and verify each one
    for block in blocks:
        if not is_valid_block(block, previous_block):
            return False
        previous_block = block

    return True


# Example Usage:
blocks = read_blocks_from_file('blockchain.txt')
if is_valid_chain(blocks):
    print("Blockchain is valid.")
else:
    print("Blockchain is not valid.")
