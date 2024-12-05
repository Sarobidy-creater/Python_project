#!/usr/bin/python3  
# -*- coding: UTF-8 -*-  
 
# Importation des modules nécessaires
import pygame  # Bibliothèque pour gérer les fonctionnalités multimédias comme jouer des fichiers audio.
from pydub import AudioSegment  # Pydub permet la manipulation des fichiers audio (conversion entre formats audio, etc.).
import time  # Le module time est utilisé pour introduire des pauses dans le programme.
import os  # Importe la bibliothèque os pour interagir avec le système de fichiers (par exemple, pour supprimer un fichier temporaire).


class Ecouter:  
    """
        Classe qui gère l'écoute d'un fichier audio donné.
    """
    
    def lire_fichier_audio(self, chemin_fichier:str) -> None:  
        """
            Fonction qui Charge et lit un fichier audio.

            Paramètre :
            - chemin_fichier : str : Chemin du fichier audio.
            
            Retour :
            - None : Aucune valeur de retour.
        """
        try:
            # Initialiser le mixer de pygame
            pygame.mixer.init()  # Initialise le module mixer de Pygame pour la lecture audio.
            pygame.mixer.music.load(chemin_fichier)  # Charge le fichier MP3 spécifié dans le chemin.
            pygame.mixer.music.play() # Joue le fichier audio.

        except pygame.error as e:
            print(f"Erreur pygame: impossible de lire le fichier audio - {e}")
        except FileNotFoundError as e:
            print(f"Erreur: fichier introuvable - {e}")
        except Exception as e:
            print(f"Erreur inattendue : {e}")
    
    def lire_fichier_wav(self, chemin_fichier:str) -> None:  
        """
            Fonction qui lit un fichier WAV.
            
            Paramètre :
            - chemin_fichier : str : chemin du fichier WAV à lire.
            
            Retour :
            - None : Aucune valeur de retour.
        """
        try:
            # Initialiser le mixer de pygame
            self.lire_fichier_audio(chemin_fichier)

            # Attendre que la musique se termine
            while pygame.mixer.music.get_busy():  # Tant que la musique est en cours de lecture (le fichier audio n'est pas terminé)...
                time.sleep(1)  # Pause d'une seconde pour éviter une boucle continue tout en permettant la lecture audio fluide.
        
        except KeyboardInterrupt:
            print("\nLecture interrompue.")
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"Erreur inattendue lors de la lecture du fichier WAV : {e}")

    def lire_fichier_flac(self, chemin_fichier:str) -> None:  
        """
            Fonction qui lit un fichier FLAC.
            
            Paramètre :
            - chemin_fichier : str : chemin du fichier FLAC à lire.
            
            Retour :
            - None : Aucune valeur de retour.
        """ 
        try:
            fichier_audio = None  # Initialisation de la variable fichier_audio à None

            temp_chem = os.path.abspath(fr"music\{chemin_fichier}")  # Création du chemin temporaire à partir du nom du fichier audio.
            print(f"Chemin absolu du fichier flac : {temp_chem}")  # Affiche le chemin pour le fichier audio temporaire.
            print("\n**********************************************\n")  # Affiche un séparateur visuel.

            # Vérification de l'existence du chemin temporaire
            if os.path.isfile(temp_chem):
                # Si le chemin temporaire existe, on l'assigne à fichier_audio
                fichier_audio = temp_chem
            else:
                # Sinon, on utilise le chemin original
                fichier_audio = chemin_fichier

            # Charger un fichier FLAC
            audio = AudioSegment.from_file(fichier_audio, format="flac") 

            # Exporter temporairement le fichier FLAC au format WAV pour le jouer avec pygame
            fichier_temp = "temp_audio.wav"  # Nom du fichier temporaire qui va contenir l'audio converti en WAV.
            audio.export(fichier_temp, format="wav")  # Convertit le fichier FLAC en WAV et l'enregistre sous "temp_audio.wav".
            
            # Jouer le fichier WAV avec pygame
            self.lire_fichier_wav(fichier_temp) 
            
            # Supprimer le fichier temporaire après utilisation
            os.remove(fichier_temp) 

        except Exception as e:
            print(f"Erreur lors de la lecture du fichier FLAC : {e}")
  
    def lire_fichier_mp3(self, chemin_fichier:str) -> None:  
        """
            Fonction qui lit un fichier MP3.
            
            Paramètre :
            - chemin_fichier : str : chemin du fichier MP3 à lire.
            
            Retour :
            - None : Aucune valeur de retour.
        """
        try:
            fichier_audio = None  # Initialisation de la variable fichier_audio à None

            temp_chem = os.path.abspath(fr"music\{chemin_fichier}")  # Création du chemin temporaire à partir du nom du fichier audio.
            print(f"Chemin absolu du fichier mp3 : {temp_chem}")  # Affiche le chemin pour le fichier audio temporaire.
            print("\n**********************************************\n")  # Affiche un séparateur visuel.

            # Vérification de l'existence du chemin temporaire
            if os.path.isfile(temp_chem):
                # Si le chemin temporaire existe, on l'assigne à fichier_audio
                fichier_audio = temp_chem
            else:
                # Sinon, on utilise le chemin original
                fichier_audio = chemin_fichier

            # Initialiser le mixer de pygame
            self.lire_fichier_audio(fichier_audio)

            # Attendre que la musique se termine
            while pygame.mixer.music.get_busy():  # Tant que la musique est en cours de lecture...
                time.sleep(1)  # Pause d'une seconde pour éviter une boucle continue et permettre une lecture fluide.

        except Exception as e:
            print(f"Erreur lors de la lecture du fichier MP3 : {e}")

    def lire_tout_audio(self, chemin:str ) -> None:
        """
            Fonction qui détermine le type de fichier audio et appelle la fonction appropriée pour le lire.
            
            Paramètre :
            - chemin : str : Chemin du fichier audio à lire.
            
            Retour :
            - None : Aucune valeur de retour.
        """
        try:
            if chemin.endswith('.mp3'):            
                self.lire_fichier_mp3(chemin)  # Crée un objet MP3 à partir du chemin si c'est un fichier MP3.

            elif chemin.endswith('.flac'):            
                self.lire_fichier_flac(chemin)

        except Exception as e:
            print(f"Erreur lors de la tentative de lecture du fichier : {e}")




   
