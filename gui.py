#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import io
import time
import tkinter as tk
import pygame  # Bibliothèque pour gérer les fonctionnalités multimédias comme jouer des fichiers audio.
from tkinter import *
from tkinter import filedialog, Listbox, Scrollbar, Label, PhotoImage, messagebox
from PIL import Image, ImageTk  # Pour gérer les images avec Pillow
from ecouterAudio import Ecouter # Importe la classe Ecouter du module ecouterAudio pour lire un fichier audio mp3 ou flac dans la console
from explorationDossier import Explorer  # Importe la classe Explorer pour explorer les dossiers
from constitutionPlaylist import Playlist  # Importe la classe Playlist du module constitutionPlaylist pour générer des playlists
from audioTagExtraction import Extraction  # Importe la classe Extraction du module audioTagExtraction pour extraire les métadonnées audio
from fetcher import Fetcher
from audioMetaEdite import Editer
from mutagen.easyid3 import EasyID3  # Pour lire et écrire les métadonnées ID3 dans les fichiers MP3.
from mutagen.mp3 import MP3  # Pour gérer les fichiers audio MP3 et accéder à leurs métadonnées.
from mutagen.id3 import ID3, APIC  # Pour manipuler les balises ID3 et gérer les images intégrées comme les couvertures d'album.
from mutagen.flac import FLAC, Picture  # Pour travailler avec les fichiers audio FLAC et gérer les images intégrées.
from PIL import Image  # Pour ouvrir, modifier et enregistrer des images dans divers formats.



class Interface:
    def __init__(self, master):
        """Initialisation de l'interface et création des composants graphiques"""
        self.master = master
        self.master.title("Lecteur Audio")  # Titre de la fenêtre
        self.master.state("zoomed")  # Agrandir la fenêtre à l'écran

        # Initialisation des variables
        self.mon_dictionnaire = {}  # Dictionnaire pour stocker les fichiers audio
        self.explo = Explorer()  # Instance de la classe Explorer pour parcourir les dossiers
        self.ecoute = Ecouter()  # Instance de la classe Ecouter pour lire les fichiers audio
        self.playlist = Playlist()  # Instance de la classe Playlist pour gérer les playlists
        self.extract = Extraction()  # Instance de la classe Extraction pour extraire les métadonnées audio
        self.fetcher = Fetcher()
        self.edite = Editer()
        self.varDirectory = ""  # Variable pour stocker le chemin du répertoire exploré
        self.valeur_par_defaut = "maPlaylist"  # Valeur par défaut de l'entrée de texte pour nommer la playlist
        self.is_paused = False  # Variable pour suivre si la lecture est en pause
        self.Varbutt = ""  # Variable pour suivre l'élément audio actuellement joué
        self.buttnext = 0  # Variable pour naviguer entre les fichiers audio
        self.tailleListbox = 0  # Taille de la liste des fichiers audio
        self.audio_lecture = False  # Statut de lecture de l'audio
        self.reche = False
        self.lightyellow = "lightyellow"  # Couleur de fond pour certaines parties de l'interface
        self.dodgerblue = "dodgerblue"  # Couleur de fond pour d'autres parties
        self.antiquewhite = "antiquewhite"  # Autre couleur de fond
        self.metadata_str = ""
        self.chemin_audio = ""
        self.verif_lecture = False
        self.playlist_window = False
        self.affiche_window = False # Attribut pour suivre si la fenêtre de modification est ouverte
        # Variables pour gérer l'interface
        self.checkbox_vars = []  # Pour stocker les variables de cases à cocher
        self.chemins_options = []  # Pour stocker les chemins des options
        self.file_path_chemins = os.path.abspath(r'python_project\FichierTemp\options_selectionnees.txt')  # Chemin du fichier où écrire les options sélectionnées

        # Création des différents panneaux de l'interface

        # Panel 1 : Fond bleu ciel avec une image et un bouton
        self.panel1 = tk.Frame(self.master, bg="#87CEEB")
        self.panel1.pack(fill="both", expand=True)

        # Obtenir le chemin absolu du répertoire actuel pour les images
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Charger l'image depuis le répertoire du projet
        chem_image = os.path.join(base_dir, "img", "nn.webp")
        self.image = Image.open(chem_image)  # Charger l'image
        self.image = self.image.resize((200, 200))  # Redimensionner l'image
        self.image_tk = ImageTk.PhotoImage(self.image)  # Convertir pour l'utiliser avec tkinter
        self.label_image = tk.Label(self.panel1, image=self.image_tk, bg="#87CEEB")  # Ajouter l'image au label
        self.label_image.pack(pady=20)  # Afficher l'image avec espacement vertical

        # Bouton pour changer de panneau (panel2)
        self.bouton_switch = tk.Button(self.panel1, text="Aller Go", command=self.direct_Goto)
        self.bouton_switch.pack(pady=10)  # Affichage avec un espacement vertical

        # Panel 2 
        self.panel2 = tk.Frame(self.master, bg=self.lightyellow)

        # Créer trois cadres avec des tailles différentes
        self.frame1_haut = tk.Frame(self.panel2, bg=self.antiquewhite)
        self.frame2_centre = tk.Frame(self.panel2, bg="gray")
        self.frame3_bas = tk.Frame(self.panel2, bg=self.dodgerblue)

        # Pack les cadres avec des tailles différentes
        self.frame1_haut.pack(fill=tk.X, padx=5, pady=5)  # Cadre 1 : petit, remplit la largeur
        self.frame2_centre.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # Cadre 2 : très grand, remplit l'espace
        self.frame3_bas.pack(fill=tk.X, padx=5, pady=5)  # Cadre 3 : intermédiaire, remplit la largeur

        # Cadre 1******************************************
        # self.button2 = tk.Button(self.frame1, text="Retour", width=12)
        # self.button2.pack(side=tk.LEFT, padx=10, pady=10)  # Aligné à droite

        self.entry_ecriture_haut = tk.Entry(self.frame1_haut, width=150)
        self.entry_ecriture_haut.pack(side=tk.LEFT, padx=5, pady=5)

        self.butt_check_api = tk.Button(self.frame1_haut, text="Check", width=12, command=self.rechercher)
        self.butt_check_api.pack(side=tk.LEFT, padx=10, pady=10)  # Aligné à droite

        self.butt_modif_metaData = tk.Button(self.frame1_haut, text=":::", width=12, command=self.modification_data)
        self.butt_modif_metaData.pack(side=tk.RIGHT, padx=10, pady=10) 

        # Cadre 2******************************************
        # Configurer le grid pour 3 colonnes de taille égale
        self.frame2_centre.grid_columnconfigure(0, weight=1)
        self.frame2_centre.grid_columnconfigure(1, weight=1)
        self.frame2_centre.grid_columnconfigure(2, weight=1)
        self.frame2_centre.grid_rowconfigure(0, weight=1)  # Une seule ligne

        # Créer trois sous-sections dans frame2 (gauche, centre, droite) avec les mêmes dimensions
        self.section1_gauche_liste = tk.Frame(self.frame2_centre, bg=self.antiquewhite)
        self.section1_gauche_liste.grid(row=0, column=0, sticky='nse', padx=5, pady=5)

        self.section2_centre_cover = tk.Frame(self.frame2_centre, bg=self.lightyellow)
        self.section2_centre_cover.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        self.section3_metaData = tk.Frame(self.frame2_centre, bg=self.lightyellow)
        self.section3_metaData.grid(row=0, column=2, sticky='nsw', padx=2, pady=2)

        # Créer une liste pour afficher les fichiers MP3
        self.audio_listbox = Listbox(self.section1_gauche_liste, width=80, height=10, bg=self.antiquewhite, selectbackground=self.dodgerblue)  # Ajuster la taille ici
        self.audio_listbox.pack(side=tk.LEFT, fill='both', expand=True)

        # Lier le double-clic à la lecture et l'affichage du titre
        self.audio_listbox.bind("<Double-Button-1>", self.affiche_path_label)

        # Lier le double-clic à la lecture et l'affichage du titre
        # self.audio_listbox.bind("<Double-Button-1>", self.ajoute_playlist)

        # Ajouter une barre de défilement
        self.scrollbarlistbox = Scrollbar(self.section1_gauche_liste)
        self.scrollbarlistbox.pack(side=tk.RIGHT, fill=tk.Y, padx=0, pady=0)  # Assurer aucun espacement

        # Lier la barre de défilement à la Listbox
        self.audio_listbox.config(yscrollcommand=self.scrollbarlistbox.set)
        self.scrollbarlistbox.config(command=self.audio_listbox.yview)

        # Label pour afficher 
        self.centrale_label = Label(self.section2_centre_cover, text="", width=70, height=10, justify="left", bg=self.lightyellow)
        self.centrale_label.pack(pady=10, fill='both', expand=True)  # Utiliser fill='both' et expand=True pour agrandir

        # Label pour afficher 
        self.A_label_cover = Label(self.centrale_label, text="", width=90, height=111, justify="left", bg=self.lightyellow)
        self.A_label_cover.pack(pady=10, fill='both', expand=True)  # Utiliser fill='both' et expand=True pour agrandir

        # Label pour afficher 
        self.B_label_fichier_boutton = Label(self.centrale_label, text="", width=30, height=1, justify="left", bg=self.lightyellow)
        self.B_label_fichier_boutton.pack(pady=10, fill='both', expand=True)  # Utiliser fill='both' et expand=True pour agrandir

        # Label pour afficher 
        self.B1_label_fichier_nom = Label(self.B_label_fichier_boutton, text="", width=2, height=1, justify="left", bg=self.lightyellow)
        self.B1_label_fichier_nom.pack(pady=10, fill='both', expand=True)  # Utiliser fill='both' et expand=True pour agrandir

        # Label pour afficher 
        self.B2_label_bouton_manip = Label(self.B_label_fichier_boutton, text="", width=11, height=1, justify="left", bg=self.lightyellow)
        self.B2_label_bouton_manip.pack(pady=10, fill='both', expand=True)  # Utiliser fill='both' et expand=True pour agrandir

        # Label pour afficher 
        self.metaData_label = Label(self.section3_metaData, text="", width=70, height=10, justify="left", bg=self.lightyellow)
        self.metaData_label.pack(pady=10, fill='both', expand=True)  # Utiliser fill='both' et expand=True pour agrandir

        # Cadre 3******************************************
        # Configurer le grid pour 3 colonnes de taille égale
        self.frame3_bas.grid_columnconfigure(0, weight=1)  # Sect1
        self.frame3_bas.grid_columnconfigure(1, weight=2)  # Sect2 (plus large)
        self.frame3_bas.grid_columnconfigure(2, weight=1)  # Sect3

        self.frame3_bas.grid_rowconfigure(0, weight=1)  # Une seule ligne

        self.explo_playlist_boutton = tk.Frame(self.frame3_bas, bg=self.lightyellow, width=28)
        self.explo_playlist_boutton.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)

        self.petit_zone_vide = tk.Frame(self.frame3_bas, bg=self.dodgerblue)
        self.petit_zone_vide.grid(row=0, column=1, sticky='nsew',padx=2, pady=2)

        self.zone_petit_logo = tk.Frame(self.frame3_bas, bg=self.dodgerblue)
        self.zone_petit_logo.grid(row=0, column=2, sticky='nsew',padx=2, pady=2)

        # logo image 
        chem_im = os.path.abspath(r"Python_project/img/nn.webp")
        self.im = Image.open(chem_im)  # Remplace par le chemin de ton image
        self.im = self.im.resize((24, 24))  # Redimensionner si nécessaire
        self.im_tk = ImageTk.PhotoImage(self.im)
        self.label_img_petit_logo = tk.Label(self.zone_petit_logo, image=self.im_tk, bg=self.dodgerblue)
        self.label_img_petit_logo.pack(side=tk.RIGHT, padx=10, pady=10) 

        # ******************************************
        # Création d'un bouton pour explorer les dossiers audio
        self.butt_exploration = tk.Button(self.explo_playlist_boutton, text="Exploration", command=self.exploration_dossier, width=13)
        self.butt_exploration.pack(side=tk.LEFT, padx=10, pady=10)  # Positionné à gauche avec un espacement horizontal et vertical

        # Création d'un bouton pour ouvrir la fenêtre de playlist
        self.butt_playlist = tk.Button(self.explo_playlist_boutton, text="Playlist", command=self.open_new_fenetre, width=13)
        self.butt_playlist.pack(side=tk.RIGHT, padx=10, pady=10)  # Positionné à droite avec un espacement horizontal et vertical

        # Création d'un bouton pour revenir au morceau audio précédent
        self.butt_next = tk.Button(self.B2_label_bouton_manip, text="◀◀", command=self.prev_audio, width=2)
        self.butt_next.pack(side=tk.LEFT, padx=10, pady=10)  # Positionné à gauche avec un espacement

        # Création d'un bouton pour lire le morceau audio actuel
        self.butt_play = tk.Button(self.B2_label_bouton_manip, text="▶", command=self.lire_audio, width=10)
        self.butt_play.pack(side=tk.LEFT, padx=10, pady=10)  # Positionné à gauche avec un espacement

        # Création d'un bouton pour mettre en pause ou reprendre la lecture du morceau audio
        self.butt_pause_reprendre = tk.Button(self.B2_label_bouton_manip, text="⏸", command=self.toggle_pause, width=10)
        self.butt_pause_reprendre.pack(side=tk.LEFT, padx=10, pady=10)  # Positionné à gauche avec un espacement
        
        # Création d'un bouton pour passer au morceau audio suivant
        self.butt_next = tk.Button(self.B2_label_bouton_manip, text="▶▶", command=self.next_audio, width=6)
        self.butt_next.pack(side=tk.RIGHT, padx=10, pady=10)  # Positionné à droite avec un espacement



    def direct_Goto(self):
        """Passage au panneau 2 et chargement de la musique par défaut."""
        self.switch_to_panel2() 
        chem = os.path.abspath(r"Python_project\music")
        self.AZEexploration_dossier(chem) 
        audio_path = self.mon_dictionnaire["0"]
        # Récupère seulement le nom du fichier à partir du chemin
        nom_fichier = os.path.basename(audio_path)
        self.B1_label_fichier_nom.config(text=nom_fichier)
        # Extraire et afficher les métadonnées de l'audio
        self.metadata_str = self.extract.extraction_et_afficher_tag(audio_path)
        self.metaData_label.config(text=self.metadata_str)  # Afficher les métadonnées dans path_label3
        self.cover_image(audio_path)  # Affiche l'image de couverture
        self.chemin_audio = audio_path
        self.Varbutt = "0"
        self.buttnext = 0
        self.audio_listbox.selection_set(self.buttnext)  # Sélectionne le premier élément

    def exploration_dossier(self):
        """Ouvre un dossier pour explorer et charger des fichiers audio."""
        # Ouvre une boîte de dialogue pour sélectionner un dossier et stocke le chemin dans 'dossier'.
        self.mon_dictionnaire.clear()
        dossier = filedialog.askdirectory()  
        
        # Vérifie si un dossier a été sélectionné
        if dossier:
            # Efface le contenu actuel de la Listbox pour éviter les doublons
            self.audio_listbox.delete(0, tk.END)

            # Remplace les antislashs (\) par des barres obliques (/) pour la compatibilité
            dossier_save = dossier.replace("\\", "/") 
            self.varDirectory = dossier_save
            
            # Appelle une méthode d'Explorer pour récupérer le chemin du fichier contenant les chemins audio
            full_path = self.explo.explorer_dossier_gui(dossier_save) 
            
            # Ouvre le fichier contenant les chemins des fichiers audio en mode lecture
            i = 0
            with open(full_path, 'r', encoding='utf-8') as f:
                # Lit chaque ligne du fichier
                for ligne in f:
                    chemin_Audi = ligne.strip()  # Supprime les espaces blancs au début et à la fin
                    
                    # Obtient le chemin absolu du fichier audio
                    cheminAudio = os.path.abspath(chemin_Audi)
                    
                    # Remplace les antislashs par des barres obliques pour la compatibilité
                    cheminVar = cheminAudio.replace("\\", "/") 

                    # Récupère seulement le nom du fichier à partir du chemin
                    nom_fichier = os.path.basename(cheminVar)
                    # Ajouter une nouvelle paire clé-valeur
                    varchar = str(i)
                    self.mon_dictionnaire[varchar] = f"{cheminVar}"
                    i += 1  # Incrémenter le compteur pour les clés du dictionnaire

                    # Insère le nom du fichier dans la Listbox
                    self.audio_listbox.insert(tk.END, nom_fichier)
                    self.tailleListbox = self.audio_listbox.size()
            self.audio_listbox.selection_set(0)  # Sélectionne le premier élément
            self.buttnext = 0  

    def AZEexploration_dossier(self, path):
        """Ouvre un dossier pour explorer et charger des fichiers audio à partir d'un chemin donné."""
        dossier = None
        if path is None:
            # Ouvre une boîte de dialogue pour sélectionner un dossier et stocke le chemin dans 'dossier'.
            dossier = filedialog.askdirectory() 
        else:
            dossier = path 
        
        # Vérifie si un dossier a été sélectionné
        if dossier:
            # Efface le contenu actuel de la Listbox pour éviter les doublons
            self.audio_listbox.delete(0, tk.END)

            # Remplace les antislashs (\) par des barres obliques (/) pour la compatibilité
            dossier_save = dossier.replace("\\", "/") 
            self.varDirectory = dossier_save
            
            # Appelle une méthode d'Explorer pour récupérer le chemin du fichier contenant les chemins audio
            full_path = self.explo.explorer_dossier_gui(dossier_save) 
            
            # Ouvre le fichier contenant les chemins des fichiers audio en mode lecture
            i = 0
            with open(full_path, 'r', encoding='utf-8') as f:
                # Lit chaque ligne du fichier
                for ligne in f:
                    chemin_Audi = ligne.strip()  # Supprime les espaces blancs au début et à la fin
                    
                    # Obtient le chemin absolu du fichier audio
                    cheminAudio = os.path.abspath(chemin_Audi)
                    
                    # Remplace les antislashs par des barres obliques pour la compatibilité
                    cheminVar = cheminAudio.replace("\\", "/") 

                    # Récupère seulement le nom du fichier à partir du chemin
                    nom_fichier = os.path.basename(cheminVar)
                    # Ajouter une nouvelle paire clé-valeur
                    varchar = str(i)
                    self.mon_dictionnaire[varchar] = f"{cheminVar}"
                    i += 1  # Incrémenter le compteur pour les clés du dictionnaire
                    self.tailleListbox = self.audio_listbox.size()

                    # Insère le nom du fichier dans la Listbox
                    self.audio_listbox.insert(tk.END, nom_fichier)

    def affiche_path_label(self, event):
        """Affiche les détails du fichier audio sélectionné dans la Listbox."""
        pygame.mixer.music.unload()
        audio = None
        self.verif_lecture = False
        
        # Récupérer l'index du fichier sélectionné dans la Listbox
        select_index = self.audio_listbox.curselection() 
        self.buttnext = select_index[0] 
        self.Varbutt = "1"  # Indique qu'un fichier a été sélectionné
        
        if select_index:
            # Obtenir le chemin du fichier audio sélectionné
            varstr = str(self.buttnext)
            audio_path = self.mon_dictionnaire[varstr]
            # Récupère seulement le nom du fichier à partir du chemin
            nom_fichier = os.path.basename(audio_path)
            self.B1_label_fichier_nom.config(text=nom_fichier)
            
            # Extraire et afficher les métadonnées de l'audio
            self.metadata_str = self.extract.extraction_et_afficher_tag(audio_path)
            self.metaData_label.config(text=self.metadata_str)  # Afficher les métadonnées dans path_label3
            
            self.cover_image(audio_path)  # Affiche l'image de couverture
            self.chemin_audio = audio_path
            print("audio_pathùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùùù")
            print(audio_path)
            
            if self.audio_lecture:  # Si un audio est déjà en lecture
                self.lire_audio()  # Lit le fichier audio

    def cover_image(self, audio_path):
        """Affiche la couverture de l'album pour le fichier audio sélectionné."""
        audio = None
        # Charger l'audio en fonction de son format
        try:
            if audio_path.endswith('.mp3'):
                audio = MP3(audio_path)  # Charge un fichier MP3
            elif audio_path.endswith('.flac'):
                audio = FLAC(audio_path)  # Charge un fichier FLAC
            else:
                self.metaData_label.config(text="Format non supporté")  # Format non supporté
                return
            
            # Extraire la couverture de l'album
            cover_image = None  # Initialisation de la variable de couverture
            
            # Pour MP3 : recherche d'APIC dans les tags
            if isinstance(audio, MP3):
                cover_image = next((tag.data for tag in audio.tags.values() if isinstance(tag, APIC)), None)
            # Pour FLAC : recherche des images
            elif isinstance(audio, FLAC):
                cover_image = next((picture.data for picture in audio.pictures if isinstance(picture, Picture)), None)
            
            image_album = None
            if cover_image:
                # Charger et redimensionner l'image de couverture
                image = Image.open(io.BytesIO(cover_image))
                image = image.resize((214, 214))  # Redimensionner l'image à la taille du label
                image_alb = ImageTk.PhotoImage(image)  # Convertir l'image pour Tkinter
                
                image_album = image_alb  
            else:
                # Charger l'image par défaut si aucune couverture n'est trouvée
                image_path = os.path.abspath(r"Python_project\img\images.jpeg")
                
                try:
                    image = Image.open(image_path)  # Ouvre l'image par défaut
                    image = image.resize((214, 214))  # Redimensionne l'image à la taille du label
                    photo = ImageTk.PhotoImage(image)

                    image_album = photo  # Garder une référence à l'image
                except Exception as e:
                    print("Erreur lors du chargement de l'image par défaut :", e)
                    self.A_label_cover.config(text="Erreur de chargement de l'image.")

            # Mettre à jour le label avec l'image de couverture
            self.A_label_cover.config(image=image_album)
            self.A_label_cover.image = image_album  # Garder une référence à l'image
            self.A_label_cover.config(text="")  # Effacer le texte pour afficher uniquement l'image
        except Exception as e:
            print("Erreur lors du traitement de l'audio :", e)
            self.metaData_label.config(text="Erreur lors du traitement de l'audio.")
        
    def switch_to_panel2(self):
        """Cache le panneau 1 et affiche le panneau 2."""
        self.panel1.pack_forget()  # Cache le panel1
        self.panel2.pack(fill="both", expand=True)  # Affiche le panel2

    def lire_audio(self):
        """Lance la lecture du fichier audio sélectionné."""
        select_index = self.audio_listbox.curselection()  
        varstr = ""  
        if self.Varbutt == "0":
            # Obtenir le chemin du fichier audio sélectionné
            varstr = str(self.buttnext)     
        elif self.Varbutt == "1":
            # Obtenir le chemin du fichier audio sélectionné
            varstr = str(select_index[0])
         # i = int(varstr)
         # while True:
        audio_path = self.mon_dictionnaire[varstr]
        # Récupère seulement le nom du fichier à partir du chemin
        nom_fichier = os.path.basename(audio_path)
        self.B1_label_fichier_nom.config(text=nom_fichier)
        self.ecoute.lire_fichier_audio(audio_path)  # Joue le fichier audio
        # Assurer que l'état est "lecture" et non "pause"
        self.is_paused = False
        self.butt_pause_reprendre.config(text="⏸")  # Met à jour le texte du bouton pour pause
        self.audio_lecture = True  # Indique que l'audio est en lecture
        self.verif_lecture = True
        
    def toggle_pause(self):
        """Met en pause ou reprend la lecture de l'audio."""
        self.verif_lecture = True
        if self.is_paused:
            self.reprendre()  # Reprend la lecture
            self.butt_pause_reprendre.config(text="⏸")  # Met à jour le texte du bouton
            self.is_paused = False
        else:
            self.pause()  # Met en pause la lecture
            self.butt_pause_reprendre.config(text="■")  # Met à jour le texte du bouton
            self.is_paused = True

    def annuler(self):
        """Ferme la fenêtre secondaire."""
        self.new_window.destroy()  # Ferme la fenêtre secondaire
        # self.playlist_window = False

    def par_defaut(self):
        """Restaure la valeur par défaut dans l'Entry et affiche cette valeur dans le label."""
        self.entry.delete(0, tk.END)  # Efface le contenu de l'Entry
        self.entry.insert(0, self.valeur_par_defaut)  # Insère la valeur par défaut
        chemin_play = self.playlist.gui_ecritureFichierxspf(self.varDirectory, None)  # Enregistre la playlist  
        self.afficher_notification(f"Playlist crée dans ce dossier : {os.path.abspath(chemin_play)}")
        self.new_window.destroy()  # Ferme la fenêtre secondaire
        # self.playlist_window = False

    def specifier(self):
        """Récupère le texte saisi et les options cochées, puis les écrit dans un fichier."""
        texte_saisi = self.entry.get()  # Récupère le texte saisi dans l'Entry
        print(texte_saisi)

        # Récupérer les chemins des options sélectionnées
        chemins_selectionnes = [path for var, path in zip(self.checkbox_vars, self.chemins_options) if var.get()]

 

        # Écrire les chemins sélectionnés dans un fichier
        with open(self.file_path_chemins, 'w') as f:
            for chemin in chemins_selectionnes:
                f.write(f"{chemin}\n")  # Écrire chaque chemin dans le fichier, suivi d'une nouvelle ligne

        # Afficher la notification avec le chemin enregistré
        chemin_play = self.playlist.gui_ecritureFichierxspf(self.file_path_chemins, texte_saisi)  # Enregistre la playlist avec le texte saisi
        self.afficher_notification(os.path.abspath(chemin_play))

        # Efface le contenu de l'Entry après avoir spécifié
        self.entry.delete(0, tk.END)  
        self.new_window.destroy()  # Ferme la fenêtre secondaire

    def open_new_fenetre(self):
        """Ouvre une nouvelle fenêtre pour gérer la playlist."""
        # Création d'une nouvelle fenêtre
        self.new_window = tk.Toplevel(root)
        self.new_window.title("Fenêtre Playlist")
        self.new_window.geometry("450x450")  # Taille de la fenêtre

        # Créer les cadres
        frame1_open_window = tk.Frame(self.new_window, bg=self.antiquewhite)
        frame2_open_window = tk.Frame(self.new_window, bg="gray")
        frame3_open_window = tk.Frame(self.new_window)  # Cadre général pour le canvas et la scrollbar

        frame1_open_window.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        frame3_open_window.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        frame2_open_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Zone de saisie (entrée de texte) avec valeur par défaut
        self.entry = tk.Entry(frame1_open_window, width=30)
        self.entry.insert(0, self.valeur_par_defaut)  # Insère la valeur par défaut dans l'Entry
        self.entry.pack(pady=10)

        # Création de la liste pour stocker les variables de case à cocher et les chemins
        self.checkbox_vars = []
        self.chemins_options = []

        # Créer un canvas
        self.canvas = tk.Canvas(frame3_open_window, bg="white")
        self.scrollbar = tk.Scrollbar(frame3_open_window, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        # Configuration du canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack le canvas et la scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Lire le fichier et créer des cases à cocher
        fichier_lire = os.path.abspath(r'python_project\FichierTemp\TempFile.txt')  
        self.options_fichier_lire(fichier_lire)

        # Création des boutons dans la nouvelle fenêtre
        button_annuler = tk.Button(frame2_open_window, text="Annuler", command=self.annuler)
        button_annuler.pack(side=tk.LEFT, padx=10, pady=10)

        button_par_defaut = tk.Button(frame2_open_window, text="Par défaut", command=self.par_defaut)
        button_par_defaut.pack(side=tk.LEFT, padx=10, pady=10)

        button_specifier = tk.Button(frame2_open_window, text="Spécifier", command=self.specifier)
        button_specifier.pack(side=tk.LEFT, padx=10, pady=10)

    def options_fichier_lire(self, filename):
        """Charge des options à partir d'un fichier et crée des cases à cocher."""
        try:
            with open(filename, 'r') as file:
                for line in file:
                    option = line.strip()  # Supprime les espaces autour
                    absolute_path = os.path.abspath(option)  # Obtenir le chemin absolu

                    # Créer une variable pour la case à cocher
                    var = tk.BooleanVar()
                    self.checkbox_vars.append(var)  # Ajouter la variable à la liste des variables de cases
                    self.chemins_options.append(absolute_path)  # Ajouter le chemin à la liste des chemins

                    # Créer la case à cocher dans le cadre défilant
                    checkbox = tk.Checkbutton(self.scrollable_frame, text=os.path.basename(option), variable=var, bg="white")
                    checkbox.pack(anchor=tk.W)  # Ancre à gauche
        except FileNotFoundError:
            print(f"Erreur : Le fichier '{filename}' n'a pas été trouvé.")
    
    def next_audio(self):
        """Passe à l'audio suivant dans la liste et met à jour l'affichage."""
        try:
            if self.tailleListbox > self.buttnext:  # Vérifie s'il y a un élément suivant
                self.next_item()  # Sélectionne l'élément suivant
                self.buttnext += 1  # Incrémente l'index
                varstr = str(self.buttnext)      

                audio_path = self.mon_dictionnaire[varstr]  # Récupère le chemin de l'audio suivant
                # Récupère seulement le nom du fichier à partir du chemin
                nom_fichier = os.path.basename(audio_path)
                self.B1_label_fichier_nom.config(text=nom_fichier)
                
                # Extraire et afficher les métadonnées de l'audio
                self.metadata_str = self.extract.extraction_et_afficher_tag(audio_path)
                self.metaData_label.config(text=self.metadata_str)  # Afficher les métadonnées dans path_label3
                
                self.cover_image(audio_path)  # Affiche l'image de couverture
                self.chemin_audio = audio_path
                self.Varbutt = "0"
                if self.audio_lecture:  # Si un audio est déjà en lecture
                    self.lire_audio()  # Lit le fichier audio
                    self.verif_lecture = True
        except IndexError:
            print("Erreur : Aucun audio suivant dans la liste.")
        except Exception as e:
            print("Erreur lors de la lecture de l'audio suivant :", e)

    def next_item(self):
        """Sélectionne l'élément suivant dans la Listbox."""
        if self.tailleListbox > self.buttnext:
            current_index = self.buttnext
            # Calcule l'index du prochain élément
            next_index = self.buttnext + 1
            self.audio_listbox.selection_clear(current_index)  # Désélectionne l'élément actuel
            self.audio_listbox.selection_set(next_index)  # Sélectionne le prochain élément
            self.audio_listbox.activate(next_index)  # Met le prochain élément en surbrillance

    def prev_audio(self):  
        """Passe à l'audio précédent dans la liste et met à jour l'affichage."""
        if 0 < self.buttnext:  # Vérifie s'il y a un élément précédent
            self.prev_item()  # Sélectionne l'élément précédent
            self.buttnext -= 1  # Décrémente l'index
            varstr = str(self.buttnext)      

            audio_path = self.mon_dictionnaire[varstr]  # Récupère le chemin de l'audio précédent
            # Récupère seulement le nom du fichier à partir du chemin
            nom_fichier = os.path.basename(audio_path)
            self.B1_label_fichier_nom.config(text=nom_fichier)
            
            # Extraire et afficher les métadonnées de l'audio
            self.metadata_str = self.extract.extraction_et_afficher_tag(audio_path)
            self.metaData_label.config(text=self.metadata_str)  # Afficher les métadonnées dans path_label3
            
            self.cover_image(audio_path)  # Affiche l'image de couverture
            self.chemin_audio = audio_path
            self.Varbutt = "0"
            if self.audio_lecture:  # Si un audio est déjà en lecture
                self.lire_audio()  # Lit le fichier audio
                self.verif_lecture = True

    def prev_item(self):
        """Sélectionne l'élément précédent dans la Listbox."""
        if 0 < self.buttnext:
            current_index = self.buttnext
            # Calcule l'index du précédent élément
            prev_index = self.buttnext - 1
            self.audio_listbox.selection_clear(current_index)  # Désélectionne l'élément actuel
            self.audio_listbox.selection_set(prev_index)  # Sélectionne le précédent élément
            self.audio_listbox.activate(prev_index)  # Met le précédent élément en surbrillance

    def pause(self):
        """Met en pause la lecture audio."""
        self.audio_lecture = False  # Met à jour l'état audio
        pygame.mixer.music.pause()  # Met en pause la musique

    def reprendre(self):
        """Reprend la lecture audio en pause."""
        self.audio_lecture = True  # Met à jour l'état audio
        pygame.mixer.music.unpause()  # Reprend la musique

    def rechercher(self):
        """Affiche les fichiers MP3 disponibles et ajoute un bouton pour revenir."""
        
        # Si le label existe déjà, on le cache au lieu de le recréer
        if hasattr(self, 'rechercher_label'):
            self.rechercher_label.pack_forget()  # Cache le label précédent
            self.scrollbar.pack_forget()  # Cache la scrollbar précédente
            self.rechercher_frame.pack_forget()  # Cache le cadre précédent

        # Crée et configure le bouton de retour
        self.butt_retour_api = tk.Button(self.frame1_haut, text="Retour", width=12, command=self.retour)
        self.butt_retour_api.pack(side=tk.LEFT, padx=10, pady=10)  # Aligné à droite

        # Cache le label des métadonnées
        self.metaData_label.pack_forget()
        self.reche = False

        # Créer un cadre pour le label et la scrollbar
        self.rechercher_frame = tk.Frame(self.section3_metaData, bg=self.lightyellow)
        self.rechercher_frame.pack(pady=10, fill='both', expand=True)

        # Créer un canvas pour la scrollbar
        self.canvas = tk.Canvas(self.rechercher_frame, bg=self.lightyellow)
        self.scrollbar = tk.Scrollbar(self.rechercher_frame, orient="vertical", command=self.canvas.yview, bg=self.lightyellow)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Configurer la scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack le canvas et la scrollbar
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Créer un label pour afficher le chemin complet du fichier sélectionné
        self.rechercher_label = Label(self.scrollable_frame, text="", width=70, justify="left", bg=self.lightyellow)
        self.rechercher_label.pack(pady=10, fill='both', expand=True)

        # Récupérer et afficher les données API
        data_api_affiche = self.fetcher_methode()
        self.rechercher_label.config(text=data_api_affiche)  # Mettre à jour le texte du label formaté
     
    def retour(self): 
        """Affiche les métadonnées du fichier audio sélectionné et cache le bouton de retour."""
        self.butt_retour_api.pack_forget()  # Cache le bouton de retour
        if self.reche == False: 
            # Label pour afficher le chemin complet du fichier sélectionné
            self.metaData_label = Label(self.section3_metaData, text="", width=70, height=10, justify="left", bg=self.lightyellow)
            self.metaData_label.pack(pady=10, fill='both', expand=True)  # Utiliser fill='both' et expand=True pour agrandir
            # Obtenir le chemin du fichier audio sélectionné
            varstr = str(self.buttnext)
            audio_path = self.mon_dictionnaire[varstr]
            
            # Extraire et afficher les métadonnées de l'audio
            
            self.metadata_str = self.extract.extraction_et_afficher_tag(audio_path)
            self.metaData_label.config(text=self.metadata_str)  # Afficher les métadonnées dans path_label3
            self.reche = True
            self.rechercher_label.pack_forget() 
            self.scrollable_frame.pack_forget()  # Cache le bouton de retour
            self.rechercher_frame.pack_forget()  # Cache le bouton de retour

    def destroy_notification(self):
        self.notification.destroy()  

    def afficher_notification(self, chemin_play):
        """Affiche une notification"""
        global notification, label, entry
        self.notification = Toplevel(root)
        self.notification.title("Notification")  # Titre de la fenêtre
        self.notification.geometry("700x100")  # Définir la taille de la fenêtre
        self.notification.resizable(False, False)  # Empêcher le redimensionnement

         # Créer un label pour afficher le message
        message_label = tk.Label(self.notification, text=f"Message : {chemin_play}", padx=20, pady=20)
        message_label.pack()

        # Créer un bouton pour fermer la notification
        close_button = tk.Button(self.notification, text="OK", command=self.destroy_notification)
        close_button.pack(pady=(0, 10))  # Ajouter un peu d'espace en bas
        # messagebox.showinfo("Notification", f"Playlist crée dans ce dossier : {chemin_play}")

    """    
    def ajoute_playlist(self,event):
        audio = None
        
        # Récupérer l'index du fichier sélectionné dans la Listbox
        select_index = self.audio_listbox.curselection() 
        self.buttnext = select_index[0] 
        self.Varbutt = "1"  # Indique qu'un fichier a été sélectionné
        
        if select_index:
            # Obtenir le chemin du fichier audio sélectionné
            varstr = str(self.buttnext)
            audio_path = self.mon_dictionnaire[varstr]
            # Récupère seulement le nom du fichier à partir du chemin
            nom_fichier = os.path.basename(audio_path)
            self.B1_label_fichier_nom.config(text=nom_fichier)
            
            # Extraire et afficher les métadonnées de l'audio
            self.metadata_str = self.extract.extraction_et_afficher_tag(audio_path)
            self.metaData_label.config(text=self.metadata_str)  # Afficher les métadonnées dans path_label3
            
            self.cover_image(audio_path)  # Affiche l'image de couverture
            
            if self.audio_lecture:  # Si un audio est déjà en lecture
                self.lire_audio()  # Lit le fichier audio
    """

    def fetcher_methode(self)-> str:
        # Récupérer la saisie de l'utilisateur, la nettoyer et la mettre en minuscules
        saisie = self.entry_ecriture_haut.get().strip().lower()
        
        # Vérifier si la saisie commence par "artiste:", "album:", ou "music:"
        if saisie.startswith("artiste:"):
            # Extraire le nom de l'artiste après "artiste:"
            artist_name = saisie[len("artiste:"):].strip()
            self.fetcher.get_artist_info(artist_name)
            auteur_saisie = self.fetcher.afficher_artiste_infos()
            return auteur_saisie
            
        elif saisie.startswith("album:"):
            # Extraire le nom de l'album après "album:"
            album_name = saisie[len("album:"):].strip()
            self.fetcher.get_album_info(album_name)
            album_saisie = self.fetcher.afficher_album_infos()
            return album_saisie

            
        elif saisie.startswith("music:"):
            # Extraire le nom de la musique après "musique:"
            track_name = saisie[len("music:"):].strip()
            self.fetcher.get_track_info(track_name)
            track_saisie = self.fetcher.afficher_track_infos()
            return track_saisie
        
        else:
            print("Commande non reconnue. Utilisez 'artiste:', 'album:', ou 'music:' pour effectuer une recherche.")

    def modification_data(self):
        """Ouvre une nouvelle fenêtre pour modifier les métadonnées de la playlist."""
        # if self.affiche_window == False:
        global modif_window
        modif_window = Toplevel(root)
        modif_window.title("Modification de métadonnées")
        modif_window.geometry("300x500")  # Augmenter la taille de la fenêtre pour inclure la couverture
        modif_window.resizable(False, False)  # Empêche la redimension de la fenêtre
        

        # Créer deux cadres pour organiser la disposition
        self.frame1_modif_window = tk.Frame(modif_window, bg=self.antiquewhite)
        self.frame2_modif_window = tk.Frame(modif_window, bg="gray")

        # Pack les cadres dans la fenêtre
        self.frame1_modif_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.frame2_modif_window.pack(fill=tk.X)
        
        dict_metadata_str = self.convertir_metadata_en_dict(self.metadata_str)
        list_metadata_str = list(dict_metadata_str.values())

        # Liste des champs et de leurs labels
        labels_text = ["Titre", "Artiste", "Album", "Genre", "Date", "Organisation"]
        self.entries = {}  # Dictionnaire pour stocker les entrées associées aux labels

        # Création des labels et zones de saisie
        i = 0
        for label_text in labels_text:
            # Label
            label = tk.Label(self.frame1_modif_window, text=label_text, bg=self.antiquewhite)
            label.pack(anchor="w", padx=5, pady=3)

            # Zone de saisie
            entry = tk.Entry(self.frame1_modif_window, width=30)
            entry.pack(anchor="w", padx=5, pady=3)

            # Ajouter l'entrée au dictionnaire avec le nom du champ en clé
            self.entries[label_text.lower()] = entry

            # Ajouter la valeur par défaut dans le champ de saisie
            entry.insert(0, list_metadata_str[i])  # Insère la valeur par défaut
            i += 1

        # Ajout de la sélection de cover
        cover_label = tk.Label(self.frame1_modif_window, text="Cover", bg=self.antiquewhite)
        cover_label.pack(anchor="w", padx=5, pady=3)

        # Afficher une image de prévisualisation de la cover
        self.cover_image_path = None

        # Bouton pour sélectionner une image de couverture
        select_cover_button = tk.Button(self.frame1_modif_window, text="Sélectionner une couverture", command=self.select_cover_image)
        select_cover_button.pack(anchor="w", padx=5, pady=3)

        # Boutons dans la deuxième section
        button_cancel = tk.Button(self.frame2_modif_window, text="Annuler", command=self.but_cancel)
        button_cancel.pack(side=tk.LEFT, padx=10, pady=10)

        button_pour_ok = tk.Button(self.frame2_modif_window, text="Enregistrer", command=self.save_modification)
        button_pour_ok.pack(side=tk.LEFT, padx=10, pady=10)
            # self.affiche_window = True
        chemin_audio = self.chemin_audio
        print("chemin_audiorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
        print(chemin_audio)

    def select_cover_image(self):
        """Ouvre une boîte de dialogue pour sélectionner une image de couverture."""
        file_path = filedialog.askopenfilename(title="Sélectionner une couverture", filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.cover_image_path = file_path
 
    def but_cancel(self):
        """Ferme la fenêtre secondaire."""
        modif_window.destroy()  # Ferme la fenêtre secondaire
        # self.affiche_window = False

    def convertir_metadata_en_dict(self,metadata_str: str) -> dict:
        """Convertit une chaîne de métadonnées en un dictionnaire."""
        metadata_dict = {}
        
        # Sépare la chaîne en lignes
        lignes = metadata_str.strip().split("\n")
        
        for ligne in lignes:
            if ':' in ligne:  # Vérifie si la ligne contient un deux-points
                cle, valeur = ligne.split(':', 1)  # Sépare la clé et la valeur
                metadata_dict[cle.strip()] = valeur.strip()  # Ajoute à la dict en supprimant les espaces

        return metadata_dict

    def save_modification(self):
        pygame.mixer.music.stop
        pygame.mixer.music.unload()
        # Récupérer le chemin audio de l'attribut de la classe
        chemin_audio = self.chemin_audio
        print("chemin_audioiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        print(chemin_audio)

        # Récupérer les valeurs des champs de saisie
        titre = self.entries["titre"].get()
        artiste = self.entries["artiste"].get()
        album = self.entries["album"].get()
        genre = self.entries["genre"].get()
        ladate = self.entries["date"].get()
        organisation = self.entries["organisation"].get()
        
        # Récupérer le chemin de l'image de cover (si sélectionnée)
        chemin_image = self.cover_image_path if self.cover_image_path else None

        self.metaData_label.pack_forget() 

        # Appeler la méthode pour afficher et modifier les métadonnées
        self.edite.afficher_et_modifier_metadata(chemin_audio, chemin_image, titre, artiste, album, genre, ladate, organisation)

        # Fermer la fenêtre de modification
        self.metaData_label = Label(self.section3_metaData, text="", width=70, height=10, justify="left", bg=self.lightyellow)
        self.metaData_label.pack(pady=10, fill='both', expand=True)  # Utiliser fill='both' et expand=True pour agrandir

        # Actualiser l'affichage des métadonnées
        self.metadata_str = self.extract.extraction_et_afficher_tag(chemin_audio)
        self.metaData_label.config(text=self.metadata_str)
        self.cover_image(chemin_audio)  # Affiche l'image de couverture
        self.chemin_audio = chemin_audio
        modif_window.destroy()
        # self.affiche_window = False


        
# Création de la fenêtre principale
if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)  # Création de l'instance de l'application
    root.mainloop()  # Lancer la boucle principale
