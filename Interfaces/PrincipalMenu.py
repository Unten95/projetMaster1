import os
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

from Inventory_Interface import Launch_Inventory

# Chemin vers le fichier des identifiants
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), '../credentials.txt')

# Variable globale pour stocker l'identifiant de l'utilisateur connecté
current_user = None

def hash_password(password):
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(password.encode('utf-8'))
    return digest.finalize()

def verify_credentials(username, password):
    try:
        with open(CREDENTIALS_FILE, "r") as file:
            for line in file:
                stored_username, stored_hashed_password = line.strip().split(",")
                if username == stored_username and hash_password(password).hex() == stored_hashed_password:
                    return True
    except FileNotFoundError:
        return False  # Retourner False si le fichier n'existe pas
    return False

def register_user(username, password):
    with open(CREDENTIALS_FILE, "a") as file:
        hashed_password = hash_password(password).hex()
        file.write(f"{username},{hashed_password}\n")

def login_window(root):
    login_frame = tk.Frame(root)
    login_frame.pack(pady=20)

    label_username = tk.Label(login_frame, text="Identifiant :")
    label_username.grid(row=0, column=0, padx=5, pady=5)
    entry_username = tk.Entry(login_frame)
    entry_username.grid(row=0, column=1, padx=5, pady=5)

    label_password = tk.Label(login_frame, text="Mot de passe :")
    label_password.grid(row=1, column=0, padx=5, pady=5)
    entry_password = tk.Entry(login_frame, show="*")
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    button_login = tk.Button(login_frame, text="Se connecter", command=lambda: check_login(root, entry_username, entry_password))
    button_login.grid(row=2, columnspan=2, padx=5, pady=5)

    button_register = tk.Button(login_frame, text="S'enregistrer", command=lambda: open_register_window(root))
    button_register.grid(row=3, columnspan=2, padx=5, pady=5)

def check_login(root, entry_username, entry_password):
    global current_user  # Utilisation de la variable globale
    username = entry_username.get()
    if verify_credentials(username, entry_password.get()):
        current_user = username  # Enregistrer l'identifiant de l'utilisateur connecté
        root.destroy()
        Launch_Inventory()  # Remplacez par la fonction réelle pour lancer l'inventaire
    else:
        messagebox.showerror("Erreur", "Identifiant ou mot de passe incorrect")

def open_register_window(root):
    register_window = tk.Toplevel(root)
    register_window.title("S'enregistrer")

    label_new_username = tk.Label(register_window, text="Nouvel identifiant :")
    label_new_username.grid(row=0, column=0, padx=5, pady=5)
    entry_new_username = tk.Entry(register_window)
    entry_new_username.grid(row=0, column=1, padx=5, pady=5)

    label_new_password = tk.Label(register_window, text="Nouveau mot de passe :")
    label_new_password.grid(row=1, column=0, padx=5, pady=5)
    entry_new_password = tk.Entry(register_window, show="*")
    entry_new_password.grid(row=1, column=1, padx=5, pady=5)

    button_register = tk.Button(register_window, text="S'enregistrer", command=lambda: save_user(register_window, entry_new_username, entry_new_password))
    button_register.grid(row=2, columnspan=2, padx=5, pady=5)

def save_user(register_window, entry_new_username, entry_new_password):
    new_username = entry_new_username.get()
    new_password = entry_new_password.get()
    if new_username and new_password:
        if not verify_credentials(new_username, new_password):
            register_user(new_username, new_password)
            messagebox.showinfo("Succès", "Enregistrement réussi")
            register_window.destroy()
        else:
            messagebox.showerror("Erreur", "Cet utilisateur existe déjà.")
    else:
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs")

def Auth_Interface():
    root = tk.Tk()
    root.title("Connexion")

    image = Image.open("images/logo.png")  # Chemin vers votre image
    image = image.resize((100, 100))
    image = ImageTk.PhotoImage(image)
    label_image = tk.Label(root, image=image)
    label_image.pack()

    login_window(root)

    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)
    root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

    root.mainloop()
