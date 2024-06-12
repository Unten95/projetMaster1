import tkinter as tk
import random
from PIL import Image, ImageTk

class MorpionGUI:
    def __init__(self, root):
        self.root = root
        self.current_player = "X"  # Joueur actuel (X ou O)

        # Chargement des images de croix et de rond
        self.cross_image = Image.open("inventaire\\blueCross.png").resize((50, 50))
        self.circle_image = Image.open("inventaire\\blueCross.png").resize((50, 50))

        # Convertir les images en images Tkinter pour affichage sur le canevas
        self.cross_image_tk = ImageTk.PhotoImage(self.cross_image)
        self.circle_image_tk = ImageTk.PhotoImage(self.circle_image)

        # Création du canevas pour le morpion
        self.canvas = tk.Canvas(root, width=150, height=150, bg="white")
        self.canvas.pack()

        # Dessiner la grille de Morpion
        for i in range(1, 3):
            self.canvas.create_line(i * 50, 0, i * 50, 150, fill="black", width=2)
            self.canvas.create_line(0, i * 50, 150, i * 50, fill="black", width=2)

        # Appeler la méthode pour commencer la partie
        self.play_next_move()

    def place_image(self, row, col):
        # Placement de l'image correspondant au joueur actuel dans la case spécifiée
        image_tk = self.cross_image_tk if self.current_player == "X" else self.circle_image_tk
        self.canvas.create_image(col * 50 + 25, row * 50 + 25, image=image_tk, anchor="center")
        # Changement du joueur actuel
        self.current_player = "O" if self.current_player == "X" else "X"

    def play_next_move(self):
        # Si c'est le tour de l'IA
        if self.current_player == "O":
            self.play_ai_move()
        else:
            # Laisser l'utilisateur jouer
            self.canvas.bind("<Button-1>", self.user_click)

    def user_click(self, event):
        # Calculer la case où l'utilisateur a cliqué
        row, col = event.y // 50, event.x // 50
        # Vérifier si la case est vide
        if self.canvas.find_withtag(f"{row}_{col}") == ():
            # Placer l'image du joueur actuel dans la case
            self.place_image(row, col)
            # Passer au prochain tour
            self.play_next_move()

    def play_ai_move(self):
        # Trouver les cases vides
        empty_cells = [(row, col) for row in range(3) for col in range(3) if self.canvas.find_withtag(f"{row}_{col}") == ()]
        if empty_cells:
            for row, col in empty_cells:
                # Vérifier si l'IA peut gagner en jouant dans cette case
                if self.check_win(row, col, self.current_player):
                    self.place_image(row, col)
                    return
            for row, col in empty_cells:
                # Vérifier si l'IA doit bloquer l'adversaire en jouant dans cette case
                if self.check_win(row, col, "X" if self.current_player == "O" else "O"):
                    self.place_image(row, col)
                    return
            # Si aucune stratégie particulière n'est applicable, sélectionnez une case au hasard
            row, col = random.choice(empty_cells)
            self.place_image(row, col)
        # Passer au prochain tour
        self.play_next_move()

    def check_win(self, row, col, player):
        # Vérifier si le joueur spécifié peut gagner en jouant dans cette case
        for i in range(3):
            if self.canvas.find_withtag(f"{row}_{i}") == () or self.canvas.find_withtag(f"{i}_{col}") == ():
                continue
            if all([self.canvas.itemcget(cell, "image") == self.cross_image_tk if player == "X" else self.circle_image_tk for cell in self.canvas.find_withtag(f"{row}_{i}")]) or \
               all([self.canvas.itemcget(cell, "image") == self.cross_image_tk if player == "X" else self.circle_image_tk for cell in self.canvas.find_withtag(f"{i}_{col}")]):
                return True
        if row == col:
            if all([self.canvas.itemcget(cell, "image") == self.cross_image_tk if player == "X" else self.circle_image_tk for cell in self.canvas.find_withtag(f"{i}_{i}")]):
                return True
        if row + col == 2:
            if all([self.canvas.itemcget(cell, "image") == self.cross_image_tk if player == "X" else self.circle_image_tk for cell in self.canvas.find_withtag(f"{i}_{2-i}")]):
                return True
        return False

def Launch_Morpion():
    root = tk.Tk()
    root.title("Morpion")

    # Créer l'interface graphique du Morpion
    morpion_game = MorpionGUI(root)

    root.mainloop()
