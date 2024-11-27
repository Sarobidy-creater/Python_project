#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Importation des modules nécessaires
from mutagen.easyid3 import EasyID3  # Pour lire et écrire les métadonnées ID3 dans les fichiers MP3.
from mutagen.mp3 import MP3  # Pour gérer les fichiers audio MP3 et accéder à leurs métadonnées.
from mutagen.id3 import ID3, APIC  # Pour manipuler les balises ID3 et gérer les images intégrées comme les couvertures d'album.
from mutagen.flac import FLAC, Picture  # Pour travailler avec les fichiers audio FLAC et gérer les images intégrées.
from PIL import Image  # Pour ouvrir, modifier et enregistrer des images dans divers formats.
import mimetypes  # Pour déterminer le type MIME des fichiers en fonction de leur extension.
import io  # Pour travailler avec des flux de données en mémoire.
import os  # Importe la bibliothèque os pour interagir avec le système de fichiers


class Extraction():
    """
        Une classe qui gère l'extraction et l'affichage des métadonnées
        des fichiers audio au format MP3 et FLAC, ainsi que l'affichage
        de leurs couvertures.
    """

    def convertir_ms_en_minutes_secondes(self, ms) -> int:
        """
            Fonction qui convertit une durée en millisecondes en minutes et secondes.

            Paramètre :
            - ms : str : La durée en millisecondes à convertir.

            Retour :
            - tuple : Un tuple contenant le nombre de minutes et de secondes.
        """
        minutes = int(ms // 60)  # Calcule le nombre de minutes en divisant les millisecondes par 60.
        secondes = int(ms % 60)   # Calcule le nombre de secondes restantes après avoir extrait les minutes.

        return minutes, secondes   # Retourne un tuple contenant les minutes et les secondes.

    def audio_extraire_et_afficher_tag(self, file_aud: str) -> None:
        """
            Méthode qui extrait et affiche les métadonnées d'un fichier audio.

            Paramètre :
            - file_aud : str : Le nom du fichier audio dont les métadonnées doivent être extraites.

            Retour :
            - None : Aucune valeur de retour.
        """
        try:
            fichier_audio = None  # Initialisation de la variable fichier_audio à None

            temp_chem = os.path.abspath(fr"music\{file_aud}")  # Création du chemin temporaire à partir du nom du fichier audio.
            print(f"chemin pour le fichier : {temp_chem}")  # Affiche le chemin pour le fichier audio temporaire.
            print("\n**********************************************\n")  # Affiche un séparateur visuel.

            # Vérification de l'existence du chemin temporaire
            if os.path.isfile(temp_chem):
                # Si le chemin temporaire existe, on l'assigne à fichier_audio
                fichier_audio = temp_chem
            else:
                # Sinon, on utilise le chemin original
                fichier_audio = file_aud
            
            audio = None  # Initialise une variable audio à None.

        
            if fichier_audio.endswith('.mp3'):            
                audio = MP3(fichier_audio, ID3=EasyID3)  # Crée un objet MP3 à partir du chemin si c'est un fichier MP3.

            elif fichier_audio.endswith('.flac'):            
                audio = FLAC(fichier_audio)  # Crée un objet FLAC à partir du chemin si c'est un fichier FLAC.

            if audio is None:
                print("Le fichier n'est ni au format MP3 ni FLAC.")  # Vérifie si le format est reconnu.
                return  # Si le format n'est pas reconnu, sort de la méthode.

            # Récupération des métadonnées audio
            titre = audio.get('title', ['Titre inconnu'])[0]  # Extrait le titre ou retourne 'Titre inconnu'.
            artiste = audio.get('artist', ['Artiste inconnu'])[0]  # Extrait l'artiste ou retourne 'Artiste inconnu'.
            album = audio.get('album', ['Album inconnu'])[0]  # Extrait l'album ou retourne 'Album inconnu'.
            genre = audio.get('genre', ['Genre inconnu'])[0]  # Extrait le genre ou retourne 'Genre inconnu'.
            date = audio.get('date', ['Date inconnu'])[0]  # Extrait la date ou retourne 'Date inconnu'.
            organization = audio.get('organization', ['Organization: inconnu'])[0]  # Extrait l'organisation ou retourne 'Organization: inconnu'.

            # Affichage des informations extraites dans la console.
            print(f"Titre : {titre}")  # Affiche le titre.
            print(f"Artiste : {artiste}")  # Affiche l'artiste.
            print(f"Album : {album}")  # Affiche l'album.
            print(f"Genre : {genre}")  # Affiche le genre.
            print(f"Date : {date}")  # Affiche la date.
            print(f"Organization : {organization}")  # Affiche l'organisation.

            duree = audio.info.length  # Récupère la durée de l'audio en secondes.
            minutes, secondes = self.convertir_ms_en_minutes_secondes(duree)  # Convertit la durée en minutes et secondes.

            print(f"Durée : {minutes}:{int(secondes):02d}")  # Affiche la durée au format 'minutes:secondes'.

        except Exception as e:  # Capture toute exception pouvant survenir dans le bloc try.
            print(f"Une erreur s'est produite lors de l'extraction des tags : {e}")  # Affiche un message d'erreur.

    def extraction_et_afficher_tag(self, file_aud: str) -> str:
        """
            Méthode qui extrait et retourne les métadonnées d'un fichier audio sous forme de chaîne.

            Paramètre :
            - file_aud : str : Le nom du fichier audio dont les métadonnées doivent être extraites.

            Retour :
            - str : Métadonnées d'un fichier audio sous forme de chaîne.
        """
        try:
            temp_chem = os.path.abspath(os.path.join("music", file_aud))  
            # Génère un chemin absolu en combinant le répertoire "music" et le nom du fichier audio.

            if not os.path.isfile(temp_chem):  
                # Vérifie si le fichier existe à ce chemin.
                return f"Le fichier {file_aud} n'existe pas dans le répertoire 'music'."  
                # Retourne un message d'erreur si le fichier n'existe pas.

            fichier_audio = temp_chem  # Définit le chemin complet du fichier audio.
            audio = None  # Initialise la variable `audio` avec None.

            if fichier_audio.endswith('.mp3'):  
                # Vérifie si le fichier est au format MP3.
                audio = MP3(fichier_audio, ID3=EasyID3)  
                # Charge les métadonnées MP3 avec le support ID3 simplifié.
            elif fichier_audio.endswith('.flac'):  
                # Vérifie si le fichier est au format FLAC.
                audio = FLAC(fichier_audio)  
                # Charge les métadonnées FLAC.

            if audio is None:  
                # Si le fichier n'est ni MP3 ni FLAC, retourne un message d'erreur.
                return "Le fichier n'est ni au format MP3 ni FLAC."

            metadata = {  
                # Crée un dictionnaire pour stocker les métadonnées.
                'Titre': audio.get('title', ['Titre inconnu'])[0],
                '\n\nArtiste': audio.get('artist', ['Artiste inconnu'])[0],
                '\n\nAlbum': audio.get('album', ['Album inconnu'])[0],
                '\n\nGenre': audio.get('genre', ['Genre inconnu'])[0],
                '\n\nDate': audio.get('date', ['Date inconnu'])[0],
                '\n\nOrganisation': audio.get('organization', ['Organisation inconnue'])[0],
            }

            metadata_str = "\n".join(f"{key} : {value}" for key, value in metadata.items())  
            # Formate les métadonnées sous forme de chaîne lisible.

            duree = audio.info.length  
            # Récupère la durée totale de l'audio en secondes.
            minutes, secondes = self.convertir_ms_en_minutes_secondes(duree)  
            # Convertit la durée en minutes et secondes.
            metadata_str += f"\n\n\nDurée : {minutes}:{int(secondes):02d}"  
            # Ajoute la durée formatée à la chaîne des métadonnées.

            return metadata_str  # Retourne la chaîne contenant les métadonnées.

        except Exception as e:
            return f"Une erreur s'est produite lors de l'extraction des tags : {e}"
