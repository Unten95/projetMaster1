from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def hash_password(password):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password.encode('utf-8'))
    return digest.finalize()

def verify_credentials(username, password):
    try:
        with open("credentials.txt", "r") as file:
            for line in file:
                stored_username, stored_hashed_password = line.strip().split(",")
                if username == stored_username and hash_password(password) == bytes.fromhex(stored_hashed_password):
                    return True
    except FileNotFoundError:
        return False  # Retourne False si le fichier n'existe pas
    return False

def register_user(username, password):
    with open("credentials.txt", "a") as file:
        # Utilisation de SHA-256 pour stocker un hachage sécurisé du mot de passe
        hashed_password = hash_password(password).hex()
        file.write(f"{username},{hashed_password}\n")
    print("Utilisateur enregistré avec succès.")

def main():
    identification = True
    while identification:
        choice = input("1. S'identifier\n2. S'enregistrer\n3. Quitter\nChoix : ")

        if choice == "1":
            username = input("Nom d'utilisateur : ")
            password = input("Mot de passe : ")
            if verify_credentials(username, password):
                print("Connexion réussie.")
                identification = False
            else:
                print("Nom d'utilisateur ou mot de passe incorrect.")
        elif choice == "2":
            username = input("Nom d'utilisateur : ")
            password = input("Mot de passe : ")
            if not verify_credentials(username, password):
                register_user(username, password)
            else:
                print("Cet utilisateur existe déjà.")
        elif choice == "3":
            break
        else:
            print("Choix invalide. Veuillez entrer 1, 2 ou 3.")

if __name__ == "__main__":
    main()