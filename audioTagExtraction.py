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


"""
    Une classe qui gère l'extraction et l'affichage des métadonnées
    des fichiers audio au format MP3 et FLAC, ainsi que l'affichage
    de leurs couvertures.
"""
class Extraction():


    """
        Fonction qui convertit une durée en millisecondes en minutes et secondes.

        Paramètre :
        - ms : int : La durée en millisecondes à convertir.

        Retour :
        - tuple : Un tuple contenant le nombre de minutes et de secondes.
    """
    def convertir_ms_en_minutes_secondes(self, ms) -> int:
        # Méthode qui convertit une durée en millisecondes en minutes et secondes.

        minutes = int(ms // 60)  # Calcule le nombre de minutes en divisant les millisecondes par 60.
        secondes = int(ms % 60)   # Calcule le nombre de secondes restantes après avoir extrait les minutes.

        return minutes, secondes   # Retourne un tuple contenant les minutes et les secondes.


    """
        Fonction qui extrait et affiche les métadonnées d'un fichier audio donné.

        Paramètre :
        - chemin : str : Le chemin du fichier audio dont les métadonnées doivent être extraites.

        Retour :
        - None : Cette méthode n'a pas de retour, elle imprime simplement les métadonnées.
    """
    def extraire_et_afficher_tag(self, chemin: str) -> None:
        # Méthode qui extrait et affiche les métadonnées d'un fichier audio donné.

        audio = None  # Initialise une variable audio à None, qui sera utilisée pour stocker l'objet audio.

        try:
            if chemin.endswith('.mp3'):
                # Vérifie si le chemin du fichier se termine par '.mp3'.
                audio = MP3(chemin, ID3=EasyID3)
                # Si c'est un fichier MP3, crée un objet MP3 à partir du chemin en utilisant EasyID3 pour lire les tags.

            elif chemin.endswith('.flac'):
                # Vérifie si le chemin du fichier se termine par '.flac'.
                audio = FLAC(chemin)
                # Si c'est un fichier FLAC, crée un objet FLAC à partir du chemin.

            if audio is None:
                print("Le fichier n'est ni au format MP3 ni FLAC.")
                return  # Si le format n'est pas reconnu, affiche un message et sort de la méthode.

            # Récupération des métadonnées audio
            # Utilisation de valeurs par défaut si elles sont absentes "blabla inconnu"
            # Utilisation [0] pour éviter d'afficher par exemple ['titre de l'audio'] ou ['artiste de l'audio']
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

            minutes, secondes = self.convertir_ms_en_minutes_secondes(duree)  # Convertit la durée en minutes et secondes en appelant la méthode convertie.

            print(f"Durée : {minutes}:{int(secondes):02d}")  # Affiche la durée au format 'minutes:secondes' avec les secondes formatées sur 2 chiffres.

        except Exception as e:  # Capture toute exception pouvant survenir dans le bloc try.
            print(f"Une erreur s'est produite lors de l'extraction des tags : {e}")  # Affiche un message d'erreur.


    """
        Fonction qui extrait et affiche la couverture d'un fichier audio donné.

        Paramètre :
        - chemin : str : Le chemin du fichier audio dont la couverture doit être extraite.

        Retour :
        
    """
    def extraire_et_afficher_cover(self, chemin: str) -> None:
        # Méthode qui extrait et affiche la couverture d'un fichier audio donné.

        nom_fichier = os.path.basename(chemin)  # Récupère le nom du fichier à partir du chemin donné.
        audio = None  # Initialise une variable audio à None.

        try:
            if chemin.endswith('.mp3'):
                audio = MP3(chemin, ID3=ID3)  # Crée un objet MP3 si c'est un fichier MP3.
            elif chemin.endswith('.flac'):
                audio = FLAC(chemin)  # Crée un objet FLAC si c'est un fichier FLAC.

            if isinstance(audio, MP3):
                # Vérifie si l'objet audio est une instance de MP3.
                for tag in audio.tags.values():  # Parcourt tous les tags de l'audio.
                    if isinstance(tag, APIC):  # Vérifie si le tag est de type APIC (Attached Picture).
                        print(f">> Cover art trouvée pour {nom_fichier}!")  # Indique que la couverture a été trouvée pour le fichier.

                        cover_data = tag.data  # Récupère les données de l'image de couverture.
                        image = Image.open(io.BytesIO(cover_data))  # Utilise PIL pour ouvrir l'image à partir des données en mémoire.
                        image.show()  # Affiche l'image de couverture à l'utilisateur.
                        break  # Sort de la boucle après avoir trouvé et affiché l'image.
                else:
                    print(f">> Aucune couverture trouvée pour {nom_fichier}!")  # Indique qu'il n'y a pas de couverture pour le fichier.

            elif isinstance(audio, FLAC):
                # Vérifie si l'objet audio est une instance de FLAC.
                for picture in audio.pictures:  # Parcourt toutes les images jointes dans le fichier FLAC.
                    if isinstance(picture, Picture):  # Vérifie si l'image est de type Picture.
                        print(f">> Cover art trouvée pour {nom_fichier}!")  # Indique que la couverture a été trouvée pour le fichier.

                        cover_data = picture.data  # Récupère les données de l'image de couverture.
                        image = Image.open(io.BytesIO(cover_data))  # Utilise PIL pour ouvrir l'image à partir des données en mémoire.
                        image.show()  # Affiche l'image de couverture à l'utilisateur.
                        break  # Sort de la boucle après avoir trouvé et affiché l'image.
                else:
                    print(f">> Aucune couverture trouvée pour {nom_fichier}!")  # Indique qu'il n'y a pas de couverture pour le fichier.

        except Exception as e:  # Capture toute exception pouvant survenir dans le bloc try.
            print(f"Une erreur s'est produite lors de l'extraction de la couverture : {e}")  # Affiche un message d'erreur.


    """
        Fonction qui extrait et affiche les métadonnées d'un fichier audio.

        Paramètre :
        - file_aud : str : Le nom du fichier audio dont les métadonnées doivent être extraites.

        Retour :
        - None : Cette méthode n'a pas de retour, elle imprime simplement les métadonnées.
    """
    def audio_extraire_et_afficher_tag(self, file_aud: str) -> None:
        # Méthode qui extrait et affiche les métadonnées d'un fichier audio.

        fichier_audio = None  # Initialisation de la variable fichier_audio à None

        temp_chem = os.path.abspath(fr"music\\{file_aud}")  # Création du chemin temporaire à partir du nom du fichier audio.
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

        try:
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
