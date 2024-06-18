import tkinter as tk
from tkinter import ttk

from Interface_Blockchain import Launch_BlockchainView
from Interface_Morpion import LaunchMorpion

def parse_transaction(line):
    parts = line.split(',')
    expediteur = parts[0].strip()
    destinataire = parts[1].strip()
    objet = parts[2].strip()
    objets_list1 = parts[3].strip('[]').split('|')
    objets_list2 = [item.strip()[:-2] if i == len(parts[4].strip('[]').split('|')) - 1 else item.strip() for i, item in enumerate(parts[4].strip('[]').split('|'))]
    return expediteur, destinataire, objet, objets_list1, objets_list2

def process_file(filename):
    expediteurs_destinataires = {}
    with open(filename, 'r') as file:
        lines = file.readlines()

    in_block = False
    seen_expedit_dest = set()

    for line in reversed(lines):
        line = line.strip()
        if line.startswith('#blockEnd'):
            in_block = True
        elif line.startswith('#blockStart'):
            in_block = False
        elif in_block and line.startswith('id') and not line.startswith('ExpediteurNULL'):
            expediteur, destinataire, objet, objets_list1, objets_list2 = parse_transaction(line)
            key = (expediteur, destinataire)
            if key not in seen_expedit_dest:
                seen_expedit_dest.add(key)
                expediteurs_destinataires[key] = {
                    'objet': objet,
                    'expediteur_objets_list1': objets_list1,
                    'expediteur_objets_list2': objets_list2,
                    'destinataire_objets_list1': objets_list1,
                    'destinataire_objets_list2': objets_list2
                }

    return expediteurs_destinataires


class Application(tk.Tk):
    def __init__(self, filename, inventory_window):
        super().__init__()
        self.title("Résultats des Transactions")
        self.filename = filename
        self.inventory_window = inventory_window  # Store the inventory window reference
        self.tree = self.setup_treeview()
        self.refresh_button = tk.Button(self, text="Actualiser", command=self.refresh)

        self.button_shop = tk.Button(self, text="Inventaire", command=self.go_to_inventory)
        self.button_shop.pack(side=tk.LEFT, padx=5)

        self.button_play = tk.Button(self, text="Jouer", command=self.play_game)
        self.button_play.pack(side=tk.LEFT, padx=5)

        self.button_blockchain = tk.Button(self, text="Blockchain & Mempool View", command=self.open_blockchain)
        self.button_blockchain.pack(side=tk.LEFT, padx=5)
        self.refresh_button.pack(pady=20)

        self.refresh()
        self.center_window()

    def setup_treeview(self):
        columns = ("expediteur", "expediteur_list1", "destinataire", "destinataire_list2")
        tree = ttk.Treeview(self, columns=columns, show='headings')

        tree.column("expediteur", anchor=tk.W, width=120)
        tree.column("expediteur_list1", anchor=tk.W, width=200)
        tree.column("destinataire", anchor=tk.W, width=120)
        tree.column("destinataire_list2", anchor=tk.W, width=200)

        tree.heading("expediteur", text="Expéditeur", anchor=tk.W)
        tree.heading("expediteur_list1", text="Objets List 1 (Expéditeur)", anchor=tk.W)
        tree.heading("destinataire", text="Destinataire", anchor=tk.W)
        tree.heading("destinataire_list2", text="Objets List 2 (Destinataire)", anchor=tk.W)

        tree.pack(pady=20, fill=tk.BOTH, expand=True)

        return tree

    def refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        results = process_file(self.filename)

        for key, value in results.items():
            self.tree.insert("", tk.END, values=(
            key[0], ", ".join(value['expediteur_objets_list1']), key[1], ", ".join(value['destinataire_objets_list2'])))

    def play_game(self):
        self.destroy()
        LaunchMorpion(self.inventory_window)

    def open_blockchain(self):
        self.destroy()
        Launch_BlockchainView(self.inventory_window)

    def go_to_inventory(self):
        self.destroy()
        self.inventory_window.deiconify()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')


def Launch_Market(inventory_window):
    app = Application("../Blockchain.txt", inventory_window)
    app.mainloop()
