import tkinter as tk
from tkinter import filedialog, Listbox, Scrollbar, Label, PhotoImage
import pygame
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen.id3 import ID3, ID3NoHeaderError
from PIL import Image, ImageTk

# Initialiser Pygame
pygame.mixer.init()

# Fonction pour jouer le fichier audio sélectionné
def play_audio():
    selected_index = song_listbox.curselection()
    if selected_index:
        selected_song = song_listbox.get(selected_index)
        pygame.mixer.music.load(selected_song)
        pygame.mixer.music.play()
        # Afficher le chemin complet dans la zone de texte
        path_label.config(text=selected_song)
        # Afficher les métadonnées
        display_metadata(selected_song)
        # Afficher la couverture de l'album
        display_cover(selected_song)

# Fonction pour rechercher tous les fichiers MP3 dans le dossier spécifié
def search_mp3_files():
    folder_path = filedialog.askdirectory()
    if folder_path:
        song_listbox.delete(0, tk.END)
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.mp3'):
                    full_path = os.path.join(root, file)
                    song_listbox.insert(tk.END, full_path)

# Fonction pour afficher les métadonnées
def display_metadata(file_path):
    try:
        audio = MP3(file_path, ID3=ID3)
        metadata = f"Title: {audio.get('TIT2', 'Unknown')}\n"
        metadata += f"Artist: {audio.get('TPE1', 'Unknown')}\n"
        metadata += f"Album: {audio.get('TALB', 'Unknown')}\n"
        metadata += f"Year: {audio.get('TDRC', 'Unknown')}\n"
        metadata_label.config(text=metadata)
    except ID3NoHeaderError:
        metadata_label.config(text="No metadata found.")

# Fonction pour afficher la couverture de l'album
def display_cover(file_path):
    try:
        audio = MP3(file_path, ID3=ID3)
        cover_art = audio.tags.get('APIC:')  # Obtenir l'art de couverture
        if cover_art:
            image_data = cover_art.data  # Récupérer les données de l'image
            image = Image.open(io.BytesIO(image_data))
            image.thumbnail((200, 200))  # Redimensionner l'image
            photo = ImageTk.PhotoImage(image)
            cover_label.config(image=photo)
            cover_label.image = photo  # Garder une référence de l'image
        else:
            cover_label.config(image='')  # Effacer l'image si aucune couverture
    except Exception as e:
        cover_label.config(image='')  # Effacer l'image si une erreur se produit

# Créer la fenêtre principale
root = tk.Tk()
root.title("Lecteur Audio")

# Créer un bouton pour rechercher des fichiers MP3
search_button = tk.Button(root, text="Rechercher des fichiers MP3", command=search_mp3_files)
search_button.pack(pady=10)

# Créer une liste pour afficher les fichiers MP3
song_listbox = Listbox(root, width=50)
song_listbox.pack(pady=10)

# Ajouter une barre de défilement
scrollbar = Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
song_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=song_listbox.yview)

# Créer un bouton pour jouer le son
play_button = tk.Button(root, text="Jouer le son sélectionné", command=play_audio)
play_button.pack(pady=10)

# Label pour afficher le chemin complet du fichier sélectionné
path_label = Label(root, text="", wraplength=400, justify="left")
path_label.pack(pady=10)

# Label pour afficher les métadonnées
metadata_label = Label(root, text="", wraplength=400, justify="left")
metadata_label.pack(pady=10)

# Label pour afficher la couverture de l'album
cover_label = Label(root)
cover_label.pack(pady=10)

# Lancer l'interface
root.mainloop()
