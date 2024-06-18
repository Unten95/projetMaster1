import tkinter as tk
from tkinter import scrolledtext

class FenetreAffichage(tk.Tk,):
    def __init__(self,inventory_window):
        super().__init__()
        self.inventory_window = inventory_window  # Store the inventory window reference
        self.title("Affichage de la Blockchain et du Mempool")
        self.iconbitmap(default='info')  # Utilisation d'une icône par défaut de tkinter

        self.fichier1 = "../Blockchain.txt"
        self.fichier2 = "../Mempool.txt"

        self.frame_fichier1 = tk.Frame(self)
        self.frame_fichier1.pack(side=tk.LEFT, fill="both", expand=True)

        self.frame_fichier2 = tk.Frame(self)
        self.frame_fichier2.pack(side=tk.RIGHT, fill="both", expand=True)

        self.texte_fichier1 = scrolledtext.ScrolledText(self.frame_fichier1, wrap="word", width=50)
        self.texte_fichier1.pack(fill="both", expand=True)

        self.texte_fichier2 = scrolledtext.ScrolledText(self.frame_fichier2, wrap="word", width=50)
        self.texte_fichier2.pack(fill="both", expand=True)

        self.afficher_contenu()

        self.bouton_inventory = tk.Button(self, text="Inventaire", command=self.go_to_inventory)
        self.bouton_inventory.pack(side=tk.LEFT)

        self.bouton_play = tk.Button(self, text="Jouer", command=self.play_game)
        self.bouton_play.pack(side=tk.LEFT)

        # Bouton pour actualiser l'affichage des fichiers
        self.bouton_actualiser = tk.Button(self, text="Actualiser", command=self.afficher_contenu)
        self.bouton_actualiser.pack(side=tk.LEFT)

        self.center_window()

    def center_window(self):
        self.update_idletasks()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (window_width / 2))
        y_coordinate = int((screen_height / 2) - (window_height / 2))
        self.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    def afficher_contenu(self):
        self.texte_fichier1.delete('1.0', tk.END)
        try:
            with open(self.fichier1, "r") as fichier:
                contenu_texte = fichier.readlines()
                for ligne in contenu_texte:
                    if ligne.startswith("Block Number"):
                        self.texte_fichier1.insert(tk.END, ligne, 'block')
                    elif ligne.startswith("#blockEnd"):
                        self.texte_fichier1.insert(tk.END, ligne, 'normal')
                    else:
                        self.texte_fichier1.insert(tk.END, ligne)
        except FileNotFoundError:
            self.texte_fichier1.configure(state="normal")
            self.texte_fichier1.delete(1.0, tk.END)
            self.texte_fichier1.insert(tk.END, "Fichier non trouvé.")
            self.texte_fichier1.configure(state="disabled")

        self.texte_fichier2.delete('1.0', tk.END)
        try:
            with open(self.fichier2, "r") as fichier:
                contenu_texte = fichier.readlines()
                for ligne in contenu_texte:
                    if ligne.startswith("Block Number"):
                        self.texte_fichier2.insert(tk.END, ligne, 'block')
                    elif ligne.startswith("#blockEnd"):
                        self.texte_fichier2.insert(tk.END, ligne, 'normal')
                    else:
                        self.texte_fichier2.insert(tk.END, ligne)
        except FileNotFoundError:
            self.texte_fichier2.configure(state="normal")
            self.texte_fichier2.delete(1.0, tk.END)
            self.texte_fichier2.insert(tk.END, "Fichier non trouvé.")
            self.texte_fichier2.configure(state="disabled")

    def go_to_inventory(self):
        self.destroy()
        self.inventory_window.deiconify()

    def play_game(self):
        from Interface_Morpion import LaunchMorpion
        self.destroy()
        LaunchMorpion(self.inventory_window)

def Launch_BlockchainView(inventory_window):
    root=FenetreAffichage(inventory_window)
    root.mainloop()
