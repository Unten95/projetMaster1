from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def hash_password(password):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password.encode('utf-8'))
    return digest.finalize()

def verify_credentials(username, password):
    try:
        with open("../credentials.txt", "r") as file:
            for line in file:
                stored_username, stored_hashed_password = line.strip().split(",")
                if username == stored_username and hash_password(password) == bytes.fromhex(stored_hashed_password):
                    return True
    except FileNotFoundError:
        return False  # Return False if the file does not exist
    return False

def register_user(username, password):
    with open("../credentials.txt", "a") as file:
        # Use SHA-256 to store a secure hash of the password
        hashed_password = hash_password(password).hex()
        file.write(f"{username},{hashed_password}\n")
    print("User registered successfully.")

def authenticate_user():
    identification = True
    while identification:
        choice = input("1. Log in\n2. Register\n3. Quit\nChoice: ")

        if choice == "1":
            username = input("Username: ")
            password = input("Password: ")
            if verify_credentials(username, password):
                print("Login successful.")
                return True  # User is authenticated
            else:
                print("Incorrect username or password.")
        elif choice == "2":
            username = input("Username: ")
            password = input("Password: ")
            if not verify_credentials(username, password):
                register_user(username, password)
            else:
                print("This user already exists.")
        elif choice == "3":
            return False  # Exit the program
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")