import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk

from Interface_Blockchain import Launch_BlockchainView
from morpion import LaunchMorpion
from InventaireUtility import list_files_in_directory

class InventoryGUI:
    def __init__(self, root, inventory):
        self.root = root
        self.inventory = inventory
        #print(self.inventory)

        # Créer une liste des noms des images
        self.item_listbox = tk.Listbox(root, width=50, height=10 )
        for item in self.inventory:
            self.item_listbox.insert(tk.END, item)  # Insérer les noms des images
        self.item_listbox.grid(row=0, column=0, padx=10, pady=10)
        self.item_listbox.bind('<<ListboxSelect>>', self.display_selected_image)  # Lier un gestionnaire d'événements à la sélection de la liste

        # Ajouter une barre de défilement à la liste
        self.scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.item_listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)

        self.item_listbox.config(yscrollcommand=self.scrollbar.set)

        self.display_image_label = tk.Label(root)
        self.display_image_label.grid(row=1, column=0, padx=10, pady=10)

        # Boutons pour aller à la boutique et jouer
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=2, column=0, padx=10, pady=10)

        self.button_shop = tk.Button(self.button_frame, text="Boutique", command=self.go_to_shop)
        self.button_shop.pack(side=tk.LEFT, padx=5)

        self.button_play = tk.Button(self.button_frame, text="Jouer", command=self.play_game)
        self.button_play.pack(side=tk.LEFT, padx=5)

        self.button_play = tk.Button(self.button_frame, text="Blockchain & Mempool View", command=self.open_blockchain)
        self.button_play.pack(side=tk.LEFT, padx=5)

    def display_selected_image(self, event):
        selected_index = self.item_listbox.curselection()  # Obtenir l'index de l'élément sélectionné
        if selected_index:
            selected_image_path = self.inventory[selected_index[0]]  # Récupérer le chemin de l'image sélectionnée
            image = Image.open("Interfaces\\inventaire\\" + selected_image_path)
            image = image.resize((100, 100))  # Redimensionner l'image pour l'aperçu
            photo = ImageTk.PhotoImage(image)
            self.display_image_label.config(image=photo)
            self.display_image_label.image = photo

    def go_to_shop(self):
        print("Aller à la boutique")

    def play_game(self):
        self.root.destroy()
        LaunchMorpion()

    def open_blockchain(self):
        self.root.destroy()
        Launch_BlockchainView()

        

def Launch_Inventory():
    root = tk.Tk()
    root.title("Inventaire")

    # Liste d'exemple d'images (chemins vers les fichiers)
    inventory = list_files_in_directory("Interfaces\\inventaire")

    # Centrer la fenêtre
    window_width = 400
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)
    root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

    # Créer l'interface de l'inventaire
    inventory_gui = InventoryGUI(root, inventory)

    root.mainloop()
