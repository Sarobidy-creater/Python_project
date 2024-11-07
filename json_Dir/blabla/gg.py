import tkinter as tk

def on_enter(event):
    print("Le curseur est dans l'Entry.")

def on_leave(event):
    print("Le curseur est sorti de l'Entry.")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Détecter le curseur dans l'Entry")

# Création de l'Entry
entry = tk.Entry(root, width=30)
entry.pack(pady=20)

# Liaison des événements
entry.bind("<Enter>", on_enter)
entry.bind("<Leave>")

# Boucle principale
root.mainloop()
