from BlockReader import read_blocks_from_file
from BlockchainVerif import is_valid_block, validate_transactions_format, is_valid_chain

"""
--------------------------------------------
Partie test
"""


# Example Usage:
#blocks = read_blocks_from_file('blockchain.txt')

#if is_valid_chain(blocks):
    #print("Blockchain is valid.")
#else:
    #print("Blockchain is not valid.")


# Lecture des transactions à partir du fichier MemPool.txt
with open('MemPool.txt', 'r') as file:
    transactions = file.readlines()

# Suppression des caractères de nouvelle ligne ('\n') à la fin de chaque transaction
transactions = [tx.strip() for tx in transactions]

# Validation des transactions
if validate_transactions_format(transactions):
    pass
    #print("Toutes les transactions sont valides.")
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
    #Ajout_transaction = "Expediteur1,Destinataire12,Objet1,[Objet2|Objet3],[Objet1|Objet4|Objet5|Objet6|Objet11]"
    Ajout_transaction = "Destinataire12,Expediteur1,Objet4,[Objet5|Objet6|Objet11],[Objet4|Objet1|Objet2|Objet3]"
    # Appeler la fonction pour tester
    result = is_valid_block(blocks2, Ajout_transaction)

    # Afficher le résultat du test
    if result==True:
        print("Les inventaires sont valides.")
    else:
        print("Les inventaires ne sont pas valides.")

# Appeler la fonction de test
test_recursive_list_traversal()