import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class Produit:
    def __init__(self, nom, prix, quantite, image_path):
        self.nom = nom
        self.prix = prix
        self.quantite = quantite
        self.image = Image.open(image_path)

class BoutiqueGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Boutique en ligne")

        self.produits = [
            Produit("T-shirt", 20, 10, "tshirt.png"),
            Produit("Pantalon", 40, 5, "pantalon.png"),
            Produit("Chaussures", 50, 3, "chaussures.png")
        ]

        self.liste_produits()

    def liste_produits(self):
        self.clear_frame()
        for i, produit in enumerate(self.produits):
            image = ImageTk.PhotoImage(produit.image)
            label = tk.Label(self, image=image)
            label.image = image
            label.grid(row=i, column=0)

            tk.Label(self, text=f"{produit.nom} - {produit.prix}€").grid(row=i, column=1)
            tk.Button(self, text="Acheter", command=lambda index=i: self.acheter_produit(index)).grid(row=i, column=2)

    def acheter_produit(self, index):
        produit = self.produits[index]
        if produit.quantite > 0:
            produit.quantite -= 1
            messagebox.showinfo("Achat effectué", f"Vous avez acheté {produit.nom}.")
            self.liste_produits()
        else:
            messagebox.showwarning("Rupture de stock", "Désolé, le produit est en rupture de stock.")

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = BoutiqueGUI()
    app.mainloop()
