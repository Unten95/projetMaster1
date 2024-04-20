import random

def creer_transactions(nom_fichier):
    transactions = []
    for _ in range(16):
        exp = f"Expediteur{_}"
        dest = f"Destinataire{_}"
        echange = f"Objet{_}"
        objets = [f"Objet{i}" for i in range(1, 4)]
        objets_str = f"[{', '.join(objets)}]"  # Convertir la liste d'objets en une chaîne avec des crochets
        transactions.append((exp, dest,echange, objets_str))
    
    with open(nom_fichier, 'w') as fichier:
        for transaction in transactions:
            ligne = ','.join(transaction) + '\n'
            fichier.write(ligne)

# Utilisation de la fonction pour créer un fichier "MemPool.txt"
creer_transactions("MemPool.txt")

