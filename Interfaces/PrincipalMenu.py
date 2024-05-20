import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image


from inventory import Launch_Inventory
from morpion import*

def login_window(root):
    # Créer le cadre de connexion
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

    button_login = tk.Button(login_frame, text="Se connecter", command=lambda: check_login(root,entry_username, entry_password))
    button_login.grid(row=2, columnspan=2, padx=5, pady=5)


def check_login(root,entry_username, entry_password):
    # Vérifier l'identifiant et le mot de passe
    if entry_username.get() == "utilisateur" and entry_password.get() == "motdepasse":
        # Afficher la nouvelle 
        #login_frame.pack_forget()
        #main_menu_frame.pack()
        root.destroy()
        Launch_Inventory()
    else:
        # Afficher un message d'erreur si les informations de connexion sont incorrectes
        messagebox.showerror("Erreur", "Identifiant ou mot de passe incorrect")



def open_shop():
    messagebox.showinfo("Action", "Vous avez choisi d'accéder à la boutique !")

# Créer la fenêtre principale
def Auth_Interface():
    root = tk.Tk()
    root.title("Connexion")

    # Charger et redimensionner l'image
    image = Image.open("Interfaces\images\logo.png")  # Chemin vers votre image
    image = image.resize((100, 100))  # Redimensionner l'image
    image = ImageTk.PhotoImage(image)
    label_image = tk.Label(root, image=image)
    label_image.pack()
    # Créer la fenêtre de connexion
    login_window(root)


    # Centrer la fenêtre
    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)
    root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

    # Exécuter l'application
    root.mainloop()
