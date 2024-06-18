import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import json

from BlockReader import read_blocks_from_file
from Transaction_Creator import get_Inventory  # Assurez-vous d'importer correctement votre fonction get_Inventory

# Chargement des couleurs depuis le fichier
def load_colors():
    with open('colors.txt', 'r') as file:
        lines = file.readlines()
        colors = [line.strip().split('=')[1].strip().strip('"') for line in lines]
        x_colors = colors[:5]
        o_colors = colors[5:]
        return x_colors, o_colors

# Chargement des couleurs pour X et O depuis le fichier
X_COLORS, O_COLORS = load_colors()
X_COLOR = 'black'  # Par défaut, noir
O_COLOR = 'black'  # Par défaut, noir

class Morpion:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'

    def play_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        for i in range(3):
            # Vérification des lignes
            if self.board[i * 3] == self.board[i * 3 + 1] == self.board[i * 3 + 2] != ' ':
                return self.board[i * 3]
            # Vérification des colonnes
            if self.board[i] == self.board[i + 3] == self.board[i + 6] != ' ':
                return self.board[i]
        # Vérification des diagonales
        if self.board[0] == self.board[4] == self.board[8] != ' ':
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != ' ':
            return self.board[2]
        # Vérification de l'égalité
        if ' ' not in self.board:
            return 'Draw'
        return None

    def play_ai_move(self):
        # Intelligence artificielle simple : choisit la première position disponible
        empty_positions = [i for i, val in enumerate(self.board) if val == ' ']
        if empty_positions:
            position = empty_positions[0]
            self.play_move(position)
            return True
        return False

class MorpionGUI:
    def __init__(self, root,inventory_window):
        self.root = root
        self.inventory_window = inventory_window
        self.game = Morpion()
        self.buttons = []

        self.x_color = 'black'
        self.o_color = 'black'

        for i in range(3):
            for j in range(3):
                button = tk.Button(root, text='', font=('Arial', 24), width=5, height=2,
                                   command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(button)

        # Bouton Boutique
        button_shop = tk.Button(root, text="Boutique", command=self.go_to_shop)
        button_shop.grid(row=3, column=0, padx=(10, 5), pady=10)

        # Bouton Inventaire
        button_inventory = tk.Button(root, text="Inventaire", command=self.go_to_inventory)
        button_inventory.grid(row=3, column=1, padx=5, pady=10)

        # Bouton Blockchain & Mempool
        button_blockchain = tk.Button(root, text="Blockchain & Mempool", command=self.open_blockchain)
        button_blockchain.grid(row=3, column=2, padx=(5, 10), pady=10)

        # Bouton Choisir Objet (remplace Choisir Couleur)
        button_object = tk.Button(root, text="Choisir Objet", command=self.choose_object)
        button_object.grid(row=4, column=1, padx=5, pady=10)

    def make_move(self, row, col):
        position = row * 3 + col
        if self.game.play_move(position):
            self.update_board()
            winner = self.game.check_winner()
            if winner:
                if winner == 'Draw':
                    messagebox.showinfo("Fin de partie", "Match nul!")
                else:
                    messagebox.showinfo("Fin de partie", f"Le joueur {winner} a gagné!")
                self.reset_game()
            else:
                # Si le jeu n'est pas terminé, l'IA joue
                self.game.play_ai_move()
                self.update_board()
                winner = self.game.check_winner()
                if winner:
                    if winner == 'Draw':
                        messagebox.showinfo("Fin de partie", "Match nul!")
                    else:
                        messagebox.showinfo("Fin de partie", f"Le joueur {winner} a gagné!")
                    self.reset_game()

    def open_blockchain(self):
        from Interface_Blockchain import Launch_BlockchainView
        self.root.destroy()
        Launch_BlockchainView(self.inventory_window)

    def go_to_inventory(self):
        self.root.destroy()
        self.inventory_window.deiconify()

    def go_to_shop(self):
        from Inventory_Interface import Launch_Market
        self.root.destroy()
        Launch_Market(self.inventory_window)

    def choose_object(self):
        from PrincipalMenu import current_user
        # Récupérer l'inventaire de l'utilisateur
        file_path = '../Blockchain.txt'
        blocks = read_blocks_from_file(file_path)
        inventory = get_Inventory(blocks, current_user)

        if not inventory:
            messagebox.showinfo("Erreur", "Aucun inventaire trouvé pour l'utilisateur.")
            return

        # Ouvrir la fenêtre pour choisir l'objet
        ObjectSelectionGUI(self.root, inventory, self)

    def update_board(self):
        for i in range(9):
            self.buttons[i].config(text=self.game.board[i])
            if self.game.board[i] == 'X':
                self.buttons[i].config(fg=self.x_color)
            elif self.game.board[i] == 'O':
                self.buttons[i].config(fg=self.o_color)

    def reset_game(self):
        self.game = Morpion()
        self.update_board()

    def set_color(self, selected_item):
        global X_COLOR, O_COLOR
        index = int(selected_item.replace('Objet', '')) - 1
        if index < 5:
            self.x_color = X_COLORS[index]
        else:
            self.o_color = O_COLORS[index - 5]
        self.update_board()

class ObjectSelectionGUI:
    def __init__(self, root, inventory, morpion_gui):
        self.top = tk.Toplevel(root)
        self.top.title("Choisir Objet")
        self.morpion_gui = morpion_gui

        # Créer des boutons pour chaque objet de l'inventaire
        for index, item in enumerate(inventory):
            btn = tk.Button(self.top, text=item, command=lambda obj=item: self.select_object(obj))
            btn.grid(row=index, column=0, padx=10, pady=5)

    def select_object(self, selected_item):
        # Appeler la méthode pour mettre à jour la couleur du jeu de Morpion
        self.morpion_gui.set_color(selected_item)
        self.top.destroy()

def LaunchMorpion(inventory_window):
    root = tk.Tk()
    root.title("Morpion")

    tic_tac_toe_frame = tk.Frame(root)
    tic_tac_toe_frame.pack(pady=20)
    game = MorpionGUI(tic_tac_toe_frame, inventory_window)

    root.update_idletasks()

    window_width = tic_tac_toe_frame.winfo_reqwidth()
    window_height = tic_tac_toe_frame.winfo_reqheight() + 70
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)

    if y_coordinate + window_height > screen_height:
        y_coordinate = screen_height - window_height

    root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

    root.mainloop()
