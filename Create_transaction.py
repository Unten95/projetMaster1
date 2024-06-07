from BlockReader import *

def get_Inventory(blocks, user_id):
    blocks_reversed = blocks[::-1]
    # Splitting transaction data
    for block in blocks_reversed:
        #print("test")
        #print(block)
        for transaction in block.get('transactions', []):
            #print("test2")
            parts = transaction.split(',')

            # inventaire source precedant doit contenir l'objet de la transaction a ajouter en plus
            sender_id, receiver_id, exchanged_item, sender_inventory_str, receiver_inventory_str = parts
            #print("sender id =" ,sender_id)
            #print("receiver id =" , receiver_id)
            if sender_id == user_id:
                return sender_inventory_str.strip('[]').split('|')
            if receiver_id == user_id:
                return receiver_inventory_str.strip('[]').split('|')

    return None

def creer_transaction(id_source, id_dest, objet_echange, inventaire_source, inventaire_dest):
    # Vérifier si l'objet échangé est dans l'inventaire de l'expéditeur
    if objet_echange not in inventaire_source:
        inventaire_source.append(objet_echange)

    # Retirer l'objet échangé de l'inventaire de l'expéditeur
    if objet_echange in inventaire_source:
        inventaire_source.remove(objet_echange)

    # Ajouter l'objet échangé à l'inventaire du destinataire
    inventaire_dest.append(objet_echange)

    # Convertir les listes d'objets en chaînes avec des crochets
    inventaire_source_str = f"[{'|'.join(inventaire_source)}]"
    inventaire_dest_str = f"[{'|'.join(inventaire_dest)}]"

    # Créer la transaction sous forme de chaîne
    transaction = f"{id_source},{id_dest},{objet_echange},{inventaire_source_str},{inventaire_dest_str}"

    return transaction


# Chemin du fichier blockchain
file_path = 'blockchain.txt'

# Lecture des blocs depuis le fichier
blocks = read_blocks_from_file(file_path)

# Identifiants des utilisateurs et inventaires correspondants
user_id_source = 'id7'
user_id_dest = 'id8'

# Récupération des inventaires des utilisateurs depuis la blockchain
inventory_source = get_Inventory(blocks, user_id_source)
inventory_dest = get_Inventory(blocks, user_id_dest)

print(inventory_source)
print(inventory_dest)

# Objet à échanger
item_to_exchange = 'Objet7'

# Création de la transaction
transaction = creer_transaction(user_id_source, user_id_dest, item_to_exchange, inventory_source, inventory_dest)

# Affichage de la transaction créée
print("Transaction créée:")
print(transaction)