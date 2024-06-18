import tkinter as tk
from tkinter import ttk

from Interfaces.Interface_Blockchain import Launch_BlockchainView
from Interfaces.Interface_Morpion import LaunchMorpion

# Exemple de données d'items
items = [
    {'name': 'Item 1', 'description': 'Description for item 1', 'price': '10.00'},
    {'name': 'Item 2', 'description': 'Description for item 2', 'price': '20.00'},
    {'name': 'Item 3', 'description': 'Description for item 3', 'price': '30.00'},
    {'name': 'Item 4', 'description': 'Description for item 4', 'price': '40.00'},
    {'name': 'Item 5', 'description': 'Description for item 5', 'price': '50.00'},
    {'name': 'Item 6', 'description': 'Description for item 6', 'price': '60.00'},
    {'name': 'Item 7', 'description': 'Description for item 7', 'price': '70.00'},
]

class MarketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Items List")

        # Centrer la fenêtre sur l'écran
        window_width = 500
        window_height = 300

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)

        self.root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        # Cadre principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Centrer le cadre principal dans la fenêtre
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Titre
        title_label = ttk.Label(main_frame, text="Items List", font=("Helvetica", 16))
        title_label.grid(row=0, column=0, pady=(0, 10), columnspan=2)

        # Cadre pour la liste et la barre de défilement
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=1, column=0, pady=5, columnspan=2, sticky=(tk.W, tk.E))

        # Liste défilante
        self.listbox = tk.Listbox(list_frame, height=10)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        for item in items:
            self.listbox.insert(tk.END, item['name'])

        # Barre de défilement
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Liaison de l'événement de sélection
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        # Labels pour les détails de l'item
        self.description_label = ttk.Label(main_frame, text="Description: ")
        self.description_label.grid(row=2, column=0, pady=5, columnspan=2, sticky=tk.W)

        # Boutons de navigation
        button_shop = tk.Button(self.root, text="Morpion", command=self.play_game)
        button_shop.grid(row=3, column=1, padx=5, pady=10)

        button_inventory = tk.Button(self.root, text="Inventaire", command=self.go_to_inventory)
        button_inventory.grid(row=3, column=2, padx=5, pady=10)

        button_blockchain = tk.Button(self.root, text="Blockchain & Mempool", command=self.open_blockchain)
        button_blockchain.grid(row=3, column=3, padx=5, pady=10)

        # Centrer la liste et les détails
        main_frame.columnconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.columnconfigure(1, weight=0)

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_item = items[selected_index[0]]
            self.description_label.config(text=f"Description: {selected_item['description']}")

    def go_to_shop(self):
        self.root.withdraw()
        Launch_Market(self)

    def play_game(self):
        self.root.withdraw()
        LaunchMorpion(self)

    def open_blockchain(self):
        self.root.withdraw()
        Launch_BlockchainView(self)

    def show_main_window(self):
        self.root.deiconify()

        


    
        

def Launch_Market():
    root = tk.Tk()
    app = MarketApp(root)
    root.mainloop()

