import os

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


# Exemple d'utilisation :
#add_transaction('mon_fichier.txt', 'Ceci est un nouveau texte.')


# Exemple d'utilisation
#nom_fichier = 'votre_fichier.txt'
#premiere_ligne = lire_premiere_ligne(nom_fichier)
#print(premiere_ligne)

#Exemple d'utilisation
#file_path = 'credentials.txt'  # Remplacez par le chemin réel de votre fichier
#first_element = read_and_extract_first_element(file_path)
#print(f"Le premier élément est : {first_element}")  # Output: "Le premier élément est : Unten95"


# Exemple d'utilisation :
#directory_path = "chemin/vers/votre/dossier"
#file_paths = list_files_in_directory(directory_path)
#print("Liste des fichiers dans le dossier :", file_paths)