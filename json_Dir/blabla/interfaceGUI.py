import tkinter as tk
from tkinter import messagebox

class AudioPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lecteur Audio")

        # Créer une Listbox pour afficher les fichiers audio
        self.audio_listbox = tk.Listbox(root)
        self.audio_listbox.pack(padx=20, pady=20)

        # Ajouter des fichiers audio à la Listbox (exemple)
        self.audio_files = ["chanson1.mp3", "chanson2.mp3", "chanson3.mp3"]
        for audio_file in self.audio_files:
            self.audio_listbox.insert(tk.END, audio_file)

        # Lier le double-clic à la lecture et à l'affichage du titre
        self.audio_listbox.bind("<Double-Button-1>", self.affiche_path_label)

        # Lier le clic droit à l'ajout dans une playlist
        self.audio_listbox.bind("<Button-3>", self.ajouter_playlist)

    def affiche_path_label(self, event):
        # Récupérer l'index de l'élément sélectionné
        selected_index = self.audio_listbox.curselection()
        if selected_index:
            # Récupérer le nom du fichier sélectionné
            selected_audio = self.audio_listbox.get(selected_index)
            # Afficher le nom du fichier (ou jouer le fichier audio)
            messagebox.showinfo("Lecture", f"Lecture du fichier : {selected_audio}")
            # Vous pouvez ajouter ici le code pour jouer le fichier audio

    def ajouter_playlist(self, event):
        # Récupérer l'index de l'élément sélectionné
        selected_index = self.audio_listbox.curselection()
        if selected_index:
            # Récupérer le nom du fichier sélectionné
            selected_audio = self.audio_listbox.get(selected_index)
            # Ajouter le fichier à une playlist (affichage d'un message par exemple)
            messagebox.showinfo("Ajout", f"Ajout de {selected_audio} à la playlist")
            # Vous pouvez ajouter ici le code pour gérer la playlist

# Créer la fenêtre principale
root = tk.Tk()

# Créer l'application
app = AudioPlayerApp(root)

# Lancer l'application
root.mainloop()
