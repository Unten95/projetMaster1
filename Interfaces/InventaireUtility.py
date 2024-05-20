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

# Exemple d'utilisation :
#directory_path = "chemin/vers/votre/dossier"
#file_paths = list_files_in_directory(directory_path)
#print("Liste des fichiers dans le dossier :", file_paths)
