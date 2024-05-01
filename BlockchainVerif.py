from BlockCreator import calculate_block_hash
from BlockReader import read_blocks_from_file

def verify_transactions(block):
    transactions = block.get('transactions', [])

    for transaction in transactions:
        # Splitting transaction data
        parts = transaction.split(',')
        if len(parts) != 4:
            print("Invalid transaction format:", transaction)
            return False

        sender_id, receiver_id, items_str, sender_inventory_str = parts

        # Extracting items from the items_str
        items = items_str.strip('[]').split('|')

        # Extracting sender's inventory from the sender_inventory_str
        sender_inventory = sender_inventory_str.strip('[]').split('|')

        print("Sender's inventory:", sender_inventory)

        # Check if sender has the exchanged items in their inventory
        for item in items:
            print("Checking item:", item)
            if item not in sender_inventory:
                print("Sender does not have the exchanged item:", transaction)
                return False

        # Here you can add more checks if needed, such as verifying the receiver_id
    print('tx are valids')
    return True



def is_valid_block(block, previous_block):
    # Verify transactions in the block
    if not verify_transactions(block):
        print("test1")
        return False

    # Calculate block hash
    block_hash = calculate_block_hash(block)

    # Check if block hash is correct
    if block_hash != block.get('current block hash'):
        print("test2")
        return False

    # Check if previous block hash matches
    if previous_block is not None and block.get('previous block hash') != previous_block.get('current block hash'):
        print("test3")
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