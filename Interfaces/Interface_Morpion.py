import random
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image


class Morpion:
    def __init__(self):
        self.board = [' ']*9
        self.current_player = 'X'

    def play_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        for i in range(3):
            # Check rows
            if self.board[i*3] == self.board[i*3+1] == self.board[i*3+2] != ' ':
                return self.board[i*3]
            # Check columns
            if self.board[i] == self.board[i+3] == self.board[i+6] != ' ':
                return self.board[i]
        # Check diagonals
        if self.board[0] == self.board[4] == self.board[8] != ' ':
            return self.board[0]
        if self.board[2] == self.board[4] == self.board[6] != ' ':
            return self.board[2]
        # Check for draw
        if ' ' not in self.board:
            return 'Draw'
        return None

    def play_ai_move(self):
        # L'IA choisit une position aléatoire non occupée
        empty_positions = [i for i, val in enumerate(self.board) if val == ' ']
        if empty_positions:
            position = random.choice(empty_positions)
            self.play_move(position)
            return True
        return False
    
class MorpionGUI:
    def __init__(self, root):
        self.root = root
        self.game = Morpion()
        self.buttons = []


        for i in range(3):
            for j in range(3):
                button = tk.Button(root, text='', font=('Arial', 24), width=5, height=2,
                                   command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i, column=j, padx=5, pady=5)
                self.buttons.append(button)

         # Bouton Boutique
        button_shop = tk.Button(root, text="Boutique", command=self.go_to_shop)
        button_shop.grid(row=3, column=0, padx=(10, 5), pady=10)  # Utilisation de padx pour l'espacement sur la longueur

        # Bouton Inventaire
        button_inventory = tk.Button(root, text="Inventaire", command=self.go_to_inventory)
        button_inventory.grid(row=3, column=1, padx=5, pady=10)

        # Bouton Blockchain & Mempool
        button_blockchain = tk.Button(root, text="Blockchain & Mempool", command=self.open_blockchain)
        button_blockchain.grid(row=3, column=2, padx=(5, 10), pady=10)




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
        Launch_BlockchainView()

    def go_to_inventory(self):
        from Interfaces.Inventory_Interface import Launch_Inventory
        self.root.destroy()
        Launch_Inventory()

    def go_to_shop(self):
        from Inventory_Interface import Launch_Market
        self.root.destroy()
        Launch_Market()
       

    def update_board(self):
        for i in range(9):
            self.buttons[i].config(text=self.game.board[i])

    def reset_game(self):
        self.game = Morpion()
        self.update_board()

def LaunchMorpion():
    root = tk.Tk()
    root.title("Morpion")

    # Création du jeu de morpion
    tic_tac_toe_frame = tk.Frame(root)
    tic_tac_toe_frame.pack(pady=20)
    game = MorpionGUI(tic_tac_toe_frame)

    # Mise à jour de l'interface utilisateur pour s'assurer que tous les widgets sont créés
    root.update_idletasks()

    # Centrage de la fenêtre de jeu
    window_width = tic_tac_toe_frame.winfo_reqwidth()
    window_height = tic_tac_toe_frame.winfo_reqheight() + 70 # Ajoutez un décalage pour le label
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (window_width / 2)
    y_coordinate = (screen_height / 2) - (window_height / 2)
    
    # Assurez-vous que la fenêtre ne dépasse pas l'écran en bas
    if y_coordinate + window_height > screen_height:
        y_coordinate = screen_height - window_height

    root.geometry("%dx%d+%d+%d" % (window_width, window_height, x_coordinate, y_coordinate))

    root.mainloop()


    

    

