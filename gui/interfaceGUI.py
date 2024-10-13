#!/usr/bin/python3
# -*- coding: UTF-8 -*-

"""
Lecteur de musique avec gestion des playlists.
Utilise Tkinter pour l'interface, pygame pour la lecture audio,
et mutagen pour manipuler les métadonnées de fichiers MP3/FLAC.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC
from mutagen.mp3 import MP3
from mutagen.flac import FLAC, Picture
from PIL import Image, ImageTk
import io
import os
import pygame  # Gestion audio avec pygame
from lxml import etree  # Pour manipuler XML


class Ecouter:
    """Gère la lecture audio à l'aide de pygame."""

    def __init__(self):
        """Initialise le moteur audio de pygame."""
        pygame.mixer.init()

    def lire_fichier(self, chemin):
        """
        Charge et lit un fichier audio.
        :param chemin: Chemin du fichier audio.
        """
        pygame.mixer.music.load(chemin)
        pygame.mixer.music.play()

    def pause(self):
        """Met en pause la lecture audio."""
        pygame.mixer.music.pause()

    def reprendre(self):
        """Reprend la lecture audio en pause."""
        pygame.mixer.music.unpause()

    def arreter(self):
        """Arrête complètement la lecture audio."""
        pygame.mixer.music.stop()


class Playlist:
    """Gère les playlists au format XSPF."""

    def __init__(self):
        """Crée un répertoire local pour stocker les playlists."""
        self.dossier_playlist = os.path.abspath('Playlists')
        os.makedirs(self.dossier_playlist, exist_ok=True)

    def creer_playlist(self, nom):
        """
        Crée une nouvelle playlist XSPF.
        :param nom: Nom de la nouvelle playlist.
        :return: Chemin complet du fichier de la playlist.
        """
        chemin = os.path.join(self.dossier_playlist, f"{nom}.xspf")
        with open(chemin, 'w', encoding='utf-8') as f:
            f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
            f.write("<playlist version=\"1\" xmlns=\"http://xspf.org/ns/0/\"></playlist>\n")
        return chemin

    def ajouter_audio_playlist(self, chemin_playlist, chemin_audio):
        """
        Ajoute un fichier audio à une playlist existante.
        :param chemin_playlist: Chemin de la playlist XSPF.
        :param chemin_audio: Chemin du fichier audio à ajouter.
        """
        try:
            tree = etree.parse(chemin_playlist)
            root = tree.getroot()
            tracklist = root.find("trackList") or etree.SubElement(root, "trackList")

            # Ajout du fichier audio à la playlist
            track = etree.Element("track")
            location = etree.Element("location")
            location.text = f"file:///{os.path.abspath(chemin_audio).replace('\\', '/')}"
            track.append(location)
            tracklist.append(track)

            with open(chemin_playlist, 'wb') as f:
                f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
        except Exception as e:
            print(f"Erreur lors de l'ajout à la playlist : {e}")

    def lister_playlists(self):
        """
        Liste les fichiers de playlist disponibles.
        :return: Liste des noms de fichiers de playlists.
        """
        return [f for f in os.listdir(self.dossier_playlist) if f.endswith('.xspf')]


class InterfaceMusicale:
    """Interface graphique principale du lecteur de musique."""

    def __init__(self, root):
        """
        Initialise l'interface utilisateur.
        :param root: Fenêtre Tkinter principale.
        """
        self.root = root
        self.root.geometry('800x600')
        self.root.title("Lecteur de Musique et Gestionnaire de Playlist")

        # Instances de gestion audio et de playlists
        self.lecteur = Ecouter()
        self.playlist_manager = Playlist()

        # Variables de sélection
        self.chemin_fichier_selectionne = None
        self.image_album = None

        # Configuration de la grille principale
        for i in range(4):
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
        self.liste_fichiers.bind("<<ListboxSelect>>", self.afficher_details_audio)

        # Affichage de la couverture d’album
        self.photo_album = ttk.Label(self.root, text="Pas de couverture", anchor="center")
        self.photo_album.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Zone d'affichage des métadonnées
        self.metadonnees = ttk.Label(self.root, text="Métadonnées réduites", anchor="center")
        self.metadonnees.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Boutons de contrôle audio
        self.frame_controles = ttk.Frame(self.root)
        self.frame_controles.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        self.btn_lecture = ttk.Button(self.frame_controles, text="Lecture", command=self.lire_audio)
        self.btn_lecture.pack(side=tk.LEFT, expand=True, padx=5)

        self.btn_pause = ttk.Button(self.frame_controles, text="Pause", command=self.lecteur.pause)
        self.btn_pause.pack(side=tk.LEFT, expand=True, padx=5)

        self.btn_reprendre = ttk.Button(self.frame_controles, text="Reprendre", command=self.lecteur.reprendre)
        self.btn_reprendre.pack(side=tk.LEFT, expand=True, padx=5)

        self.btn_stop = ttk.Button(self.frame_controles, text="Arrêter", command=self.lecteur.arreter)
        self.btn_stop.pack(side=tk.LEFT, expand=True, padx=5)

        # Section Playlists
        self.frame_playlist = ttk.Frame(self.root)
        self.frame_playlist.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        self.btn_creer_playlist = ttk.Button(self.frame_playlist, text="Créer Playlist", command=self.creer_playlist)
        self.btn_creer_playlist.pack(side=tk.LEFT, padx=5)

        self.liste_playlists = tk.Listbox(self.frame_playlist)
        self.liste_playlists.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5)
        self.liste_playlists.bind("<<ListboxSelect>>", self.selectionner_playlist)

        # Chargement initial des playlists
        self.rafraichir_playlists()

    def explorer_dossier(self):
        """Ouvre une boîte de dialogue pour sélectionner un dossier contenant des fichiers audio."""
        dossier = filedialog.askdirectory()
        if dossier:
            fichiers_audio = [f for f in os.listdir(dossier) if f.endswith(('.mp3', '.flac'))]
            self.liste_fichiers.delete(0, tk.END)
            for fichier in fichiers_audio:
                self.liste_fichiers.insert(tk.END, fichier)

    def afficher_details_audio(self, event):
        """Affiche les détails du fichier audio sélectionné."""
        selection = self.liste_fichiers.curselection()
        if selection:
            self.chemin_fichier_selectionne = filedialog.askopenfilename()
            self.extraire_et_afficher_tag(self.chemin_fichier_selectionne)
            self.extraire_et_afficher_cover(self.chemin_fichier_selectionne)

    def extraire_et_afficher_tag(self, chemin):
        """Affiche les métadonnées du fichier audio sélectionné."""
        try:
            audio = MP3(chemin, ID3=EasyID3) if chemin.endswith('.mp3') else FLAC(chemin)
            titre = audio.get('title', ['Titre inconnu'])[0]
            artiste = audio.get('artist', ['Artiste inconnu'])[0]
            self.metadonnees.config(text=f"Titre: {titre}\nArtiste: {artiste}")
        except Exception as e:
            self.metadonnees.config(text=f"Erreur: {e}")

    def extraire_et_afficher_cover(self, chemin):
        """Affiche la couverture d'album du fichier audio."""
        try:
            audio = MP3(chemin) if chemin.endswith('.mp3') else FLAC(chemin)
            image = next((Image.open(io.BytesIO(tag.data)) for tag in audio.tags.values() if isinstance(tag, APIC)), None)
            if image:
                image = image.resize((80, 80))
                self.image_album = ImageTk.PhotoImage(image)
                self.photo_album.config(image=self.image_album, text="")
            else:
                self.photo_album.config(text="Pas de couverture disponible")
        except Exception as e:
            self.photo_album.config(text=f"Erreur: {e}")

    def lire_audio(self):
        """Lance la lecture du fichier audio sélectionné."""
        if self.chemin_fichier_selectionne:
            self.lecteur.lire_fichier(self.chemin_fichier_selectionne)

    def creer_playlist(self):
        """Crée une nouvelle playlist et la recharge dans la liste."""
        nom = filedialog.asksaveasfilename(defaultextension=".xspf", filetypes=[("XSPF Playlist", "*.xspf")])
        if nom:
            self.playlist_manager.creer_playlist(nom)
            self.rafraichir_playlists()

    def selectionner_playlist(self, event):
        """Ajoute le fichier audio sélectionné à la playlist choisie."""
        selection = self.liste_playlists.curselection()
        if selection:
            nom_playlist = self.liste_playlists.get(selection[0])
            chemin_playlist = os.path.join(self.playlist_manager.dossier_playlist, nom_playlist)
            if self.chemin_fichier_selectionne:
                self.playlist_manager.ajouter_audio_playlist(chemin_playlist, self.chemin_fichier_selectionne)

    def rafraichir_playlists(self):
        """Recharge la liste des playlists disponibles."""
        self.liste_playlists.delete(0, tk.END)
        for playlist in self.playlist_manager.lister_playlists():
            self.liste_playlists.insert(tk.END, playlist)


if __name__ == "__main__":
    # Démarre l'application Tkinter
    root = tk.Tk()
    app = InterfaceMusicale(root)
    root.mainloop()
