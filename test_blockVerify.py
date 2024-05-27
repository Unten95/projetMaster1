from BlockchainVerif import *


"""
--------------------------------------------
Partie test
"""
"""

# Example Usage:
blocks = read_blocks_from_file('blockchain.txt')




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

if is_valid_chain(blocks) == -1 :
    print("Blockchain non valide")
else:
    print("longueur de la blockchain : " ,is_valid_chain(blocks))
