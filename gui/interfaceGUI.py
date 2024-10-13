#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import tkinter as tk
from tkinter import ttk, filedialog
import os


class InterfaceMusicale:
    def __init__(self, root):
        self.root = root
        self.root.geometry('500x500')
        self.root.title("Lecteur de Musique")

        # Configuration de la grille 3x3
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1)

        # Barre de recherche et bouton d'exploration
        self.frame_recherche = ttk.Frame(self.root)
        self.frame_recherche.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        self.entry_recherche = ttk.Entry(self.frame_recherche)
        self.entry_recherche.pack(side=tk.LEFT, expand=True, fill=tk.X)

        self.btn_explorer = ttk.Button(self.frame_recherche, text="Explorer", command=self.explorer_dossier)
        self.btn_explorer.pack(side=tk.RIGHT)

        # Liste des fichiers audio
        self.liste_fichiers = tk.Listbox(self.root)
        self.liste_fichiers.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        # Photo de l'album
        self.photo_album = ttk.Label(self.root, text="Photo de l'album")
        self.photo_album.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Métadonnées
        self.metadonnees = ttk.Label(self.root, text="Métadonnées")
        self.metadonnees.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Boutons du bas
        self.btn_creer_playlist = ttk.Button(self.root, text="Créer Playlist")
        self.btn_creer_playlist.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        self.frame_controles = ttk.Frame(self.root)
        self.frame_controles.grid(row=2, column=1, sticky="nsew", padx=5, pady=5)

        self.btn_precedent = ttk.Button(self.frame_controles, text="Précédent")
        self.btn_precedent.pack(side=tk.LEFT, expand=True)

        self.btn_lecture = ttk.Button(self.frame_controles, text="Lecture/Pause")
        self.btn_lecture.pack(side=tk.LEFT, expand=True)

        self.btn_suivant = ttk.Button(self.frame_controles, text="Suivant")
        self.btn_suivant.pack(side=tk.LEFT, expand=True)

        self.btn_modifier_meta = ttk.Button(self.root, text="Modifier Métadonnées")
        self.btn_modifier_meta.grid(row=2, column=2, sticky="nsew", padx=5, pady=5)

    def explorer_dossier(self):
        dossier = filedialog.askdirectory()
        if dossier:
            fichiers_audio = [f for f in os.listdir(dossier) if f.endswith(('.mp3', '.flac'))]
            self.liste_fichiers.delete(0, tk.END)
            for fichier in fichiers_audio:
                self.liste_fichiers.insert(tk.END, fichier)


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfaceMusicale(root)
    root.mainloop()
