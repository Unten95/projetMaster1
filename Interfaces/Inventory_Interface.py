import threading
import tkinter as tk
from BlockReader import read_blocks_from_file
from Interface_Blockchain import Launch_BlockchainView
from Interface_Market import Launch_Market
from Interface_Morpion import LaunchMorpion
from p2p import Peer
from Transaction_Creator import get_Inventory
import tkinter as tk
import threading


class InventoryGUI:
    def __init__(self, root, inventory):
        self.node1 = Peer("0.0.0.0", 8005)
        self.thread = threading.Thread(target=self.node1.start)
        self.thread.start()

        self.root = root
        self.inventory = inventory

        # Create a listbox for item names
        self.item_listbox = tk.Listbox(root, width=50, height=10)
        self.update_listbox()
        self.item_listbox.grid(row=0, column=0, padx=10, pady=10)

        # Add a scrollbar to the listbox
        self.scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.item_listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.item_listbox.config(yscrollcommand=self.scrollbar.set)

        self.display_image_label = tk.Label(root)
        self.display_image_label.grid(row=1, column=0, padx=10, pady=10)

        # Buttons to go to the shop and play
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=2, column=0, padx=10, pady=10)

        self.button_shop = tk.Button(self.button_frame, text="Boutique", command=self.go_to_shop)
        self.button_shop.pack(side=tk.LEFT, padx=5)

        self.button_play = tk.Button(self.button_frame, text="Jouer", command=self.play_game)
        self.button_play.pack(side=tk.LEFT, padx=5)

        self.button_blockchain = tk.Button(self.button_frame, text="Blockchain & Mempool View",
                                           command=self.open_blockchain)
        self.button_blockchain.pack(side=tk.LEFT, padx=5)

        self.button_init_transaction = tk.Button(self.button_frame, text="Initialiser une transaction",
                                                 command=self.open_transaction)
        self.button_init_transaction.pack(side=tk.LEFT, padx=5)

        self.button_init_blockchain = tk.Button(self.button_frame, text="Miner", command=self.mine_block)
        self.button_init_blockchain.pack(side=tk.LEFT, padx=5)

        # Button to refresh inventory
        self.button_refresh = tk.Button(self.button_frame, text="Actualiser l'inventaire",
                                        command=self.update_inventory)
        self.button_refresh.pack(side=tk.LEFT, padx=5)

    def update_listbox(self):
        # Clear the current items in the listbox
        self.item_listbox.delete(0, tk.END)
        # Insert updated inventory items into the listbox
        if self.inventory is not None:
            for item in self.inventory:
                self.item_listbox.insert(tk.END, item)

    def update_inventory(self):
        # Update self.inventory with the latest data
        from PrincipalMenu import current_user  # Re-import to ensure updated data
        file_path = '../Blockchain.txt'
        blocks = read_blocks_from_file(file_path)
        self.inventory = get_Inventory(blocks, current_user)
        # Update the listbox with new inventory
        self.update_listbox()

    def open_transaction(self):
        register_window = tk.Toplevel()
        register_window.title("Transaction")

        label_new_username = tk.Label(register_window, text="Receveur:")
        label_new_username.grid(row=0, column=0, padx=5, pady=5)
        entry_new_username = tk.Entry(register_window)
        entry_new_username.grid(row=0, column=1, padx=5, pady=5)

        label_new_password = tk.Label(register_window, text="Objet :")
        label_new_password.grid(row=1, column=0, padx=5, pady=5)
        entry_new_password = tk.Entry(register_window)
        entry_new_password.grid(row=1, column=1, padx=5, pady=5)

        button_register = tk.Button(register_window, text="Envoyer",
                                    command=lambda: self.send_transaction(entry_new_username.get(),
                                                                          entry_new_password.get()))
        button_register.grid(row=2, columnspan=2, padx=5, pady=5)

    def send_transaction(self, recipient, item):
        self.node1.create_and_send_transaction(recipient, item)
        self.update_inventory()  # Update inventory after sending a transaction

    def go_to_shop(self):
        self.root.withdraw()
        Launch_Market(self.root)

    def play_game(self):
        self.root.withdraw()
        LaunchMorpion(self.root)

    def open_blockchain(self):
        self.root.withdraw()
        Launch_BlockchainView(self.root)

    def mine_block(self):
        self.node1.mine_blockchain()
        self.update_inventory()  # Update inventory after mining a block


def Launch_Inventory():
    from PrincipalMenu import current_user
    root = tk.Tk()
    root.title("Inventaire")

    # Example list of images (file paths)
    file_path = '../Blockchain.txt'
    blocks = read_blocks_from_file(file_path)
    inventory = get_Inventory(blocks, current_user)

    # Center the window
    window_width = 600
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Create the inventory interface
    inventory_gui = InventoryGUI(root, inventory)

    root.mainloop()
