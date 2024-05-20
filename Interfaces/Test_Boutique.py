import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

class Morpion(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jeu de Morpion")

        self.player_symbol = ""
        self.ai_symbol = ""
        self.current_player = ""
        self.board = [['' for _ in range(3)] for _ in range(3)]

        self.choose_symbol()

    def choose_symbol(self):
        self.symbol_window = tk.Toplevel(self)
        self.symbol_window.title("Choix du symbole")
        label = tk.Label(self.symbol_window, text="Choisissez votre symbole :")
        button_cross = tk.Button(self.symbol_window, text="Croix", command=lambda: self.start_game("cross"))
        button_circle = tk.Button(self.symbol_window, text="Cercle", command=lambda: self.start_game("circle"))
        label.pack(pady=10)
        button_cross.pack(pady=5)
        button_circle.pack(pady=5)

    def start_game(self, symbol):
        self.player_symbol = symbol
        self.ai_symbol = "circle" if symbol == "cross" else "cross"
        self.current_player = "cross"
        self.symbol_window.destroy()
        self.create_board()

    def create_board(self):
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self, text='', font=('Arial', 30), width=3, height=1,
                                                command=lambda row=i, col=j: self.on_button_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

        # Si l'IA commence, elle joue le premier coup
        if self.ai_symbol == "cross":
            self.ai_play()

    def on_button_click(self, row, col):
        if self.board[row][col] == '':
            self.board[row][col] = self.player_symbol
            self.draw_symbol(row, col, self.player_symbol)
            if self.check_winner(row, col):
                messagebox.showinfo("Victoire", "Vous avez gagné !")
                self.ask_play_again()
            elif self.check_draw():
                messagebox.showinfo("Match nul", "Match nul !")
                self.ask_play_again()
            else:
                self.current_player = self.ai_symbol
                self.ai_play()

    def ai_play(self):
        # Chercher une case vide aléatoire pour l'IA
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == '']
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.board[row][col] = self.ai_symbol
            self.draw_symbol(row, col, self.ai_symbol)
            if self.check_winner(row, col):
                messagebox.showinfo("Défaite", "Vous avez perdu !")
                self.ask_play_again()
            elif self.check_draw():
                messagebox.showinfo("Match nul", "Match nul !")
                self.ask_play_again()
            else:
                self.current_player = self.player_symbol

    def draw_symbol(self, row, col, symbol):
        try:
            if symbol == "cross":
                image = Image.open("Interfaces/images/green-circle.png")
            else:
                image = Image.open("Interfaces/images/red-cross.jpg")
            image = image.resize((100, 50))  # Ajustez la taille au besoin
            photo = ImageTk.PhotoImage(image)
            self.buttons[row][col].config(image=photo)
            self.buttons[row][col].image = photo
        except Exception as e:
            print("Erreur lors du chargement de l'image:", e)


    def check_winner(self, row, col):
        # Vérifier la ligne
        if self.board[row][0] == self.board[row][1] == self.board[row][2] == self.current_player:
            return True
        # Vérifier la colonne
        if self.board[0][col] == self.board[1][col] == self.board[2][col] == self.current_player:
            return True
        # Vérifier les diagonales
        if row == col:
            if self.board[0][0] == self.board[1][1] == self.board[2][2] == self.current_player:
                return True
        if row + col == 2:
            if self.board[0][2] == self.board[1][1] == self.board[2][0] == self.current_player:
                return True
        return False

    def check_draw(self):
        for row in self.board:
            for cell in row:
                if cell == '':
                    return False
        return True

    def reset_board(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(image='', text='')
                self.board[i][j] = ''
        if self.ai_symbol == "cross":
            self.ai_play()

    def ask_play_again(self):
        answer = messagebox.askyesno("Nouvelle partie", "Voulez-vous jouer à nouveau ?")
        if answer:
            self.reset_board()
        else:
            self.destroy()

if __name__ == "__main__":
    app = Morpion()
    app.mainloop()
