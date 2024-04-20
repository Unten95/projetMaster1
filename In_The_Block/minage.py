from BlockCreator import calculate_block_hash


def mine_block(previous_block, transactions):
    # Convertir le numéro de bloc précédent en entier avant d'ajouter 1
    block_number = int(previous_block['block number']) + 1

    # Définir la difficulté du minage
    difficulty = 4

    # Initialiser le nonce à zéro
    nonce = 0

    # Concaténer le bloc précédent avec les transactions
    block_data = {
        'block number': block_number,
        'transactions': transactions,
        'nonce': nonce,
        'previous block hash': previous_block['current block hash'],  # Utiliser le hachage du bloc précédent
        'current block hash': ''
    }

    # Calculer le hachage du bloc en utilisant le nonce
    block_hash = calculate_block_hash(block_data)

    # Tant que le hachage ne respecte pas la difficulté, incrémenter le nonce et recalculer le hachage
    while not block_hash.startswith('0' * difficulty):
        nonce += 1
        block_data['nonce'] = nonce
        block_hash = calculate_block_hash(block_data)

    # Une fois que le hachage respecte la difficulté, mettre à jour le hachage du bloc
    block_data['current block hash'] = block_hash

    return block_data