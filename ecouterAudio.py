#!/usr/bin/python3  
# -*- coding: UTF-8 -*-  

# Importation des modules nécessaires
import pygame  # Bibliothèque pour gérer les fonctionnalités multimédias comme jouer des fichiers audio.
from pydub import AudioSegment  # Pydub permet la manipulation des fichiers audio (conversion entre formats audio, etc.).
import time  # Le module time est utilisé pour introduire des pauses dans le programme.
from pydub.playback import play

"""
Classe qui gère l'écoute d'un fichier audio donné.
"""
class Ecouter:  # Déclaration de la classe 'Ecouter', qui contient des méthodes pour lire différents formats audio.

    """
    Fonction qui lit un fichier FLAC.
    
    Paramètre :
    - chemin_fichier : chemin du fichier FLAC à lire.
    
    Retour :
    - Aucun.
    """
    def lire_fichier_flac(self, chemin_fichier: str) -> None: 
        try:
            audio = AudioSegment.from_file(chemin_fichier)  # Cela peut être .mp3 ou .flac
            play(audio)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")


    """
    Fonction qui lit un fichier MP3.
    
    Paramètre :
    - chemin_fichier : chemin du fichier MP3 à lire.
    
    Retour :
    - Aucun.
    """
    def lire_fichier_mp3(self, chemin_fichier: str) -> None:  
        # Initialiser le mixer de pygame
        pygame.mixer.init()  # Initialise le module mixer de Pygame pour la lecture audio.
        pygame.mixer.music.load(chemin_fichier)  # Charge le fichier MP3 spécifié dans le chemin.
        pygame.mixer.music.play()  # Joue le fichier audio.

        # Attendre que la musique se termine
        while pygame.mixer.music.get_busy():  # Tant que la musique est en cours de lecture...
            time.sleep(1)  # Pause d'une seconde pour éviter une boucle continue et permettre une lecture fluide.


    """
    Fonction qui choisi le fichier audio a lire.
    
    Paramètre :
    - chemin_fichier : chemin du fichier WAV à lire.
    
    Retour :
    - Aucun.
    """
    def lecture_music(self, chemin_fichier: str) -> None:
        # Vérifie si le fichier se termine par l'extension '.mp3'
        if chemin_fichier.endswith('.mp3'):
            # Si le fichier est un MP3, appelle la méthode pour lire un fichier MP3
            self.lire_fichier_mp3(chemin_fichier)
        
        # Si le fichier n'est pas un MP3, vérifie s'il se termine par l'extension '.flac'
        elif chemin_fichier.endswith('.flac'):
            # Si le fichier est un FLAC, appelle la méthode pour lire un fichier FLAC
            self.lire_fichier_flac(chemin_fichier)


    
# Exemple d'utilisation :
# ecoute = Ecouter()  # Crée une instance de la classe Ecouter.

# Lire un fichier FLAC (exemple désactivé)
# ecoute.lire_fichier_flac(r'C:\Users\nelly\Desktop\projet python\Python_project\music\sample2.flac')  # Lancer la lecture d'un fichier MP3.

# Lire un fichier MP3
# ecoute.lire_fichier_flac(r'C:\Users\nelly\Desktop\projet python\Python_project\music\Halsey - 929.mp3')  # Lancer la lecture d'un fichier MP3.
