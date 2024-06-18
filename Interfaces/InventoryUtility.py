import os
import re


def read_and_extract_all_elements(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]


def list_files_in_directory(directory):
    """
    Recherche tous les fichiers dans un dossier donné et retourne une liste des chemins de ces fichiers.

    Args:
    - directory: Le chemin du dossier à rechercher.

    Returns:
    - Une liste contenant les chemins de tous les fichiers trouvés dans le dossier.
    """
    file_paths = []
    # Vérifie si le chemin fourni est un dossier existant
    if os.path.isdir(directory):
        # Parcours tous les éléments dans le dossier
        for filename in os.listdir(directory):
            # Vérifie si l'élément est un fichier
            if os.path.isfile(os.path.join(directory, filename)):
                # Ajoute le chemin complet du fichier à la liste
                file_paths.append(os.path.join(filename))
    else:
        print("Le chemin spécifié n'est pas un dossier valide.")
    return file_paths


def read_and_extract_first_element(file_path):
    with open(file_path, 'r') as file:
        content = file.read().strip()  # Read the file and remove leading/trailing whitespace
        first_element = content.split(',')[0]  # Split the content by comma and take the first part
    return first_element


def lire_premiere_ligne(nom_fichier):
    try:
        with open(nom_fichier, 'r') as fichier:
            premiere_ligne = fichier.readline().strip()  # Lire la première ligne et retirer les espaces
        return premiere_ligne
    except FileNotFoundError:
        return "Le fichier n'existe pas."
    except Exception as e:
        return f"Une erreur est survenue: {e}"


def add_transaction(nom_fichier, nouvelle_ligne):
    """
    Ajoute une ligne à la fin du fichier si elle n'est pas déjà présente.

    :param nom_fichier: Nom du fichier (chemin complet si nécessaire).
    :param nouvelle_ligne: Ligne à ajouter au fichier.
    """
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            lignes_existantes = fichier.read().splitlines()

        if nouvelle_ligne in lignes_existantes:
            print("La ligne est déjà présente dans le fichier.")
        else:
            with open(nom_fichier, 'a', encoding='utf-8') as fichier:
                fichier.write(nouvelle_ligne)
            print("Ligne ajoutée avec succès.")

    except FileNotFoundError:
        # Si le fichier n'existe pas, on le crée et on ajoute la nouvelle ligne
        with open(nom_fichier, 'w', encoding='utf-8') as fichier:
            fichier.write(nouvelle_ligne)
        print("Fichier créé et ligne ajoutée avec succès.")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


def read_first_three_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        premiere_ligne = file.readline()  # Lire la première ligne et retirer les espaces
    return premiere_ligne


def write_lines_to_file(lines_string, output_file_path):
    lines = lines_string.split('\n')
    if lines_string.strip():  # Vérifie si le string n'est pas vide
        with open(output_file_path, 'a', encoding='utf-8') as file:
            for line in lines:
                file.write(line + '\n')


def supprimer_lignes_vides(nom_fichier):
    # Lire toutes les lignes du fichier
    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()

    # Filtrer les lignes non vides
    lignes_non_vides = [ligne for ligne in lignes if ligne.strip()]

    # Écrire les lignes non vides dans le fichier
    with open(nom_fichier, 'w') as fichier:
        fichier.writelines(lignes_non_vides)


def enlever_transaction(filename,string_to_remove):
    with open(filename, 'r') as file:
         lines = file.readlines()

    # Remove the specified string from each line and filter out empty lines
    cleaned_lines = [line.replace(string_to_remove, '').strip() for line in lines if line.strip()]

    with open(filename, 'w') as file:
        file.write("\n".join(cleaned_lines))


def vider_first_line(output_file_path):
    # Lire toutes les lignes du fichier
    with open(output_file_path, 'r') as fichier:
        lignes = fichier.readlines()

    # Écrire les lignes sauf la première dans le fichier
    with open(output_file_path, 'w') as fichier:
        fichier.writelines(lignes[1:])

def extract_ip_address(message):
    ip_address = message.split(',')[0]
    return ip_address


def get_last_block_number(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Regex pattern to find block numbers
    block_pattern = re.compile(r'Block Number: (\d+);')
    blocks = block_pattern.findall(content)

    if not blocks:
        print("No blocks found.")
        return None

    last_block_number = int(blocks[-1])
    return last_block_number + 1


"""
file_path = 'Blockchain.txt'
last_block_number = get_last_block_number(file_path)
print(last_block_number)
"""

# Exemple d'utilisation
# message = "191.168.151.1,Mine"
# ip_address = extract_ip_address(message)
# print(ip_address)  # Devrait afficher: 191.168.151.1


# Exemple d'utilisation :
# add_transaction('mon_fichier.txt', 'Ceci est un nouveau texte.')


# Exemple d'utilisation
# nom_fichier = 'votre_fichier.txt'
# premiere_ligne = lire_premiere_ligne(nom_fichier)
# print(premiere_ligne)

# Exemple d'utilisation
# file_path = 'credentials.txt'  # Remplacez par le chemin réel de votre fichier
# first_element = read_and_extract_first_element(file_path)
# print(f"Le premier élément est : {first_element}")  # Output: "Le premier élément est : Unten95"


# Exemple d'utilisation :
# directory_path = "chemin/vers/votre/dossier"
# file_paths = list_files_in_directory(directory_path)
# print("Liste des fichiers dans le dossier :", file_paths)