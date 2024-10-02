import tkinter as tk
from PIL import Image, ImageTk  # Pour gérer les images avec Pillow

# Fonction pour changer de panel
def switch_to_panel2():
    panel1.pack_forget()  # Cache le panel1
    panel2.pack(fill="both", expand=True)  # Affiche le panel2

# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Fenêtre avec panneaux")
fenetre.geometry("500x400")

# ********************************************************************* # 
# Panel 1 - avec une image, un fond bleu ciel et un bouton
panel1 = tk.Frame(fenetre, bg="#87CEEB")  # Couleur de fond bleu ciel (light blue)
panel1.pack(fill="both", expand=True)
# *********************************************************************

# Chargement et ajout de l'image dans le panel1
image = Image.open("c:\\Users\\nelly\\Documents\\L3-info\\nn.webp")  # Remplace par le chemin de ton image
image = image.resize((200, 200))  # Redimensionner si nécessaire
image_tk = ImageTk.PhotoImage(image)
label_image = tk.Label(panel1, image=image_tk, bg="#87CEEB")  # Assurez-vous que le label a aussi un fond bleu ciel
label_image.pack(pady=20)

# Ajouter un bouton pour passer à panel2
bouton_switch = tk.Button(panel1, text="Aller au panel 2", command=switch_to_panel2)
bouton_switch.pack(pady=10)

# ********************************************************************* # 
# Panel 2 - divisé en 4 sous-panneaux avec un centre
panel2 = tk.Frame(fenetre, bg="lightyellow")

# Lancement de la boucle principale
fenetre.mainloop()
