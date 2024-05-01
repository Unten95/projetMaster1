from BlockCreator import calculate_block_hash
from BlockReader import read_blocks_from_file

def validate_transactions_format(transactions):
    for transaction in transactions:
        # Splitting transaction data
        parts = transaction.split(',')
        if len(parts) != 5:
            print("Invalid transaction format:", transaction)
            return False

        sender_id, receiver_id, exchanged_item, sender_inventory_str, receiver_inventory_str = parts

        # Here you can add more specific checks if needed, such as verifying the sender_id

        # Extracting sender's inventory after the transaction
        sender_inventory = sender_inventory_str.strip('[]').split('|')

        # Extracting receiver's inventory after the transaction
        receiver_inventory = receiver_inventory_str.strip('[]').split('|')

        # Check if exchanged item is present in receiver's inventory
        if exchanged_item not in receiver_inventory:
            print("Recipient does not have the exchanged item:", transaction)
            return False

    print('Transactions are valid')
    return True


def recursive_list_traversal(blocks, Ajout_transaction):
    verif_1 = False
    verif_2 = False
    blocks_reversed = blocks[::-1]
    # Splitting transaction data
    parts = Ajout_transaction.split(',')
    Ajout_sender_id, Ajout_receiver_id, Ajout_exchanged_item, Ajout_sender_inventory_str, Ajout_receiver_inventory_str = parts

    # Here you can add more specific checks if needed, such as verifying the sender_id

    # Extracting sender's inventory after the transaction
    Ajout_sender_inventory = Ajout_sender_inventory_str.strip('[]').split('|')

    # Extracting receiver's inventory after the transaction
    Ajout_receiver_inventory = Ajout_receiver_inventory_str.strip('[]').split('|')

    # Traitement de l'élément actuel
    for block in blocks_reversed:
        for transaction in block.get('transactions', []):
            # Splitting transaction data
            parts = transaction.split(',')
            if len(parts) != 5:
                print("Invalid transaction format:", transaction)
                return False
            # inventaire source precedant doit contenir l'objet de la transaction a ajouter en plus
            sender_id, receiver_id, exchanged_item, sender_inventory_str, receiver_inventory_str = parts

            # Here you can add more specific checks if needed, such as verifying the sender_id

            # Extracting sender's inventory after the transaction
            sender_inventory = sender_inventory_str.strip('[]').split('|')

            # Extracting receiver's inventory after the transaction
            receiver_inventory = receiver_inventory_str.strip('[]').split('|')

            if (sender_id == Ajout_sender_id):
                if Ajout_exchanged_item in sender_inventory:
                    verif_1 = True
            if (receiver_id == Ajout_sender_id):
                if Ajout_exchanged_item in receiver_inventory:
                    verif_1 = True
            if (Ajout_receiver_id == sender_id):
                if Ajout_exchanged_item not in sender_inventory:
                    verif_2 = True
            if (Ajout_receiver_id == receiver_id):
                if Ajout_exchanged_item not in receiver_inventory:
                    verif_2 = True

            if verif_1 and verif_2:
                return True

                # Appel récursif pour l'élément

    return False

def is_valid_block(block, previous_block):
    """
    # Verify transactions in the block
    if not verify_transactions(block):
        print("test1")
        return False
    """

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



"""
--------------------------------------------
Partie test
"""


# Example Usage:
blocks = read_blocks_from_file('blockchain.txt')
"""
if is_valid_chain(blocks):
    print("Blockchain is valid.")
else:
    print("Blockchain is not valid.")
"""

# Lecture des transactions à partir du fichier MemPool.txt
with open('MemPool.txt', 'r') as file:
    transactions = file.readlines()

# Suppression des caractères de nouvelle ligne ('\n') à la fin de chaque transaction
transactions = [tx.strip() for tx in transactions]

# Validation des transactions
if validate_transactions_format(transactions):
    print("Toutes les transactions sont valides.")
else:
    print("Au moins une transaction est invalide.")



def test_recursive_list_traversal():
    # Créer une liste de blocs (simulée pour cet exemple)
    blocks = [
        {
            'transactions': [
                "Expediteur1,Destinataire1,Objet1,[Objet1|Objet2|Objet3|Objet6],[Objet4|Objet5|Objet6]",
                "Expediteur2,Destinataire3,Objet2,[Objet1|Objet2|Objet3],[Objet4|Objet5|Objet6]",
                "Expediteur3,Destinataire3,Objet3,[Objet1|Objet2|Objet3],[Objet4|Objet5]"
            ]
        },
        {
            'transactions': [
                "Expediteur4,Destinataire4,Objet4,[Objet1|Objet2|Objet3],[Objet4|Objet5|Objet6]",
                "Expediteur5,Destinataire5,Objet5,[Objet1|Objet2|Objet3],[Objet4|Objet5]"
            ]
        }
    ]

    blocks2 = read_blocks_from_file('blockchain.txt')

    # Définir une transaction à ajouter (simulée pour cet exemple)
    Ajout_transaction = "Expediteur1,Destinataire3,Objet6,[Objet1|Objet2|Objet3],[Objet4|Objet5|Objet6]"

    # Appeler la fonction pour tester
    result = recursive_list_traversal(blocks2, Ajout_transaction)

    # Afficher le résultat du test
    if result:
        print("Les inventaires sont valides.")
    else:
        print("Les inventaires ne sont pas valides.")

# Appeler la fonction de test
test_recursive_list_traversal()
