import random

def creer_transactions(nom_fichier):
    transactions = []
    for i in range(1, 16):
        id_source = f"Expediteur{i}"
        id_dest = f"Destinataire{i+1}"
        objet_echange = f"Objet{i}"

        # Créer des listes d'objets pour l'expéditeur et le destinataire
        inventaire_source = [f"Objet{i}" for i in range(1, 4)]
        inventaire_dest = [f"Objet{i}" for i in range(4, 7)]

        # Ajouter l'objet échangé à l'inventaire du destinataire
        inventaire_dest.append(objet_echange)

        # Convertir les listes d'objets en chaînes avec des crochets
        inventaire_source_str = f"[{'|'.join(inventaire_source)}]"
        inventaire_dest_str = f"[{'|'.join(inventaire_dest)}]"

        # Ajouter la transaction à la liste des transactions
        transactions.append((id_source, id_dest, objet_echange, inventaire_source_str, inventaire_dest_str))

    with open(nom_fichier, 'w') as fichier:
        for transaction in transactions:
            ligne = ','.join(transaction) + '\n'
            fichier.write(ligne)


# Utilisation de la fonction pour créer un fichier "MemPool.txt"
creer_transactions("MemPool.txt")