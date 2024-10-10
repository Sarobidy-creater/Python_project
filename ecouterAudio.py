#!/usr/bin/python3  
# -*- coding: UTF-8 -*-  

# Importation des modules nécessaires
import pygame  # Bibliothèque pour gérer les fonctionnalités multimédias comme jouer des fichiers audio.
from pydub import AudioSegment  # Pydub permet la manipulation des fichiers audio (conversion entre formats audio, etc.).
import time  # Le module time est utilisé pour introduire des pauses dans le programme.
import os  # Importe la bibliothèque os pour interagir avec le système de fichiers (par exemple, pour supprimer un fichier temporaire).


"""
Classe qui gère l'écoute d'un fichier audio donné.
"""
class Ecouter:  # Déclaration de la classe 'Ecouter', qui contient des méthodes pour lire différents formats audio.


    """
    Fonction qui lit un fichier WAV.
    
    Paramètre :
    - chemin_fichier : chemin du fichier WAV à lire.
    
    Retour :
    - Aucun.
    """
    def lire_fichier_wav(self, chemin_fichier):  
        # Initialiser le mixer de pygame
        pygame.mixer.init()  # Initialise le module mixer de Pygame, nécessaire pour jouer de la musique.
        pygame.mixer.music.load(chemin_fichier)  # Charge le fichier WAV spécifié dans le chemin.
        pygame.mixer.music.play()  # Joue le fichier audio.

        # Attendre que la musique se termine
        while pygame.mixer.music.get_busy():  # Tant que la musique est en cours de lecture (le fichier audio n'est pas terminé)...
            time.sleep(1)  # Pause d'une seconde pour éviter une boucle continue tout en permettant la lecture audio fluide.


    """
    Fonction qui lit un fichier FLAC.
    
    Paramètre :
    - chemin_fichier : chemin du fichier FLAC à lire.
    
    Retour :
    - Aucun.
    """
    def lire_fichier_flac(self, chemin_fichier):  
        # Charger un fichier FLAC
        audio = AudioSegment.from_file(chemin_fichier, format="flac")  # Utilise Pydub pour charger le fichier FLAC.

        # Exporter temporairement le fichier FLAC au format WAV pour le jouer avec pygame
        fichier_temp = "temp_audio.wav"  # Nom du fichier temporaire qui va contenir l'audio converti en WAV.
        audio.export(fichier_temp, format="wav")  # Convertit le fichier FLAC en WAV et l'enregistre sous "temp_audio.wav".
        
        # Jouer le fichier WAV avec pygame
        self.lire_fichier_wav(fichier_temp)  # Appelle la méthode 'lire_fichier_wav' pour jouer le fichier WAV temporaire.
        
        # Supprimer le fichier temporaire après utilisation
        os.remove(fichier_temp)  # Supprime le fichier temporaire une fois la lecture terminée pour éviter l'encombrement.


    """
    Fonction qui lit un fichier MP3.
    
    Paramètre :
    - chemin_fichier : chemin du fichier MP3 à lire.
    
    Retour :
    - Aucun.
    """
    def lire_fichier_mp3(self, chemin_fichier):  # Définit une méthode pour lire un fichier audio au format MP3.
        # Initialiser le mixer de pygame
        pygame.mixer.init()  # Initialise le module mixer de Pygame pour la lecture audio.
        pygame.mixer.music.load(chemin_fichier)  # Charge le fichier MP3 spécifié dans le chemin.
        pygame.mixer.music.play()  # Joue le fichier audio.

        # Attendre que la musique se termine
        while pygame.mixer.music.get_busy():  # Tant que la musique est en cours de lecture...
            time.sleep(1)  # Pause d'une seconde pour éviter une boucle continue et permettre une lecture fluide.


# Exemple d'utilisation :
ecoute = Ecouter()  # Crée une instance de la classe Ecouter.

# Lire un fichier FLAC (exemple désactivé)
# ecoute.lire_fichier_flac('chemin_du_fichier.flac')  # Lancer la lecture d'un fichier FLAC (cette ligne est actuellement commentée).

# Lire un fichier MP3
ecoute.lire_fichier_mp3(r'C:\Users\nelly\Desktop\projet python\Python_project\music\Halsey - 929.mp3')  # Lancer la lecture d'un fichier MP3.
