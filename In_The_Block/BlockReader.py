import re

def read_blocks_from_file(file_path):
    # Création d'un dictionnaire vide pour stocker les blocs
    blocks = []

    # Lecture du fichier texte
    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Initialisation du dictionnaire pour stocker les détails d'un bloc
        current_block = {
            'block number': None,
            'transactions': [],
            'nonce': None,
            'current block hash': None,
            'previous block hash': None
        }

        # Parcourir chaque ligne du fichier
        for line in lines:
        # Si la ligne indique le début d'un nouveau bloc
            if line.strip() == '#blockStart':
                # Ajouter le bloc actuel à la liste des blocs (à l'exception du premier bloc vide)
                if current_block['block number'] is not None:
                    blocks.append(current_block.copy())
                # Réinitialiser le dictionnaire pour le nouveau bloc
                current_block = {
                    'block number': None,
                    'transactions': [],
                    'nonce': None,
                    'current block hash': None,
                    'previous block hash': None
                }
            # Si la ligne contient des données de bloc
            elif line.startswith('Block Number:'):
                block_number = line.split(': ')[1].rstrip(';\n')
                current_block['block number'] = block_number
            elif line.startswith('Expediteur'):
                # Récupérer les transactions en séparant par ';'
                # Retirer les éléments vides résultants
                current_block['transactions'].append(line.rstrip(';\n'))
            elif line.startswith('Nonce:'):
                current_block['nonce'] = line.split(': ')[1].strip(';\n')
            elif line.startswith('Previous Block Hash:'):
                current_block['previous block hash'] = line.split(': ')[1].strip()
                #if  (current_block['previous block hash'] ==""):
                    #current_block['previous block hash'] = None
            elif line.startswith('Current Block Hash:'):
                current_block['current block hash'] = line.split(': ')[1].strip()

        # Ajouter le dernier bloc à la liste des blocs

        #print(current_block)
        blocks.append(current_block)


    return blocks

def display_transactions_and_hashes(blocks):
    for block in blocks:
        print("Block {}:".format(block.get('block number')))
        for transaction in block.get('transactions', []):
            print("- {}".format(transaction))
        print("Previous Block Hash: {}".format(block.get('previous block hash', )))  # Inversion
        print("Current Block Hash: {}".format(block.get('current block hash', )))    # Inversion
        print("")



# Example Usage:
#blocks = read_blocks_from_file('blockchain.txt')
#display_transactions_and_hashes(blocks)
