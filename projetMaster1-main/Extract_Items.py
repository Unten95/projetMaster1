def parse_transaction(line):
    parts = line.split(',')
    expediteur = parts[0]
    destinataire = parts[1]
    objet = parts[2]
    objets_list1 = parts[3].strip('[]').split('|')
    # Retirer les deux derniers caractères de la dernière chaîne dans objets_list2
    objets_list2 = [item[:-2] if i == len(parts[4].split('|')) - 1 else item for i, item in enumerate(parts[4].strip('[]').split('|'))]
    return expediteur, destinataire, objet, objets_list1, objets_list2



def process_file(filename):
    expediteurs_destinataires = {}
    with open(filename, 'r') as file:
        lines = file.readlines()

    in_block = False
    seen_expedit_dest = set()  # To keep track of seen (expediteur, destinataire)

    for line in reversed(lines):
        line = line.strip()
        if line.startswith('#blockEnd'):
            in_block = True
        elif line.startswith('#blockStart'):
            in_block = False
        elif in_block and line.startswith('ID') and not line.startswith('ExpediteurNULL'):
            expediteur, destinataire, objet, objets_list1, objets_list2 = parse_transaction(line)
            key = (expediteur, destinataire)
            if key not in seen_expedit_dest:
                seen_expedit_dest.add(key)
                expediteurs_destinataires[key] = {
                    'objet': objet,
                    'expediteur_objets_list1': objets_list1,
                    'expediteur_objets_list2': objets_list2,
                    'destinataire_objets_list1': objets_list1,
                    'destinataire_objets_list2': objets_list2
                }

    return expediteurs_destinataires

# Exemple d'utilisation
filename = 'Blockchain.txt'
result = process_file(filename)

for key, value in result.items():
    print(f"{key[0]} {value['expediteur_objets_list1']}")
    print(f"{key[1]} {value['expediteur_objets_list2']}")
