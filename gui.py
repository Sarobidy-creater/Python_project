#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import io
import time
import pygame  
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import *
from tkinter import filedialog, Listbox, Scrollbar, Label, PhotoImage, messagebox
from PIL import Image, ImageTk
from mutagen.easyid3 import EasyID3  # Pour lire et écrire les métadonnées ID3 dans les fichiers MP3.
from mutagen.mp3 import MP3  # Pour gérer les fichiers audio MP3 et accéder à leurs métadonnées.
from mutagen.id3 import ID3, APIC  # Pour manipuler les balises ID3 et gérer les images intégrées comme les couvertures d'album.
from mutagen.flac import FLAC, Picture  # Pour travailler avec les fichiers audio FLAC et gérer les images intégrées.
from library.ecouterAudio import Ecouter # Importe la classe Ecouter du module ecouterAudio pour lire un fichier audio mp3 ou flac dans la console
from library.explorationDossier import Explorer  # Importe la classe Explorer pour explorer les dossiers
from library.constitutionPlaylist import Playlist  # Importe la classe Playlist du module constitutionPlaylist pour générer des playlists
from library.audioTagExtraction import Extraction  # Importe la classe Extraction du module audioTagExtraction pour extraire les métadonnées audio
from library.fetcher import Fetcher # Importe la classe Fetcher pour gérer la connection afin d'utiliser l'API
from library.audioMetaEdite import Editer # Importe la classe Editer pour éditer les métadonnées d'un fichier audio




class Interface:
    def __init__(self, master):
        """Initialisation de l'interface et création des composants graphiques"""
        self.master = master
        self.master.title("Lecteur Audio")  # Titre de la fenêtre
        self.master.state("zoomed")  # Agrandir la fenêtre à l'écran

        # Initialisation des variables pour gérer l'interface et les fonctionnalités
        self.mon_dictionnaire = {}  # Dictionnaire pour stocker les fichiers audio (chemin absolu fichiers audio)
        self.tab_play = {} # Dictionnaire pour stocker les playlist et fichier (chemin absolu playlist)
        self.explo = Explorer()  # Instance de la classe Explorer pour parcourir les dossiers
        self.ecoute = Ecouter()  # Instance de la classe Ecouter pour lire les fichiers audio
        self.playlist = Playlist()  # Instance de la classe Playlist pour gérer les playlists
        self.extract = Extraction()  # Instance de la classe Extraction pour extraire les métadonnées audio
        self.fetcher = Fetcher() # Instance de la classe Fetcher pour gérer la connection afin d'utiliser l'API
        self.edite = Editer() # Instance de la classe Editer pour éditer les métadonnées d'un fichier audio
        self.varDirectory = ""  # Variable pour stocker le chemin du répertoire exploré
        self.valeur_par_defaut = "maPlaylist"  # Valeur par défaut de l'entrée de texte pour nommer la playlist
        self.playlist_defaut = "" # Nom par défaut d'une playlist par défaut
        self.is_paused = False  # Variable pour suivre si la lecture est en pause
        self.is_playlist = False # Variable pour informer si c'est une playlist ou pas lors insertion dans la listbox
        self.Varbutt = None  # Variable pour suivre l'élément audio actuellement joué
        self.buttnext = 0  # Variable pour naviguer entre les fichiers audio
        self.tailleListbox = 0  # Taille de la liste des fichiers audio
        self.audio_lecture = False  # Variable pour indiquer létat de lecture d'un audio (uniquement quand ça marche)
        self.reche = False # Variable pour indiquer qu'on a fait une recherche  (quand on veut creer ou modifier une playlist)
        self.exist_play = False  # Variable pour indiquer si la playlist existe ou pas
        self.reche_retour = False # Variable pour indiquer qu'on a fait un retour après avoir fait une recherche
        self.modification_fichier_play= True # Indique si les fichiers playlist peuvent être modifiés
        self.lightyellow = "lightyellow"  # Couleur de fond pour certaines parties de l'interface
        self.dodgerblue = "dodgerblue"  # Couleur de fond pour d'autres parties
        self.antiquewhite = "antiquewhite"  # Autre couleur de fond
        self.metadata_str = "" # variable pour mettre les métadonnées de l'audio
        self.chemin_audio = "" # variable pour mettre le chemin complet du fichier audio en cours  
        self.varstr = "" # variable pour la clé du chemin complet du fichier audio en cours 
        self.final_lecture = False # Variable pour indiquer qu'un fichier audio et chargé en lecture (pause ou quand ça marche)
        self._open_window  = False # Variable pour indiquer létat de la fenêtre pour gérer la playlist (fenêtre ouverte ou non)
        # self.playlist_window = False
        # self._specifier = False
        self.affiche_window = False # Attribut pour suivre si la fenêtre de modification est ouverte
        self.max_length = 78 # Variable pour la taille de l'affichage du nom de l'audio dans la listebox
        self.max_length_milieu  = 38 # Variable pour la taille de l'affichage sous la cover
        self.checkbox_vars = []  # Pour stocker les variables de cases à cocher
        self.chemins_options = []  # Pour stocker les chemins des options
        self.file_path_chemins = os.path.abspath(r'python_project\FichierTemp\options_selectionnees.txt')  # Chemin du fichier pour écrire les options sélectionnées
        self.fichier_lire = os.path.abspath(r'python_project\FichierTemp\TempFile.txt')  # Fichier temporaire pour lecture de données
        self.chem_im = os.path.abspath(r"Python_project/img/nn.webp")  # Chemin de l'image par défaut pour l'interface
        self.chem__music = os.path.abspath(r"Python_project\music")  # Répertoire par défaut pour les fichiers musicaux
        self.image_path = os.path.abspath(r"Python_project\img\images.jpeg")  # Image par défaut pour la couverture d'album
        self.creation_interface() 
         
    def creation_interface(self) -> None:  
        """
            Fonction qui efféctue la création et structuration de l'interface.

            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """

        # **************************************************************************
        # Création des différents panneaux de l'interface

        ##  ******Panel 1****** : Panneau d'ouverture fond bleu ciel avec une image et un bouton

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

        ##  ******Panel 2****** : Panneau avec toutes les fonctionnalités

        self.panel2 = tk.Frame(self.master, bg=self.lightyellow)

        # Créer trois cadres avec des tailles différentes
        self.frame1_haut = tk.Frame(self.panel2, bg=self.antiquewhite)
        self.frame2_centre = tk.Frame(self.panel2, bg="gray")
        self.frame3_bas = tk.Frame(self.panel2, bg=self.dodgerblue)

        # Pack les cadres avec des tailles différentes
        self.frame1_haut.pack(fill=tk.X, padx=5, pady=5) 
        self.frame2_centre.pack(fill=tk.BOTH, expand=True, padx=5, pady=5) 
        self.frame3_bas.pack(fill=tk.X, padx=5, pady=5) 

        # Cadre 1.#******************************************#

        # Label pour indiquer a l'utilisateur la où il faut écrire
        self.label_Check = tk.Label(self.frame1_haut, text="Entrez votre recherche :")
        self.label_Check.pack(side=tk.LEFT, padx=10, pady=10)

        # Zone de saisie de l'utilisateur pour utiliser l'API
        self.entry_ecriture_haut = tk.Entry(self.frame1_haut, width=105)
        self.entry_ecriture_haut.pack(side=tk.LEFT, padx=5, pady=5)

        # Bouton pour lancer la recherche avec l'API
        self.butt_check_api = tk.Button(self.frame1_haut, text="Check", width=12, command=self.rechercher)
        self.butt_check_api.pack(side=tk.LEFT, padx=10, pady=10)  # Aligné à droite
    
        # Bouton de retour pour revenir a la fenetre avant et enlève la recherche de l'API
        self.butt_retour_api = tk.Button(self.frame1_haut, text="Retour", width=12, command=self.retour)
        self.butt_retour_api.pack(side=tk.LEFT, padx=10, pady=10)  # Aligné à droite

        # Bouton pour modifier les méta données pour un fichier audio donnée
        self.butt_modif_metaData = tk.Button(self.frame1_haut, text=":::", width=12, command=self.modification_data)
        self.butt_modif_metaData.pack(side=tk.RIGHT, padx=10, pady=10) 

        # Cadre 2.#******************************************#
        # Configurer le grid pour 3 colonnes de taille égale
        self.frame2_centre.grid_columnconfigure(0, weight=1)
        self.frame2_centre.grid_columnconfigure(1, weight=1)
        self.frame2_centre.grid_columnconfigure(2, weight=1)
        self.frame2_centre.grid_rowconfigure(0, weight=1)  # Une seule ligne

        # Créer trois sous-sections dans frame2 (gauche, centre, droite) avec les mêmes dimensions
        # section gauche pour mettre la liste des audios
        self.section1_gauche_liste = tk.Frame(self.frame2_centre, bg=self.antiquewhite)
        self.section1_gauche_liste.grid(row=0, column=0, sticky='nse', padx=5, pady=5)

        # section centre pour afficher le cover d'un fichier audio et les boutons pour écouter etc
        self.section2_centre_cover = tk.Frame(self.frame2_centre, bg=self.lightyellow)
        self.section2_centre_cover.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        # section droite pour afficher les méta données d'un audio 
        self.section3_metaData = tk.Frame(self.frame2_centre, bg=self.lightyellow)
        self.section3_metaData.grid(row=0, column=2, sticky='nsw', padx=2, pady=2)
        
        # Dans le cadre 2.++++++++++++++++++++++++++++++++++++++
        # Créer une liste pour afficher les fichiers MP3
        self.audio_listbox = Listbox(self.section1_gauche_liste, width=80, height=10, bg=self.antiquewhite, selectbackground=self.dodgerblue)  # Ajuster la taille ici
        self.audio_listbox.pack(side=tk.LEFT, fill='both', expand=True)

        # Lier le double-clic à la lecture et l'affichage du titre
        self.audio_listbox.bind("<Double-Button-1>", self.affiche_path_label)

        # Ajouter une barre de défilement a la listbox
        self.scrollbarlistbox = Scrollbar(self.section1_gauche_liste)
        self.scrollbarlistbox.pack(side=tk.RIGHT, fill=tk.Y, padx=0, pady=0)  # Assurer aucun espacement

        # Lier la barre de défilement à la Listbox
        self.audio_listbox.config(yscrollcommand=self.scrollbarlistbox.set)
        self.scrollbarlistbox.config(command=self.audio_listbox.yview)

        # Label pour qui va contenir le cover d'un fichier audio et les boutons pour écouter etc et le nom du fichier
        self.centrale_label = Label(self.section2_centre_cover, text="", width=70, height=10, justify="left", bg=self.lightyellow)
        self.centrale_label.pack(pady=10, fill='both', expand=True) 

        # Label pour va contenir le cover d'un fichier audio
        self.A_label_cover = Label(self.centrale_label, text="", width=90, height=111, justify="left", bg=self.lightyellow)
        self.A_label_cover.pack(pady=10, fill='both', expand=True) 

        # Label pour va contenir les boutons pour écouter, mettre en paus etc et le nom du fichier
        self.B_label_fichier_boutton = Label(self.centrale_label, text="", width=30, height=1, justify="left", bg=self.lightyellow)
        self.B_label_fichier_boutton.pack(pady=10, fill='both', expand=True) 

        # Label pour va afficher le nom du fichier sélectioné
        self.B1_label_fichier_nom = Label(self.B_label_fichier_boutton, text="", width=2, height=1, justify="left", bg=self.lightyellow)
        self.B1_label_fichier_nom.pack(pady=10, fill='both', expand=True) 

        # Label pour va contenir les boutons pour écouter, mettre en paus etc 
        self.B2_label_bouton_manip = Label(self.B_label_fichier_boutton, text="", width=11, height=1, justify="left", bg=self.lightyellow)
        self.B2_label_bouton_manip.pack(pady=10, fill='both', expand=True)  

        # Label pour afficher les méta donnees d'un fichier audio sélectioné
        self.metaData_label = Label(self.section3_metaData, text="", width=70, height=10, justify="left", bg=self.lightyellow)
        self.metaData_label.pack(pady=10, fill='both', expand=True)
        

        # Cadre 3******************************************
        # Configurer le grid pour 3 colonnes de taille égale
        self.frame3_bas.grid_columnconfigure(0, weight=1)  # Sect1
        self.frame3_bas.grid_columnconfigure(1, weight=3)  # Sect2 (plus large)
        self.frame3_bas.grid_columnconfigure(2, weight=3)  # Sect3

        self.frame3_bas.grid_rowconfigure(0, weight=1)  # Une seule ligne

        # Label va contenir les boutons pour parcourir, créer une playlist et pour écouter une playlist 
        self.explo_playlist_boutton = tk.Frame(self.frame3_bas, bg=self.lightyellow, width=28)
        self.explo_playlist_boutton.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)

        # Label vide pour le moment
        self.petit_zone_vide = tk.Frame(self.frame3_bas, bg=self.dodgerblue)
        self.petit_zone_vide.grid(row=0, column=1, sticky='nsew',padx=2, pady=2)

        # Label qui contient le petit logo en bas
        self.zone_petit_logo = tk.Frame(self.frame3_bas, bg=self.dodgerblue)
        self.zone_petit_logo.grid(row=0, column=2, sticky='nsew',padx=2, pady=2)

        # logo image en bas pour le style de l'interface du panneau 2
        chem_im = self.chem_im 
        self.im = Image.open(chem_im)  # Remplace par le chemin de ton image
        self.im = self.im.resize((24, 24))  # Redimensionner si nécessaire
        self.im_tk = ImageTk.PhotoImage(self.im)
        self.label_img_petit_logo = tk.Label(self.zone_petit_logo, image=self.im_tk, bg=self.dodgerblue)
        self.label_img_petit_logo.pack(side=tk.RIGHT, padx=10, pady=10) 

        # QUE Des Boutons******************************************
        # Création d'un bouton pour explorer les dossiers audio
        self.butt_exploration = tk.Button(self.explo_playlist_boutton, text="Exploration", command=self.exploration_dossier, width=13)
        self.butt_exploration.pack(side=tk.LEFT, padx=10, pady=10)  # Positionné à gauche avec un espacement horizontal et vertical
        
        # Création d'un bouton pour écouter une playlist
        self.butt_playlist = tk.Button(self.explo_playlist_boutton, text="Ecouter", command=self.ecouter_playlist, width=13)
        self.butt_playlist.pack(side=tk.RIGHT, padx=10, pady=10)  # Positionné à droite avec un espacement horizontal et vertical

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

        # Fonctionnalité pour mettre le lien entre la fonction direct_goto au bouton du clavier retourner a la ligne
        self.master.bind("<Return>", self.direct_Goto) 

    def direct_Goto(self, event=None) -> None:  
        """
            Fonction qui efféctue le passage au panneau 2 et chargement de la musique par défaut.

            Paramètre :
            - event

            Retourne :
            - None : Aucune valeur de retour.
        """
        # Passe à l'affichage du panneau 2, celui qui contient les fonctionnalités principales
        self.switch_to_panel2() 
        
        # Définir le répertoire de musique par défaut à explorer
        chem = self.chem__music
        
        # Lancer l'exploration du dossier contenant les fichiers musicaux par défaut
        self.AZEexploration_dossier(chem) 
        
        # Récupère le premier fichier audio dans le dictionnaire (présumé être la première musique à jouer)
        audio_path = self.mon_dictionnaire["0"]
        
        # Récupère seulement le nom du fichier audio à partir du chemin complet
        chemin_nom_fichier = os.path.basename(audio_path)
        
        # Vérifie et ajuste le nom du fichier pour ne pas le couper de façon incorrecte
        nom_fichier = self.verifier_et_couper_nom_Milieu(chemin_nom_fichier)
        
        # Affiche le nom du fichier sélectionné dans l'interface utilisateur
        self.B1_label_fichier_nom.config(text=nom_fichier)
        
        # Utilise la classe Extraction pour obtenir et afficher les métadonnées du fichier audio
        self.metadata_str = self.extract.extraction_et_afficher_tag(audio_path)
        
        # Affiche les métadonnées dans le label prévu à cet effet dans l'interface
        self.metaData_label.config(text=self.metadata_str)
        
        # Affiche l'image de couverture de l'album du fichier audio
        self.cover_image(audio_path)  
        
        # Stocke le chemin du fichier audio en cours dans une variable
        self.chemin_audio = audio_path
        
        # Indique qu'un fichier audio est en cours de lecture
        self.Varbutt = True
        
        # Réinitialise l'index pour naviguer à travers les fichiers audio
        self.buttnext = 0
        
        # Sélectionne le premier fichier dans la liste (Listbox) pour le mettre en surbrillance
        self.audio_listbox.selection_set(self.buttnext)
        
        # Indique que la lecture ne provient pas d'une playlist, mais d'un fichier individuel
        self.is_playlist = False
        
        # Vide le dictionnaire des playlists, puisqu'on n'en joue pas pour le moment
        self.tab_play.clear() 
        
        # Charge toutes les playlists disponibles dans l'explorateur de playlists
        self.tab_play = self.explo.explorer_Playlist()

    def exploration_dossier(self) -> None:
        """
        Fonction qui ouvre un dossier pour explorer et charger des fichiers audio.

        Paramètre :
        - None : Aucune valeur en paramètre.

        Retourne :
        - None : Aucune valeur de retour.
        """

        # Si une fenêtre d'exploration est déjà ouverte, annule l'exploration en cours
        if(self._open_window == True):
            self.annuler()
        
        # Ouvre une boîte de dialogue pour sélectionner un dossier et stocke le chemin dans 'dossier'
        dossier = filedialog.askdirectory()
        
        # Vérifie si un dossier a été sélectionné (dossier n'est pas vide)
        if dossier:
            # Efface le contenu actuel de la Listbox pour éviter les doublons avant de charger de nouveaux fichiers
            self.audio_listbox.delete(0, tk.END)

            # Remplace les antislashs (\) par des barres obliques (/) pour garantir la compatibilité des chemins
            dossier_save = dossier.replace("\\", "/") 
            self.varDirectory = dossier_save
            
            # Appelle la méthode explorer_dossier_gui de l'explorateur pour récupérer le chemin complet du fichier contenant les chemins audio
            full_path = self.explo.explorer_dossier_gui(dossier_save) 
            
            # Initialise un compteur pour indexer les fichiers audio
            i = 0

            # Vide le dictionnaire avant de le remplir avec les nouveaux fichiers audio
            self.mon_dictionnaire.clear()

            # Ouvre le fichier contenant les chemins des fichiers audio en mode lecture
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()

                # Si le fichier est vide (pas de contenu), affiche une notification
                if not content:
                    message = "Aucun fichier audio trouvé dans ce dossier."
                    self.afficher_notification(message)
                    self.direct_Goto(event=None)  # Passe au panneau 2 après la notification

                else:
                    # Si des fichiers audio sont présents, remet le pointeur du fichier au début
                    f.seek(0)

                    # Parcourt chaque ligne du fichier pour traiter les chemins des fichiers audio
                    for ligne in f:
                        chemin_Audi = ligne.strip()  # Supprime les espaces blancs au début et à la fin de la ligne
                        
                        # Obtient le chemin absolu du fichier audio
                        cheminAudio = os.path.abspath(chemin_Audi)
                        
                        # Remplace les antislashs (\) par des barres obliques (/) pour garantir la compatibilité
                        cheminVar = cheminAudio.replace("\\", "/")

                        # Récupère uniquement le nom du fichier à partir du chemin complet
                        nom_cheminVar = os.path.basename(cheminVar)
                        nom_fichier = self.verifier_et_couper_nom_fichier(nom_cheminVar)
                        
                        # Ajoute chaque fichier audio au dictionnaire avec une clé numérique
                        varchar = str(i)
                        self.mon_dictionnaire[varchar] = f"{cheminVar}"
                        i += 1  # Incrémente le compteur pour générer des clés uniques pour chaque fichier

                        # Insère le nom du fichier dans la Listbox pour affichage à l'utilisateur
                        self.audio_listbox.insert(tk.END, nom_fichier)
                        
                        # Met à jour la taille de la Listbox
                        self.tailleListbox = self.audio_listbox.size()
            
            # Sélectionne le premier fichier dans la Listbox après avoir ajouté tous les fichiers
            self.audio_listbox.selection_set(0)
            
            # Initialisation de la variable qui indique quel fichier est sélectionné (ici le premier fichier)
            self.buttnext = 0  
            
            # Indique que l'on ne joue pas une playlist mais un fichier individuel
            self.is_playlist = False

    def AZEexploration_dossier(self, path: str) -> None:
        """
        Fonction qui ouvre un dossier pour explorer et charger des fichiers audio à partir d'un chemin donné.

        Paramètre :
        - path: str : Chemin absolu du dossier à analyser, y compris les sous-dossiers.

        Retourne :
        - None : Aucune valeur de retour.
        """
        
        # Initialisation de la variable 'dossier' à None
        dossier = None
        
        # Si aucun chemin n'est fourni, ouvrir une boîte de dialogue pour sélectionner un dossier
        if path is None:
            dossier = filedialog.askdirectory()  # Ouvre une boîte de dialogue pour la sélection du dossier
        else:
            dossier = path  # Utilise le chemin fourni si un paramètre 'path' est donné
        
        # Vérifie si un dossier a été sélectionné ou fourni
        if dossier:
            # Efface tous les éléments actuels dans la Listbox pour éviter les doublons
            self.audio_listbox.delete(0, tk.END)
            
            # Remplace les antislashs par des barres obliques pour assurer la compatibilité des chemins
            dossier_save = dossier.replace("\\", "/")
            
            # Stocke le chemin du dossier sélectionné dans une variable pour l'utiliser plus tard
            self.varDirectory = dossier_save
            
            # Appelle la méthode d'exploration pour obtenir le chemin complet du fichier contenant les chemins des fichiers audio
            full_path = self.explo.explorer_dossier_gui(dossier_save)
            
            # Initialise un compteur pour la gestion des clés dans le dictionnaire
            i = 0
            
            # Ouvre le fichier contenant les chemins des fichiers audio (chemins relatifs ou absolus)
            with open(full_path, 'r', encoding='utf-8') as f:
                # Parcourt chaque ligne du fichier
                for ligne in f:
                    chemin_Audi = ligne.strip()  # Enlève les espaces blancs inutiles autour du chemin
                    
                    # Convertit le chemin relatif en chemin absolu
                    cheminAudio = os.path.abspath(chemin_Audi)
                    
                    # Remplace les antislashs par des barres obliques pour assurer la compatibilité avec différents systèmes
                    cheminVar = cheminAudio.replace("\\", "/")
                    
                    # Extrait seulement le nom du fichier à partir du chemin complet
                    nom_cheminVar = os.path.basename(cheminVar)
                    
                    # Vérifie et ajuste le nom du fichier pour qu'il s'affiche correctement
                    nom_fichier = self.verifier_et_couper_nom_fichier(nom_cheminVar)
                    
                    # Ajoute une nouvelle entrée dans le dictionnaire pour garder une trace des fichiers audio
                    varchar = str(i)  # Crée une clé unique pour chaque fichier audio
                    self.mon_dictionnaire[varchar] = f"{cheminVar}"
                    
                    # Incrémente le compteur pour passer à la prochaine clé
                    i += 1
                    
                    # Récupère la taille actuelle de la Listbox
                    self.tailleListbox = self.audio_listbox.size()
                    
                    # Insère le nom du fichier dans la Listbox pour l'affichage
                    self.audio_listbox.insert(tk.END, nom_fichier)

    def affiche_path_label(self, event) -> None:
        """
        Fonction qui affiche les détails du fichier audio sélectionné dans la Listbox.

        Paramètre :
        - event : L'événement lié à la sélection dans la Listbox.

        Retourne :
        - None : Aucune valeur de retour.
        """
        
        # Initialisation de la variable pour l'audio et la vérification de lecture
        audio = None
        self.verif_lecture = False
        
        # Vérifie si la Listbox contient des éléments
        if self.tailleListbox > 0: 
            
            # Récupère l'index du fichier sélectionné dans la Listbox
            select_index = self.audio_listbox.curselection()
            
            # Si un fichier est sélectionné
            if select_index:
                # Récupère l'index du fichier sélectionné
                self.buttnext = select_index[0]
                
                # Indique que le fichier est sélectionné et n'est pas en lecture (préparation pour un changement de lecture)
                self.Varbutt = False  
                
                # Obtient le chemin du fichier audio correspondant à l'index sélectionné dans le dictionnaire
                varstr = str(self.buttnext)
                audio_path = self.mon_dictionnaire[varstr]
                
                # Récupère uniquement le nom du fichier audio à partir du chemin complet
                chemin_nom_fichier = os.path.basename(audio_path)
                
                # Vérifie et ajuste le nom du fichier pour éviter toute coupure incorrecte du nom
                nom_fichier = self.verifier_et_couper_nom_Milieu(chemin_nom_fichier)
                
                # Affiche le nom du fichier dans l'interface utilisateur
                self.B1_label_fichier_nom.config(text=nom_fichier)

                # Extraire et afficher les métadonnées du fichier audio sélectionné
                self.metadata_str = self.extract.extraction_et_afficher_tag(audio_path)
                # Affiche les métadonnées dans le label prévu à cet effet
                self.metaData_label.config(text=self.metadata_str)
                
                # Affiche l'image de couverture de l'album associée à l'audio
                self.cover_image(audio_path)
                
                # Stocke le chemin du fichier audio pour une utilisation ultérieure
                self.chemin_audio = audio_path
                
                # Si un audio est déjà en lecture, relance la lecture du fichier sélectionné
                if self.audio_lecture:
                    self.lire_audio()  # Lance ou continue la lecture du fichier audio

    def cover_image(self, audio_path: str) -> None:
        """
        Fonction qui affiche la couverture de l'album pour le fichier audio sélectionné.

        Paramètre :
        - audio_path: str : Chemin absolu du fichier audio dont on veut afficher la couverture.

        Retourne :
        - None : Aucune valeur de retour.
        """
        audio = None  # Initialisation de la variable audio pour stocker l'objet audio en fonction du format

        # Charger l'audio en fonction de son format
        try:
            if audio_path.endswith('.mp3'):
                # Si le fichier est un MP3, on charge les métadonnées avec la bibliothèque MP3
                audio = MP3(audio_path)  # Charge un fichier MP3
            elif audio_path.endswith('.flac'):
                # Si le fichier est un FLAC, on charge les métadonnées avec la bibliothèque FLAC
                audio = FLAC(audio_path)  # Charge un fichier FLAC
            else:
                # Si le format n'est ni MP3 ni FLAC, on affiche un message d'erreur
                self.metaData_label.config(text="Format non supporté")  # Format non supporté
                return
            
            # Initialisation de la variable de couverture d'album
            cover_image = None
            
            # Recherche de la couverture de l'album dans les tags de l'audio
            # Pour MP3, on cherche le tag 'APIC' qui contient les informations de couverture
            if isinstance(audio, MP3):
                cover_image = next((tag.data for tag in audio.tags.values() if isinstance(tag, APIC)), None)
            # Pour FLAC, on cherche les images dans les métadonnées sous 'pictures'
            elif isinstance(audio, FLAC):
                cover_image = next((picture.data for picture in audio.pictures if isinstance(picture, Picture)), None)
            
            image_album = None  # Initialisation de la variable pour l'image de couverture

            if cover_image:
                # Si une couverture a été trouvée, on la charge et la redimensionne
                image = Image.open(io.BytesIO(cover_image))  # Ouvre l'image à partir des données binaires
                image = image.resize((214, 214))  # Redimensionne l'image à la taille du label
                image_alb = ImageTk.PhotoImage(image)  # Convertir l'image en format compatible avec Tkinter
                
                image_album = image_alb  # Stocke l'image de couverture
            else:
                # Si aucune couverture n'est trouvée, on charge une image par défaut
                image_path = self.image_path  # Le chemin de l'image par défaut
                try:
                    image = Image.open(image_path)  # Ouvre l'image par défaut
                    image = image.resize((214, 214))  # Redimensionne l'image à la taille du label
                    photo = ImageTk.PhotoImage(image)  # Convertit l'image pour Tkinter

                    image_album = photo  # Stocke l'image par défaut
                except Exception as e:
                    # En cas d'erreur lors du chargement de l'image par défaut
                    print("Erreur lors du chargement de l'image par défaut :", e)
                    self.A_label_cover.config(text="Erreur de chargement de l'image.")  # Affiche un message d'erreur dans le label

            # Mettre à jour le label avec l'image de couverture (soit celle trouvée, soit l'image par défaut)
            self.A_label_cover.config(image=image_album)  # Affecte l'image au label de couverture
            self.A_label_cover.image = image_album  # Conserve une référence à l'image pour éviter qu'elle ne soit collectée par le garbage collector
            self.A_label_cover.config(text="")  # Efface tout texte du label pour n'afficher que l'image
        except Exception as e:
            # En cas d'erreur lors du traitement de l'audio (problème de lecture, de format, etc.)
            print("Erreur lors du traitement de l'audio :", e)
            self.metaData_label.config(text="Erreur lors du traitement de l'audio.")  # Affiche un message d'erreur dans le label des métadonnées

    def switch_to_panel2(self) -> None:
        """
            Fonction qui cache le panneau 1 et affiche le panneau 2.

            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        self.panel1.pack_forget()  # Cache le panel1
        self.panel2.pack(fill="both", expand=True)  # Affiche le panel2

    def lire_audio(self) -> None:   
        """
            Fonction qui lance la lecture du fichier audio sélectionné.

            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        select_index = self.audio_listbox.curselection()
        if self.Varbutt == True:
            self.varstr = str(self.buttnext)     
        elif self.Varbutt == False:
            self.varstr = str(select_index[0])
        
        audio_path = self.mon_dictionnaire[self.varstr]
        chemin_nom_fichier = os.path.basename(audio_path)
        nom_fichier = self.verifier_et_couper_nom_Milieu(chemin_nom_fichier)
        self.B1_label_fichier_nom.config(text=nom_fichier)
        self.ecoute.lire_fichier_audio(audio_path)  # Joue le fichier audio
        self.is_paused = False
        self.butt_pause_reprendre.config(text="⏸")  # Met à jour le texte du bouton pour pause
        self.audio_lecture = True
        self.final_lecture = True

        # Liaison de la barre d'espace pour la pause/reprise
        self.master.bind("<Return>", self.toggle_pause)  # Appuyer sur la barre d'espace pour mettre en pause/reprendre

        # Liaison des touches de direction pour les actions Précédent et Suivant
        self.master.bind("<Left>", self.prev_audio)  # Flèche gauche pour le morceau précédent
        self.master.bind("<Right>", self.next_audio)  # Flèche droite pour le morceau suivant

        # Vérifier périodiquement si la musique est terminée et passer à la suivante
        self.master.after(100, self.check_audio_finish)

    def check_audio_finish(self) -> None:   
        """
            Fonction qui lance la lecture du fichier audio suivant

            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        if self.audio_lecture and not pygame.mixer.music.get_busy():
            self.next_audio(event=None)  # Lire la prochaine chanson
        else:
            self.master.after(100, self.check_audio_finish)  # Vérifier à nouveau dans 100ms
        
    def toggle_pause(self, event=None) -> None:
        """
            Fonction qui met en pause ou reprend la lecture de l'audio.
            
            Paramètre :
            - event

            Retourne :
            - None : Aucune valeur de retour.
        """
        self.verif_lecture = True
        if self.is_paused:
            self.reprendre()  # Reprend la lecture
            self.butt_pause_reprendre.config(text="⏸")  # Met à jour le texte du bouton
            self.is_paused = False
        else:
            self.pause()  # Met en pause la lecture
            self.butt_pause_reprendre.config(text="■")  # Met à jour le texte du bouton
            self.is_paused = True

    def annuler(self) -> None:
        """
            Fonction qui ferme la fenêtre secondaire pour la création d'une playlist.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        # Ferme la fenêtre secondaire
        self.new_window.destroy()  
        self._open_window  = False
        # self.playlist_window = False

    def par_defaut(self) -> None:
        """
            Fonction pour créer une playlist par défaut parmi la liste dans la listbox.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        
        self.select_all()
        self.entry.delete(0, tk.END)  # Efface le contenu de l'Entry
        chemin_play = ""
        if self.is_playlist == False:
            self.entry.insert(0, self.valeur_par_defaut)  # Insère la valeur par défaut
            chemin_play = self.playlist.gui_ecritureFichierxspf(self.varDirectory, None)  # Enregistre la playlist
        else:
            self.entry.insert(0, self.playlist_defaut)
            self.entry.config(state="readonly") 
            chemin_play = self.playlist.gui_ecritureFichierxspf(self.varDirectory, self.playlist_defaut)  # Enregistre la playlist  
        self.afficher_notification(f"Votre playlist est crée dans ce dossier : \n\n Chemin : {os.path.abspath(chemin_play)}")
        self._open_window  = False
        self.new_window.destroy()  # Ferme la fenêtre secondaire
        # self.playlist_window = False

    def specifier(self) -> None:
        """
            Fonction pour créer une playlist en spécifiant le nom de la playlist et son nom.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        texte_saisi = self.entry.get()  # Récupère le texte saisi dans l'Entry
         # self._specifier = True
        chemin_audio = os.path.abspath(fr"Python_project/Playlist/{texte_saisi}.xspf")
        self.verification_playlist(chemin_audio)

        if self.modification_fichier_play == True :
            self.suite_specifier()

    def suite_specifier(self) -> None:
        """
            Fonction suite pour la création d'une playlist spécifiée.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        texte_saisi = self.entry.get()
        
        # Récupérer les chemins des options sélectionnées
        chemins_selectionnes = [path for var, path in zip(self.checkbox_vars, self.chemins_options) if var.get()]

        # Écrire les chemins sélectionnés dans un fichier
        with open(self.file_path_chemins, 'w', encoding="utf-8") as f:
            for chemin in chemins_selectionnes:
                f.write(f"{chemin}\n")  # Écrire chaque chemin dans le fichier, suivi d'une nouvelle ligne

        # Afficher la notification avec le chemin enregistré
        chemin_play = self.playlist.gui_ecritureFichierxspf(self.file_path_chemins, texte_saisi)  # Enregistre la playlist avec le texte saisi
        self.exist_play = False
        self.afficher_notification(f"Votre playlist est crée dans ce dossier : \n\n Chemin : {os.path.abspath(chemin_play)}")

        # Efface le contenu de l'Entry après avoir spécifié
        self.entry.delete(0, tk.END)  
        self._open_window  = False
        self.new_window.destroy()  # Ferme la fenêtre secondaire
         # self._specifier = False

    def open_new_fenetre(self) -> None:
        """
            Fonction qui ouvre une nouvelle fenêtre pour gérer la playlist.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        # Création d'une nouvelle fenêtre
        self.new_window = tk.Toplevel(root)
        self.new_window.title("Fenêtre Playlist")
        self.new_window.geometry("510x420")  # Taille de la fenêtre
        self.new_window.resizable(True, False)  # Empêche la redimension de la fenêtre
        self._open_window  = True
        # Créer les cadres
        frame1_open_window = tk.Frame(self.new_window, bg=self.antiquewhite)
        frame2_open_window = tk.Frame(self.new_window, bg="gray")
        frame3_open_window = tk.Frame(self.new_window)  # Cadre général pour le canvas et la scrollbar

        frame1_open_window.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        frame3_open_window.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        frame2_open_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.label_name = tk.Label(frame1_open_window, text="Nom Playlist :", bg=self.antiquewhite)
        self.label_name.pack(side=tk.LEFT, padx=10, pady=10)

        # Zone de saisie (entrée de texte) avec valeur par défaut
        self.entry = tk.Entry(frame1_open_window, width=30)
        if self.is_playlist == False:
            self.entry.insert(0, self.valeur_par_defaut)  # Insère la valeur par défaut
        else:
            # Définir l'Entry en mode readonly pour empêcher la modification
            self.entry.insert(0, self.playlist_defaut) 
        self.entry.pack(side=tk.LEFT, padx=10, pady=10)

        # Bouton pour désélectionner toutes les checkboxes
        self.deselect_all_btn = tk.Button(frame1_open_window, text="T-déselect", command=self.deselect_all)
        self.deselect_all_btn.pack(side=tk.RIGHT, padx=10, pady=10)

        # Bouton pour sélectionner toutes les checkboxes
        self.select_all_btn = tk.Button(frame1_open_window, text="T-select", command=self.select_all)
        self.select_all_btn.pack(side=tk.RIGHT, padx=10, pady=10)

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
        
        self.options_fichier_lire(self.fichier_lire)

        # Création des boutons dans la nouvelle fenêtre
        button_annuler = tk.Button(frame2_open_window, text="Annuler", command=self.annuler)
        button_annuler.pack(side=tk.LEFT, padx=10, pady=10)

        button_par_defaut = tk.Button(frame2_open_window, text="Par défaut", command=self.par_defaut)
        button_par_defaut.pack(side=tk.LEFT, padx=10, pady=10)

        button_specifier = tk.Button(frame2_open_window, text="Spécifier", command=self.specifier)
        button_specifier.pack(side=tk.LEFT, padx=10, pady=10)

    def options_fichier_lire(self, filename: str) -> None:
        """
            Fonction qui charge des options à partir d'un fichier et crée des cases à cocher.
            
            Paramètre :
            - filename: str : Chemin du fichier  lire.

            Retourne :
            - None : Aucune valeur de retour.
        """
        try:
            with open(filename, 'r', encoding="utf-8") as file:
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

    def select_all(self) -> None:
        """
            Fonction pour cocher toutes les checkboxes.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        for var in self.checkbox_vars:
            var.set(True)

    def deselect_all(self) -> None:
        """
            Fonction pour décocher toutes les checkboxes
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        for var in self.checkbox_vars:
            var.set(False)

    def next_audio(self, event=None) -> None:
        """
            Fonction pour passer à l'audio suivant dans la liste et met à jour l'affichage.
            
            Paramètre :
            - event

            Retourne :
            - None : Aucune valeur de retour.
        """
        try:
            if self.tailleListbox > self.buttnext:  # Vérifie s'il y a un élément suivant
                self.next_item()  # Sélectionne l'élément suivant
                self.buttnext += 1  # Incrémente l'index
                self.varstr = str(self.buttnext)      

                audio_path = self.mon_dictionnaire[self.varstr]  # Récupère le chemin de l'audio suivant
                # Récupère seulement le nom du fichier à partir du chemin
                chemin_nom_fichier = os.path.basename(audio_path)
                nom_fichier =self.verifier_et_couper_nom_Milieu(chemin_nom_fichier)
                self.B1_label_fichier_nom.config(text=nom_fichier)
                
                # Extraire et afficher les métadonnées de l'audio
                self.metadata_str = self.extract.extraction_et_afficher_tag(audio_path)
                self.metaData_label.config(text=self.metadata_str)  # Afficher les métadonnées dans path_label3
                
                self.cover_image(audio_path)  # Affiche l'image de couverture
                self.chemin_audio = audio_path
                self.Varbutt = True
                if self.audio_lecture:  # Si un audio est déjà en lecture
                    self.lire_audio()  # Lit le fichier audio
        except IndexError:
            print("Erreur : Aucun audio suivant dans la liste.")
        except Exception as e:
            print("Erreur lors de la lecture de l'audio suivant :", e)

    def next_item(self) -> None:
        """
            Fonction pour Sélectionne l'élément suivant dans la Listbox.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        if self.tailleListbox > self.buttnext:
            current_index = self.buttnext
            # Calcule l'index du prochain élément
            next_index = self.buttnext + 1
            self.audio_listbox.selection_clear(current_index)  # Désélectionne l'élément actuel
            self.audio_listbox.selection_set(next_index)  # Sélectionne le prochain élément
            self.audio_listbox.activate(next_index)  # Met le prochain élément en surbrillance

    def prev_audio(self, event=None) -> None:  
        """
            Fonction pour passer à l'audio précédent dans la liste et met à jour l'affichage.
            
            Paramètre :
            - event

            Retourne :
            - None : Aucune valeur de retour.
        """
        if 0 < self.buttnext:  # Vérifie s'il y a un élément précédent
            self.prev_item()  # Sélectionne l'élément précédent
            self.buttnext -= 1  # Décrémente l'index
            self.varstr = str(self.buttnext)      

            audio_path = self.mon_dictionnaire[self.varstr]  # Récupère le chemin de l'audio précédent
            # Récupère seulement le nom du fichier à partir du chemin
            chemin_nom_fichier = os.path.basename(audio_path)
            nom_fichier =self.verifier_et_couper_nom_Milieu(chemin_nom_fichier)
            self.B1_label_fichier_nom.config(text=nom_fichier)
            
            # Extraire et afficher les métadonnées de l'audio
            self.metadata_str = self.extract.extraction_et_afficher_tag(audio_path)
            self.metaData_label.config(text=self.metadata_str)  # Afficher les métadonnées dans path_label3
            
            self.cover_image(audio_path)  # Affiche l'image de couverture
            self.chemin_audio = audio_path
            self.Varbutt = True
            if self.audio_lecture:  # Si un audio est déjà en lecture
                self.lire_audio()  # Lit le fichier audio

    def prev_item(self) -> None:
        """
            Fonction pour Sélectionne l'élément précédent dans la Listbox.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        if 0 < self.buttnext:
            current_index = self.buttnext
            # Calcule l'index du précédent élément
            prev_index = self.buttnext - 1
            self.audio_listbox.selection_clear(current_index)  # Désélectionne l'élément actuel
            self.audio_listbox.selection_set(prev_index)  # Sélectionne le précédent élément
            self.audio_listbox.activate(prev_index)  # Met le précédent élément en surbrillance

    def pause(self) -> None:
        """
            Fonction pour mettre en pause la lecture audio.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        if self.final_lecture == True and self.audio_lecture == True:
            self.audio_lecture = False  # Met à jour l'état audio
            self.final_lecture = True
            pygame.mixer.music.pause()  # Met en pause la musique

    def reprendre(self) -> None:
        """
            Fonction pour reprend la lecture audio en pause.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        if self.final_lecture == True and self.audio_lecture == False:
            self.audio_lecture = True  # Met à jour l'état audio
            self.final_lecture = True
            pygame.mixer.music.unpause()  # Reprend la musique

    def rechercher(self) -> None:
        """
            Fonction pour chercher des infos sur un album, un artiste et un titre.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        # Récupérer la saisie de l'utilisateur, la nettoyer et la mettre en minuscules
        if self.fetcher.check_internet_and_authorize() == True :
            saisie = self.entry_ecriture_haut.get().strip().lower()

            if saisie == "" :
                message = "La saisie de l'utilisateur est vide"
                self.afficher_notification(message)
                return ""
            if saisie == "album:" or saisie == "artiste:" or saisie == "music:" :
                message = "La saisie de l'utilisateur est non complète"
                self.afficher_notification(message)
                return ""
            if not (saisie.startswith("album:") or saisie.startswith("artiste:") or saisie.startswith("music:")):
                message = "La saisie de l'utilisateur incorrect \n Ecrivez: \"album:nom_album\" ou \"artiste:nom_artiste\" ou \"music:titre_music\""
                self.afficher_notification(message)
                return ""
            
            # Si le label existe déjà, on le cache au lieu de le recréer
            if hasattr(self, 'rechercher_label'):
                self.rechercher_label.pack_forget()  # Cache le label précédent
                self.scrollbar.pack_forget()  # Cache la scrollbar précédente
                self.rechercher_frame.pack_forget()  # Cache le cadre précédent


            # Cache le label des métadonnées
            self.metaData_label.pack_forget()
            self.reche = False

            # Créer un cadre pour le label et la scrollbar
            self.rechercher_frame = tk.Frame(self.section3_metaData, width=270, height=10, bg=self.lightyellow)
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
            data_api_affiche = self.fetcher_methode(saisie)
            self.rechercher_label.config(text=data_api_affiche)  # Mettre à jour le texte du label formaté
            
            self.reche_retour = True
        else: 
            message = "Aucune connexion Internet. L'accès à l'API Spotify est limité"
            self.afficher_notification(message)
     
    def retour(self) -> None: 
        """
            Fonction pour affiche les métadonnées du fichier audio sélectionné et cache le bouton de retour.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        if self.reche == False and self.reche_retour == True :
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
            self.reche_retour = False

    def destroy_notification(self) -> None: 
        """
            Fonction pour fermer la fenêtre secondaire de notification.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        self.notification.destroy()  

    def clo_notification(self) -> None:
        """
            Fonction pour fermer la fenêtre secondaire de notification.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        self.modification_fichier_play = False
        self.notification.destroy()  

    def Modifier_play_name(self) -> None:
        """
            Fonction pour modifier le nom d'une playlist.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        self.modification_fichier_play = True
        self.notification.destroy()  
        self.suite_specifier()

    def afficher_notification(self, chemin_play:str) -> None:
        """
            Fonction qui créer une fenetre pour afficher une notification.
            
            Paramètre :
            - chemin_play:str : Chemin de la playlist.

            Retourne :
            - None : Aucune valeur de retour.
        """
        global notification, label, entry
        self.notification = Toplevel(root)
        self.notification.title("Notification")  # Titre de la fenêtre
        self.notification.geometry("700x180")  # Définir la taille de la fenêtre
        self.notification.resizable(False, False)  # Empêcher le redimensionnement

         # Créer un label pour afficher le message
        message_label = tk.Label(self.notification, text=f"Message : {chemin_play}", padx=20, pady=20)
        message_label.pack()
        if self.exist_play == True:
            # Si `self.exist_play` est True, ajouter les boutons pour annuler et modifier
            cancel_button = tk.Button(self.notification, text="Annuler", command=self.clo_notification)
            cancel_button.pack(side=tk.LEFT, padx=10, pady=10)

            modify_button = tk.Button(self.notification, text="Modifier", command=self.Modifier_play_name)
            modify_button.pack(side=tk.RIGHT, padx=10, pady=10)
        else:
            # Si `self.exist_play` est False, seulement un bouton pour fermer
            close_button = tk.Button(self.notification, text="OK", command=self.destroy_notification)
            close_button.pack(pady=(0, 10))  # Ajouter un peu d'espace en bas

    def fetcher_methode(self, saisie:str)-> str:
        """
            Fonction pour traiter la saisie et effectuer des recherches basées sur artiste, album ou musique via un API.
            
            Paramètre :
            - saisie:str : la saisie de l'utilisateur pour utiliser l'API.

            Retourne :
            - str : renvoie soit les albums ou les artistes ou les musiques
        """
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

    def modification_data(self) -> None:
        """
            Fonction qui créer une fenetre pour modifier les méta données d'un fichier audio.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        # if self.affiche_window == False:
        global modif_window
        modif_window = Toplevel(root)
        modif_window.title("Modification")
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
        print("list_metadata_str", list_metadata_str)

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

    def select_cover_image(self) -> None:
        """
            Fonction qui ouvre une boîte de dialogue pour sélectionner une image de couverture.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        file_path = filedialog.askopenfilename(title="Sélectionner une couverture", filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.cover_image_path = file_path
 
    def but_cancel(self) -> None:
        """
            Fonction pour fermer la fenêtre secondaire.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        modif_window.destroy()  # Ferme la fenêtre secondaire
        # self.affiche_window = False

    def convertir_metadata_en_dict(self,metadata_str: str) -> dict: 
        """
            Fonction pour convertir une chaîne de métadonnées en un dictionnaire.

            Paramètre :
            - metadata_str: str : une dictionnaire de donnée en chaîne de caractère.

            Retourne :
            - dict : une dictionnaire de données.
        """
        metadata_dict = {}
        
        # Sépare la chaîne en lignes
        lignes = metadata_str.strip().split("\n")
        
        for ligne in lignes:
            if ':' in ligne:  # Vérifie si la ligne contient un deux-points
                cle, valeur = ligne.split(':', 1)  # Sépare la clé et la valeur
                metadata_dict[cle.strip()] = valeur.strip()  # Ajoute à la dict en supprimant les espaces

        return metadata_dict

    def save_modification(self) -> None: 
        """
            Fonction pour enregistre les modifications des métadonnées et actualise l'affichage.

            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        self.remettre_music = False
        if self.final_lecture == True :
            pygame.mixer.music.stop
            pygame.mixer.music.unload()
            if self.audio_lecture == True:
                self.remettre_music = True
        else:
            pygame.mixer.music.stop
            self.remettre_music = False
        # Récupérer le chemin audio de l'attribut de la classe
        chemin_audio = self.chemin_audio

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
        if self.remettre_music == True:
            self.ecoute.lire_fichier_audio(chemin_audio)
            self.final_lecture = True

    def ecouter_playlist(self) -> None:
        """
            Fonction qui ouvre une fenêtre secondaire pour écouter une playlist.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        self.playlist_window = tk.Toplevel(self.master)
        self.playlist_window.title("Playlist")
        self.playlist_window.geometry("510x448")
        self.playlist_window.resizable(False, False)

        # Créer les cadres
        frame1_playlist_window = tk.Frame(self.playlist_window, bg=self.antiquewhite)
        frame2_playlist_window = tk.Frame(self.playlist_window, bg="gray")
        frame3_playlist_window = tk.Frame(self.playlist_window)

        frame1_playlist_window.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        frame3_playlist_window.pack(fill=tk.BOTH, expand=False, padx=10, pady=10)
        frame2_playlist_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.label_name = tk.Label(frame1_playlist_window, text="Toutes vos Playlists", bg=self.antiquewhite)
        self.label_name.pack(side=tk.LEFT, padx=10, pady=10)



        # Créer un canvas pour la liste des playlists avec scrollbar
        self.canvas = tk.Canvas(frame3_playlist_window, bg="white")
        self.scrollbar = tk.Scrollbar(frame3_playlist_window, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        # Configuration du canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Liste des playlists
        self.tab_play.clear() 
        self.tab_play = self.explo.explorer_Playlist()
        liste_play_str = list(self.tab_play)
        self.selected_playlist = tk.IntVar()

        for i, line in enumerate(liste_play_str):
            radio_button = tk.Radiobutton(
                self.scrollable_frame,
                text=self.align_date_in_string(line),
                variable=self.selected_playlist,
                value=i,
                bg="white"
            )
            radio_button.pack(anchor=tk.W)
            
        nombre_play = len(liste_play_str)

        self.label_number_entry = tk.Entry(frame1_playlist_window, width=5)
        self.label_number_entry.pack(side=tk.RIGHT, padx=8, pady=8)

        self.label_number_entry.insert(0,nombre_play) 
        self.label_number_entry.config(state="readonly") 

        self.label_Liste_play= tk.Label(frame1_playlist_window, text="Listes :", bg=self.antiquewhite)
        self.label_Liste_play.pack(side=tk.RIGHT, padx=10, pady=10)

        # Boutons dans la nouvelle fenêtre
        button_annuler = tk.Button(frame2_playlist_window, text="Annuler", command=self.annuleroPeration)
        button_annuler.pack(side=tk.LEFT, padx=10, pady=10)

        button_choisir = tk.Button(
            frame2_playlist_window, 
            text="Choisir", 
            command=lambda: self.playlistChoisir(self.tab_play [self.selected_playlist.get()])
        )
        button_choisir.pack(side=tk.RIGHT, padx=10, pady=10)

    def annuleroPeration(self) -> None:
        """
            Fonction pour fermer la fenêtre secondaire pour écouter une playlist.
            
            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - None : Aucune valeur de retour.
        """
        self.playlist_window.destroy()

    def playlistChoisir(self, chemin_complet: str) -> None: 
        """
            Fonction pour choisir la playlist qu'on souhaite écouter.

            Paramètre :
            - chemin_complet: str: 

            Retourne :
            - None : Aucune valeur de retour.
        """
        chansons = self.explo.extraire_pistes_de_playlist(chemin_complet) 
        self.audio_listbox.delete(0, tk.END)
        self.mon_dictionnaire.clear()
        
        for i, chan in enumerate(chansons):
            cheminAudio = chan.strip().replace("\\", "/")
            nom_cheminVar = os.path.basename(cheminAudio)
            self.mon_dictionnaire[str(i)] = str(cheminAudio)
            nom_fichier =self.verifier_et_couper_nom_fichier(nom_cheminVar)
            self.audio_listbox.insert(tk.END, nom_fichier)
            self.tailleListbox = self.audio_listbox.size()
        self.annuleroPeration()
        self.audio_listbox.selection_set(0)  # Sélectionne le premier élément
        self.buttnext = 0  
        self.vider_fichier(self.fichier_lire)
        self.playlistModif(chansons)
        # Extraire le nom du fichier à partir du chemin complet
        nom_fichier = os.path.basename(chemin_complet)

        # Trouver la position du dernier ".xspf"
        position = nom_fichier.rfind('.xspf')

        # Extraire le nom de fichier sans l'extension ".xspf"
        resultat = nom_fichier[:position]

        # Affecter à playlist_defaut le nom sans extension
        self.playlist_defaut = resultat
        self.is_playlist = True

    def playlistModif(self, chansons: str) -> None: 
        """
            Fonction qui  modifie les chansons dans la playlist.

            Paramètre :
            - chansons: str: 

            Retourne :
            - None : Aucune valeur de retour.
        """
        # Ouvrir un fichier en mode écriture
        with open(self.fichier_lire, "w", encoding="utf-8") as fichier:
            for chan in chansons:
                # Écrire chaque chanson dans le fichier
                fichier.write(f"{chan}\n")
            
    def vider_fichier(self,nom_fichier: str ) -> None: 
        """
            Fonction qui vide un fichier donné.

            Paramètre :
            - nom_fichier: str: Nom de fichier a vider.

            Retourne :
            - None : Aucune valeur de retour.
        """
        # Ouvrir le fichier en mode écriture, ce qui écrase tout son contenu
        with open(nom_fichier, "w", encoding="utf-8") as fichier:
            pass  # Ne rien écrire dans le fichier
    
    def verification_playlist(self, f_name: str) -> None:
        """
        Fonction qui vérifie la mise à jour d'une playlist.

        Paramètre :
        - f_name : str : Nom de la playlist xspf.

        Retourne :
        - None : Aucune valeur de retour.
        """
        # Vérifie si la playlist f_name existe déjà dans la liste des playlists
        if f_name in self.tab_play:
            # Si la playlist existe, on marque qu'elle existe déjà
            self.exist_play = True
            # Aucune modification n'est en cours pour cette playlist
            self.modification_fichier_play = False
            # Message à afficher pour informer l'utilisateur de la modification possible de la playlist
            message = f"Voulez vous modifié la liste des audios dans cette playlist : {os.path.basename(f_name)}  \n\n Chemin : {f_name} ?"
            # Affiche la notification avec le message préparé
            self.afficher_notification(message)

    def verifier_et_couper_nom_fichier(self, nom_fichier: str) -> str:
        """
        Fonction qui coupe l'affichage du nom de l'audio dans la listbox si le nom est trop long.

        Paramètre :
        - nom_fichier : str : Nom du fichier à couper.

        Retourne :
        - str : Renvoie le nom du fichier coupé lors de l'affichage dans la listbox.
        """
        max_length = self.max_length  # Récupère la longueur maximale pour l'affichage
        # Vérifie si la longueur du nom du fichier dépasse la limite maximale
        if len(nom_fichier) > max_length:
            # Si le nom est trop long, on le coupe à la longueur maximale et ajoute des points de suspension
            nom_fichier = nom_fichier[:max_length] + "..."

        # Retourne le nom du fichier coupé
        return nom_fichier

    def verifier_et_couper_nom_Milieu(self, nom_fichier: str) -> str:
        """
        Fonction qui coupe l'affichage du nom de l'audio une fois sélectionné.

        Paramètre :
        - nom_fichier : str : Nom du fichier à couper.

        Retourne :
        - str : Renvoie le nom du fichier coupé sous la couverture.
        """
        max_length = self.max_length_milieu  # Récupère la longueur maximale pour le nom au milieu de l'interface
        # Vérifie si la longueur du nom du fichier dépasse la limite
        if len(nom_fichier) > max_length:
            # Si le nom est trop long, on le coupe à la longueur maximale et ajoute des points de suspension
            nom_fichier = nom_fichier[:max_length] + "..."

        # Retourne le nom du fichier coupé
        return nom_fichier

    def get_date_from_xml(self, xspf_string: str) -> str:
        """
        Fonction qui donne la date de création d'une playlist.

        Paramètre :
        - xspf_string : str : Le contenu XML sous forme de chaîne ou le chemin vers le fichier xspf.

        Retourne :
        - str : La date de création de la playlist ou un message d'erreur si la balise <date> est introuvable.
        """
        try:
            # Si le paramètre est une chaîne XML, l'utiliser directement
            if xspf_string.startswith('<?xml'):
                xml_string = xspf_string
            else:
                # Sinon, c'est un chemin vers un fichier, donc on lit le contenu du fichier XML
                with open(xspf_string, 'r', encoding='utf-8') as file:
                    xml_string = file.read()

            # Analyse le contenu XML
            root = ET.fromstring(xml_string)

            # Définit l'espace de noms XML utilisé pour les balises xspf
            namespace = {'xspf': 'http://xspf.org/ns/0/'}

            # Recherche de la balise <date> dans le fichier XML
            date_element = root.find('.//xspf:date', namespace)

            # Si la balise <date> est trouvée, renvoie la date
            if date_element is not None:
                return date_element.text
            else:
                return "Date non trouvée dans le fichier XML"

        except ET.ParseError:
            # Si une erreur se produit lors du parsing XML, renvoie un message d'erreur
            return "Erreur de parsing XML. Vérifiez le format du fichier."
        except FileNotFoundError:
            # Si le fichier XML n'est pas trouvé, renvoie un message d'erreur
            return "Fichier non trouvé. Vérifiez le chemin du fichier."
        except Exception as e:
            # Si une autre erreur se produit, renvoie l'exception sous forme de message
            return f"Une erreur est survenue : {e}"

    def align_date_in_string(self, line: str) -> str:
        """
        Fonction qui gère l'alignement du nom du fichier et la date de création.

        Paramètre :
        - line : str : le chemin du fichier xspf

        Retourne :
        - str : Le nom du fichier et la date de création, alignés pour l'affichage.
        """
        # Obtient le nom du fichier à partir du chemin complet
        file_name = os.path.basename(line)
        # Appelle la fonction pour obtenir la date de création de la playlist
        date = self.get_date_from_xml(line)

        # Retourne une chaîne formatée contenant le nom du fichier et la date, alignée
        return f"{file_name}         {date}"

# Création de la fenêtre principale
if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)  # Création de l'instance de l'application
    root.mainloop()  # Lancer la boucle principale