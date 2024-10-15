import os
import io
import tkinter as tk
import pygame  # Bibliothèque pour gérer les fonctionnalités multimédias comme jouer des fichiers audio.
from tkinter import *
from tkinter import filedialog, Listbox, Scrollbar, Label, PhotoImage
from PIL import Image, ImageTk  # Pour gérer les images avec Pillow
from ecouterAudio import Ecouter # Importe la classe Ecouter du module ecouterAudio pour lire un fichier audio mp3 ou flac dans la console
from explorationDossier import Explorer  # Importe la classe Explorer pour explorer les dossiers
from constitutionPlaylist import Playlist  # Importe la classe Playlist du module constitutionPlaylist pour générer des playlists
from audioTagExtraction import Extraction  # Importe la classe Extraction du module audioTagExtraction pour extraire les métadonnées audio
from mutagen.easyid3 import EasyID3  # Pour lire et écrire les métadonnées ID3 dans les fichiers MP3.
from mutagen.mp3 import MP3  # Pour gérer les fichiers audio MP3 et accéder à leurs métadonnées.
from mutagen.id3 import ID3, APIC  # Pour manipuler les balises ID3 et gérer les images intégrées comme les couvertures d'album.
from mutagen.flac import FLAC, Picture  # Pour travailler avec les fichiers audio FLAC et gérer les images intégrées.
from PIL import Image  # Pour ouvrir, modifier et enregistrer des images dans divers formats.



class AudioPlayerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Lecteur Audio")
        self.master.state("zoomed")
        # Création d'un dictionnaire vide
        self.mon_dictionnaire = {}
        # Crée une instance de la classe Explorer pour explorer le dossier
        self.explo = Explorer()  
        self.ecoute = Ecouter() 
        self.playlist = Playlist() 
        self.extract = Extraction()
        self.varDirectory = ""
        # La valeur par défaut pour l'Entry
        self.valeur_par_defaut = "maPlaylist"

        # Panel 1 - avec une image, un fond bleu ciel et un bouton
        self.panel1 = tk.Frame(self.master, bg="#87CEEB")
        self.panel1.pack(fill="both", expand=True)

        # Chargement et ajout de l'image dans le panel1
        chem_image = os.path.abspath(r"Python_project/img/nn.webp")
        self.image = Image.open(chem_image)  # Remplace par le chemin de ton image
        self.image = self.image.resize((200, 200))  # Redimensionner si nécessaire
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.label_image = tk.Label(self.panel1, image=self.image_tk, bg="#87CEEB")
        self.label_image.pack(pady=20)

        # Ajouter un bouton pour passer à panel2
        self.bouton_switch = tk.Button(self.panel1, text="Aller Go", command=self.direct_Goto)
        self.bouton_switch.pack(pady=10)

        # Panel 2 
        self.panel2 = tk.Frame(self.master, bg="lightyellow")

        # Créer trois cadres avec des tailles différentes
        self.frame1 = tk.Frame(self.panel2, bg="dodgerblue")
        self.frame2 = tk.Frame(self.panel2, bg="gray")
        self.frame3 = tk.Frame(self.panel2, bg="dodgerblue")

        # Pack les cadres avec des tailles différentes
        self.frame1.pack(fill=tk.X, padx=5, pady=5)  # Cadre 1 : petit, remplit la largeur
        self.frame2.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)  # Cadre 2 : très grand, remplit l'espace
        self.frame3.pack(fill=tk.X, padx=5, pady=5)  # Cadre 3 : intermédiaire, remplit la largeur

        # Cadre 1******************************************
        self.entry1 = tk.Entry(self.frame1, width=150)
        self.entry1.pack(side=tk.LEFT, padx=5, pady=5)
        self.button2 = tk.Button(self.frame1, text="Check",) 
        self.button2.pack(side=tk.RIGHT, padx=10, pady=10)  # Aligné à droite

        # Cadre 2******************************************
        # Configurer le grid pour 3 colonnes de taille égale
        self.frame2.grid_columnconfigure(0, weight=1)
        self.frame2.grid_columnconfigure(1, weight=1)
        self.frame2.grid_columnconfigure(2, weight=1)
        self.frame2.grid_rowconfigure(0, weight=1)  # Une seule ligne

        # Créer trois sous-sections dans frame2 (gauche, centre, droite) avec les mêmes dimensions
        self.section1 = tk.Frame(self.frame2, bg='white')
        self.section1.grid(row=0, column=0, sticky='nse', padx=5, pady=5)

        self.section2 = tk.Frame(self.frame2, bg='white')
        self.section2.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        self.section3 = tk.Frame(self.frame2, bg='white')
        self.section3.grid(row=0, column=2, sticky='nsw', padx=2, pady=2)

        # Créer une liste pour afficher les fichiers MP3
        self.song_listbox = Listbox(self.section1, width=80, height=10)  # Ajuster la taille ici
        self.song_listbox.pack(side=tk.LEFT, fill='both', expand=True)

        # Lier le double-clic à la lecture et l'affichage du titre
        self.song_listbox.bind("<Double-Button-1>", self.affiche_path_label)

        # Ajouter une barre de défilement
        self.scrollbar = Scrollbar(self.section1)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=0, pady=0)  # Assurer aucun espacement

        # Lier la barre de défilement à la Listbox
        self.song_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.song_listbox.yview)

        # Label pour afficher le chemin complet du fichier sélectionné
        self.path_label2 = Label(self.section2, text="", width=70, height=10, justify="left", bg='white')
        self.path_label2.pack(pady=10, fill='both', expand=True)  # Utiliser fill='both' et expand=True pour agrandir

        # Label pour afficher le chemin complet du fichier sélectionné
        self.path_lab1 = Label(self.path_label2, text="", width=80, height=17, justify="left", bg='white')
        self.path_lab1.pack(pady=10, fill='both', expand=True)  # Utiliser fill='both' et expand=True pour agrandir

        # Label pour afficher le chemin complet du fichier sélectionné, plus petit
        self.path_lab2 = Label(self.path_label2, text="", width=20, height=1, justify="left", bg='white')
        self.path_lab2.pack(pady=10, fill='both', expand=True)  # Utiliser fill='both' et expand=True pour agrandir


        # Label pour afficher le chemin complet du fichier sélectionné
        self.path_label3 = Label(self.section3, text="", width=70, height=10, justify="left", bg='white')
        self.path_label3.pack(pady=10, fill='both', expand=True)  # Utiliser fill='both' et expand=True pour agrandir

        # Cadre 3******************************************
        # Configurer le grid pour 3 colonnes de taille égale
        self.frame3.grid_columnconfigure(0, weight=1)  # Sect1
        self.frame3.grid_columnconfigure(1, weight=2)  # Sect2 (plus large)
        self.frame3.grid_columnconfigure(2, weight=1)  # Sect3

        self.frame3.grid_rowconfigure(0, weight=1)  # Une seule ligne

        self.sect1 = tk.Frame(self.frame3, bg='white')
        self.sect1.grid(row=0, column=0, sticky='nsew', padx=2, pady=2)

        self.sect2 = tk.Frame(self.frame3, bg='dodgerblue')
        self.sect2.grid(row=0, column=1, sticky='nsew',padx=2, pady=2)

        self.sect3 = tk.Frame(self.frame3, bg='dodgerblue')
        self.sect3.grid(row=0, column=2, sticky='nsew',padx=2, pady=2)

        self.button3 = tk.Button(self.sect1, text="Exploration", command=self.exploration_dossier)
        self.button3.pack(side=tk.LEFT, padx=10, pady=10)  # Aligné à gauche

        self.button4 = tk.Button(self.sect1, text="Playlist", command=self.open_new_fenetre) 
        self.button4.pack(side=tk.RIGHT, padx=10, pady=10)  # Aligné à droite

        

        self.butt_play = tk.Button(self.path_lab2, text="Lecture", command= self.lire_audio)
        self.butt_play.pack(side=tk.LEFT, padx=10, pady=10)  

        self.butt_pause = tk.Button(self.path_lab2, text="Pause", command= self.ecoute.pause)
        self.butt_pause.pack(side=tk.RIGHT, padx=10, pady=10) 

        self.butt_reprendre = tk.Button(self.path_lab2, text="Reprendre", command= self.ecoute.reprendre)
        self.butt_reprendre.pack(side=tk.RIGHT, padx=10, pady=10) 
        # Créer un bouton pour mettre en pause/reprendre la musique
        # self.pause_resume_button = tk.Button(self.path_lab2, text="Pause", state=tk.DISABLED, command=self.pause_resume_music)
        # self.pause_resume_button.pack(side=tk.LEFT, padx=10, pady=10) 

        # self.butt_reprendre = tk.Button(self.path_lab2, text="::")
        # self.butt_reprendre.pack(side=tk.LEFT, padx=10, pady=10) 


    def direct_Goto(self):
        self.switch_to_panel2()
        chem = os.path.abspath(r"Python_project\music")
        self.AZEexploration_dossier(chem) 
        audio_path = self.mon_dictionnaire["0"]
        # Extraire et afficher les métadonnées de l'audio
        metadata_str = self.extract.extraction_et_afficher_tag(audio_path)
        self.path_label3.config(text=metadata_str)  # Afficher les métadonnées dans path_label3
        self.cover_image(audio_path)


    def exploration_dossier(self):
        """Ouvre une boîte de dialogue pour sélectionner un dossier contenant des fichiers audio."""
        
        # Ouvre une boîte de dialogue pour sélectionner un dossier et stocke le chemin dans 'dossier'.
        dossier = filedialog.askdirectory()  
        
        # Vérifie si un dossier a été sélectionné
        if dossier:
            # Efface le contenu actuel de la Listbox pour éviter les doublons
            self.song_listbox.delete(0, tk.END)
            
            
                
            # Remplace les antislashs (\) par des barres obliques (/) pour la compatibilité
            dossier_save = dossier.replace("\\", "/") 
            self.varDirectory = dossier_save
            
            # Appelle une méthode d'Explorer pour récupérer le chemin du fichier contenant les chemins audio
            full_path = self.explo.explorer_dossier_interface(dossier_save) 
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
                    self.song_listbox.insert(tk.END, nom_fichier)
    

    def AZEexploration_dossier(self,path):
        """Ouvre une boîte de dialogue pour sélectionner un dossier contenant des fichiers audio."""
        dossier = None
        if path == None:
            # Ouvre une boîte de dialogue pour sélectionner un dossier et stocke le chemin dans 'dossier'.
            dossier = filedialog.askdirectory() 
        else:
            dossier = path 
        
        # Vérifie si un dossier a été sélectionné
        if dossier:
            # Efface le contenu actuel de la Listbox pour éviter les doublons
            self.song_listbox.delete(0, tk.END)
            
            
                
            # Remplace les antislashs (\) par des barres obliques (/) pour la compatibilité
            dossier_save = dossier.replace("\\", "/") 
            self.varDirectory = dossier_save
            
            # Appelle une méthode d'Explorer pour récupérer le chemin du fichier contenant les chemins audio
            full_path = self.explo.explorer_dossier_interface(dossier_save) 
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
                    self.song_listbox.insert(tk.END, nom_fichier)
    

    def affiche_path_label(self, event):
        """Affiche le chemin et les métadonnées de la chanson sélectionnée dans les labels appropriés."""
        audio = None
        
        # Récupérer l'index du fichier sélectionné dans la Listbox
        select_index = self.song_listbox.curselection()        
        
        if select_index:
            # Obtenir le chemin du fichier audio sélectionné
            varstr = str(select_index[0])
            audio_path = self.mon_dictionnaire[varstr]
            
            # Extraire et afficher les métadonnées de l'audio
            metadata_str = self.extract.extraction_et_afficher_tag(audio_path)
            self.path_label3.config(text=metadata_str)  # Afficher les métadonnées dans path_label3
            
            self.cover_image(audio_path)


    def cover_image(self,audio_path):
        audio = None
        # Charger l'audio en fonction de son format
        try:
            if audio_path.endswith('.mp3'):
                audio = MP3(audio_path)
            elif audio_path.endswith('.flac'):
                audio = FLAC(audio_path)
            else:
                self.path_label3.config(text="Format non supporté")
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
                image = image.resize((214, 214)) # Redimensionner l'image à la taille du label
                image_alb = ImageTk.PhotoImage(image)  # Convertir l'image pour Tkinter
                
                image_album = image_alb  
            else:
                # Charger l'image par défaut si aucune couverture n'est trouvée
                image_path = os.path.abspath(r"Python_project\img\images.jpeg")
                print("Chemin de l'image par défaut :", image_path)
                
                try:
                    image = Image.open(image_path)
                    image = image.resize((214, 214))
                    photo = ImageTk.PhotoImage(image)

                    image_album = photo  # Garder une référence à l'image
                except Exception as e:
                    print("Erreur lors du chargement de l'image par défaut :", e)
                    self.path_lab1.config(text="Erreur de chargement de l'image.")

            # Mettre à jour le label avec l'image de couverture
            self.path_lab1.config(image=image_album)
            self.path_lab1.image = image_album  # Garder une référence à l'image
            self.path_lab1.config(text="")  # Effacer le texte pour afficher uniquement l'image
        except Exception as e:
            print("Erreur lors du traitement de l'audio :", e)
            self.path_label3.config(text="Erreur lors du traitement de l'audio.")
    
    
    def switch_to_panel2(self):
        self.panel1.pack_forget()  # Cache le panel1
        self.panel2.pack(fill="both", expand=True)  # Affiche le panel2


    def lire_audio(self):
        """Lance la lecture du fichier audio sélectionné."""
        
        # Récupérer l'index du fichier sélectionné dans la Listbox
        select_index = self.song_listbox.curselection()         
        if select_index:

            # Obtenir le chemin du fichier audio sélectionné
            varstr = str(select_index[0])
            audio_path = self.mon_dictionnaire[varstr]
            self.ecoute.lire_fichier_audio(audio_path)

    """    
    # Fonction pour mettre en pause ou reprendre la musique
    def pause_resume_music(self):
        global is_paused
        if is_paused:
            pygame.mixer.music.unpause()  # Reprendre la musique
            self.pause_resume_button.config(text="Pause")  # Changer le texte du bouton
        else:
            pygame.mixer.music.pause()  # Mettre en pause la musique
            self.pause_resume_button.config(text="Reprendre")  # Changer le texte du bouton
        is_paused = not is_paused  # Inverser l'état de la musique
    """


    # Fonction à exécuter lorsque le bouton "Annuler" est cliqué
    def annuler(self):
        new_window.destroy()  # Ferme la fenêtre secondaire


    # Fonction à exécuter lorsque le bouton "Par défaut" est cliqué
    def par_defaut(self):
        # Restaure la valeur par défaut dans l'Entry et affiche cette valeur dans le label
        entry.delete(0, tk.END)  # Efface le contenu de l'Entry
        entry.insert(0, self.valeur_par_defaut)  # Insère la valeur par défaut
        self.playlist.ecritureFichierxspf(self.varDirectory,None)

    # Fonction à exécuter lorsque le bouton "Spécifier" est cliqué
    def specifier(self):
        # Récupère le texte saisi et l'affiche dans le label
        texte_saisi = entry.get()
        self.playlist.ecritureFichierxspf(self.varDirectory,texte_saisi)
        entry.delete(0, tk.END)  # Efface le contenu de l'Entry après avoir spécifié

    # Fonction pour ouvrir une nouvelle fenêtre
    def open_new_fenetre(self):
        global new_window, label, entry
        new_window = Toplevel(root, bg="white")
        new_window.title("fenêtre Playlist")
        new_window.geometry("300x200")  # Taille de la petite fenêtre

        # Un label pour afficher des messages
        label = tk.Label(new_window, text="")
        label.pack(pady=10)

        # Zone de saisie (entrée de texte) avec valeur par défaut
        entry = tk.Entry(new_window, width=30)
        entry.insert(0, self.valeur_par_defaut)  # Insère la valeur par défaut dans l'Entry
        entry.pack(pady=10)

        # Création des boutons dans la nouvelle fenêtre
        button_annuler = tk.Button(new_window, text="Annuler", command=self.annuler)
        button_annuler.pack(side=tk.LEFT, padx=10, pady=10)

        button_par_defaut = tk.Button(new_window, text="Par défaut", command=self.par_defaut)
        button_par_defaut.pack(side=tk.LEFT, padx=10, pady=10)

        button_specifier = tk.Button(new_window, text="Spécifier", command=self.specifier)
        button_specifier.pack(side=tk.LEFT, padx=10, pady=10)


# Création de la fenêtre principale
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioPlayerApp(root)  # Création de l'instance de l'application
    root.mainloop()  # Lancer la boucle principale
