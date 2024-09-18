from Calcul_hash import calculate_block_hash
from BlockReader import read_blocks_from_file


def validate_transactions_format(transaction):
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
    if exchanged_item not in receiver_inventory_str:
        print("Recipient does not have the exchanged item:", transaction)
        return False

    #print('Transactions are valid')
    return True


def verify_transactions(blocks, Ajout_transaction):
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

    Add_trans = Ajout_transaction
    if not (validate_transactions_format(Add_trans)):
        print("trans suivante invalide : ", Add_trans)
        return
    else:
        print("Transactions suivante valide :" , Add_trans)
    # Traitement de l'élément actuel
    for block in blocks_reversed:
        for transaction in block.get('transactions', []):
            if not (validate_transactions_format(transaction)):
                print("trans suivante invalide : " ,transaction)
                return
            #print("test 1," ,transaction)
            #print("test 2," , Add_trans)
            if transaction == Add_trans:
                print("trans suivante invalide : ", transaction)
                return
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

            #print("pppp =" ,parts)
            if (sender_id == Ajout_sender_id):
                # print(sender_id)
                # print(Ajout_sender_id)
                # print(Ajout_sender_inventory)
                # print(sender_inventory)
                if Ajout_exchanged_item in sender_inventory:
                    #print("test 1")
                    sender_inventory.remove(Ajout_exchanged_item)
                    if (len(Ajout_sender_inventory)) == len(sender_inventory):
                        print("1 je rentre dans la comparaison Ajout sender sender")
                        for element in sender_inventory:
                            #print("comp : ",element)
                            if element in Ajout_sender_inventory:
                                #print("New inv : ", Ajout_sender_inventory)
                                #print("Old inv : ", sender_inventory)
                                Ajout_sender_inventory.remove(element)
                                #print("New inv 2 : ", Ajout_sender_inventory)
                                #print("Old inv 2 : ", sender_inventory)
                        if len(Ajout_sender_inventory) == 0:
                            verif_1 = True
                            print("1 = ok")

            if (receiver_id == Ajout_sender_id):
                #print("test 2")
                if Ajout_exchanged_item in receiver_inventory:
                    receiver_inventory.remove(Ajout_exchanged_item)
                    if len(receiver_inventory) == (len(Ajout_sender_inventory)):
                        print("2 je rentre dans la comparaison recceiver Ajout sender")
                        for element in receiver_inventory:
                            if element in Ajout_sender_inventory:
                                Ajout_sender_inventory.remove(element)
                                #print(Ajout_sender_inventory)
                        if len(Ajout_sender_inventory) == 0:
                            verif_1 = True

            if (Ajout_receiver_id == sender_id):
                #print("test 3")
                #print(Ajout_exchanged_item)
                #print(sender_inventory)
                #if Ajout_exchanged_item not in Ajout_sender_inventory:
                if (len(Ajout_receiver_inventory) - 1) == len(sender_inventory):
                    print("3 je rentre dans la comparaison Ajout_receiver sender")
                    for element in Ajout_receiver_inventory:
                        if element in sender_inventory:
                            sender_inventory.remove(element)
                            #print(sender_inventory)
                    if len(sender_inventory) == 0:
                        #print("3 ok")
                        verif_2 = True

            if (Ajout_receiver_id == receiver_id):
                #print("test 4")
                #print(Ajout_exchanged_item)
                #print(Ajout_receiver_inventory)
                if Ajout_exchanged_item in Ajout_receiver_inventory:
                    if (len(Ajout_receiver_inventory) - 1) == len(receiver_inventory):
                        print("4 je rentre dans la comparaison Ajout receiver reciver")
                        for element in Ajout_receiver_inventory:
                            if element in receiver_inventory:
                                #print("10", Ajout_receiver_inventory)
                                #print("20", receiver_inventory)
                                receiver_inventory.remove(element)
                                #print(receiver_inventory)
                        if len(receiver_inventory) == 0:
                            verif_2 = True
                            print("4 = ok")

            if verif_1 and verif_2:
                return True
            # print ("1",verif_1)
            # print(verif_2)
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
    #print('block hash 1 =',block_hash)
    #print("block 1 =" ,block)

    # Check if block hash is correct
    if block_hash != block.get('current block hash'):
        #print('block hash2 =',block_hash)
        #print('block get =',block.get('current block hash'))
        #print("test2")
        return False

    # Check if previous block hash matches
    if previous_block is not None and block.get('previous block hash') != previous_block.get('current block hash'):
        print("test3")
        return False

    return True


def is_valid_chain(blocks):
    # Initialize previous block as None for the first block
    previous_block = None

    # Initialize blockchain length
    blockchain_length = 0

    # Iterate through blocks and verify each one
    for block in blocks:
        #print("test" ,block)
        # Verify the block
        if not is_valid_block(block, previous_block):
            # If any block is invalid, return -1
            #print("brobleme")
            #print(block)
            #print(previous_block)
            return -1
        # Increment blockchain length
        blockchain_length += 1
        # Update previous block
        previous_block = block

    # Return the length of the blockchain
    return blockchain_length


"""
--------------------------------------------
Partie test
"""


# Example Usage:
#blocks = read_blocks_from_file('blockchain.txt')
"""
if is_valid_chain(blocks):
    print("Blockchain is valid.")
else:
    print("Blockchain is not valid.")


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



"""
"""
def test_recursive_list_traversal():

    blocks2 = read_blocks_from_file('blockchain.txt')

    # Définir une transaction à ajouter (simulée pour cet exemple)
    #[Objet1 | Objet2 | Objet6], [Objet4 | Objet5 | Objet2 | Objet3]
    Ajout_transaction = ("Expediteur1,Destinataire3,Objet1,[Objet2|Objet3],[Objet4|Objet5|Objet6|Objet2|Objet1]")
    #[Objet4|Objet5|Objet6],[Objet1|Objet2|Objet3|Objet1]
    #Ajout_transaction = "Destinataire2,Expediteur4,Objet1,[Objet4|Objet5|Objet6],[Objet1|Objet2|Objet3|Objet1]"

    # Appeler la fonction pour tester
    result = verify_transactions(blocks2, Ajout_transaction)


    # Afficher le résultat du test
    if result:
        print("Les inventaires sont valides.")
    else:
        print("Les inventaires ne sont pas valides.")

# Appeler la fonction de test
test_recursive_list_traversal()
"""
"""
if is_valid_chain(blocks) == -1 :
    print("Blockchain non valide")
else:
    print("longueur de la blockchain : " ,is_valid_chain(blocks))
"""