import tkinter as tk
from tkinter import ttk

def create_tab(content, notebook, tab_name):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=tab_name)
    # Configurez le contenu de chaque onglet ici
    label = tk.Label(tab, text=content, foreground="white", background="black")
    label.pack(expand=True, fill='both')

# Création de la fenêtre principale
root = tk.Tk()
root.title("Interface Noir avec Onglets")

# Configuration de la couleur de fond à noir pour la fenêtre
root.configure(bg='black')

# Définition de la taille de la fenêtre
root.geometry('800x600')

# Configuration du style des onglets
style = ttk.Style()
style.theme_use('default')  # 'default' peut être remplacé par 'alt', 'clam', ou un autre selon votre système

# Configuration générale du style des onglets pour s'adapter au thème noir
style.configure('TNotebook', background='black', borderwidth=0)
style.configure('TNotebook.Tab', background='grey20', foreground='white', lightcolor='grey20', darkcolor='grey20', borderwidth=0, padding=[5, 2])

# Style pour les onglets actifs
style.map('TNotebook.Tab', background=[('selected', 'grey35')], foreground=[('selected', 'white')])

# Création du widget Notebook (onglets)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Ajout des onglets avec leur contenu spécifique
create_tab("Contenu de l'Onglet 1", notebook, 'Onglet 1')
create_tab("Contenu de l'Onglet 2", notebook, 'Onglet 2')
create_tab("Contenu de l'Onglet 3", notebook, 'Onglet 3')

# Lancement de la boucle principale
root.mainloop()
