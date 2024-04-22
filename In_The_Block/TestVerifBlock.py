import re

def extraire_premier_objet(transaction):
    """
    Extrait le premier "Objet" suivi d'un chiffre rencontré dans la transaction.

    Args:
        transaction (str): La chaîne représentant la transaction.

    Returns:
        str: Le premier "Objet" suivi d'un chiffre rencontré dans la transaction, ou None si aucun n'est trouvé.
    """
    # Utiliser une expression régulière pour trouver le premier "Objet" suivi d'un chiffre
    match = re.search(r'Objet\d', transaction)
    if match:
        return match.group()
    else:
        return None

def verifier_presence_objet(transaction):
    """
    Vérifie si le premier "Objet" suivi d'un chiffre rencontré dans la transaction est présent dans la suite de la transaction.

    Args:
        transaction (str): La chaîne représentant la transaction.

    Returns:
        bool: True si le premier "Objet" suivi d'un chiffre rencontré est présent dans la suite de la transaction, False sinon.
    """
    # Extraire le premier "Objet" de la transaction
    premier_objet = extraire_premier_objet(transaction)
    
    if premier_objet:
        # Trouver l'index du premier "Objet" dans la transaction complète
        index_premier_objet = transaction.find(premier_objet)
        
        # Extraire la suite de la transaction après le premier "Objet"
        suite_transaction = transaction[index_premier_objet + len(premier_objet):]
        
        # Vérifier si le premier "Objet" est présent dans la suite de la transaction
        return premier_objet in suite_transaction
    else:
        # Aucun "Objet" trouvé dans la transaction
        return False

def verifier_presence_objet_dans_bloc(block):
    """
    Vérifie si le premier "Objet" de chaque transaction dans le bloc est présent dans la suite de chaque transaction.

    Args:
        block (dict): Le bloc contenant les transactions.

    Returns:
        dict: Un dictionnaire indiquant pour chaque transaction si le premier "Objet" est présent dans la suite.
    """
    resultats = {}
    
    # Parcourir chaque transaction dans le bloc
    for transaction in block['transactions']:
        resultats[transaction] = verifier_presence_objet(transaction)
    
    return resultats
