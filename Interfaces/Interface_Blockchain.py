import tkinter as tk
from tkinter import scrolledtext




class FenetreAffichage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Affichage de la Blockchain et du Mempool")
        self.iconbitmap(default='info')  # Utilisation d'une icône par défaut de tkinter

        self.fichier1 = "Blockchain.txt"
        self.fichier2 = "Mempool.txt"

        self.frame_fichier1 = tk.Frame(self)
        self.frame_fichier1.pack(side=tk.LEFT, fill="both", expand=True)

        self.frame_fichier2 = tk.Frame(self)
        self.frame_fichier2.pack(side=tk.RIGHT, fill="both", expand=True)

        self.texte_fichier1 = scrolledtext.ScrolledText(self.frame_fichier1, wrap="word", width=50)
        self.texte_fichier1.pack(fill="both", expand=True)

        self.texte_fichier2 = scrolledtext.ScrolledText(self.frame_fichier2, wrap="word", width=50)
        self.texte_fichier2.pack(fill="both", expand=True)

        self.afficher_contenu()

        self.bouton_actualiser = tk.Button(self, text="Inventaire", command=self.go_to_inventory)
        self.bouton_actualiser.pack(side=tk.LEFT)

        self.bouton_actualiser = tk.Button(self, text="Jouer", command=self.play_game)
        self.bouton_actualiser.pack(side=tk.LEFT)

        # Bouton pour actualiser l'affichage des fichiers
        self.bouton_actualiser = tk.Button(self, text="Actualiser", command=self.afficher_contenu)
        self.bouton_actualiser.pack(side=tk.LEFT)

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
        from inventory import Launch_Inventory
        self.destroy()
        Launch_Inventory()

    def play_game(self):
        from morpion import LaunchMorpion
        self.destroy()
        LaunchMorpion()



def Launch_BlockchainView():
    fenetre_affichage = FenetreAffichage()
    fenetre_affichage.mainloop()

# Maintenant, vous pouvez appeler cette fonction depuis n'importe quelle partie de votre code pour lancer la fenêtre FenetreAffichage.

