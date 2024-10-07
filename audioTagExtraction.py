#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from mutagen.flac import FLAC, Picture
from PIL import Image 
import mimetypes
import io
import os


class Extraction():
    # Définition d'une classe nommée Extraction qui contient des méthodes pour extraire des métadonnées audio.


    """
        Convertit une durée millisecondes en minutes et secondes.

        Paramètre :
        - ms : la durée en millisecondes.

        Retour :
        - Un tuple (minutes, secondes).
    """
    def convertir_ms_en_minutes_secondes(self, ms) -> int:
        # Méthode qui convertit une durée en millisecondes en minutes et secondes.

        minutes = int(ms // 60)
        # Calcule le nombre de minutes en divisant les millisecondes par 60.

        secondes = int(ms % 60)
        # Calcule le nombre de secondes restantes après avoir extrait les minutes.

        return minutes, secondes
        # Retourne un tuple contenant les minutes et les secondes.


    """
        Extrait et affiche les métadonnées d'un fichier audio (MP3 ou FLAC).

        Paramètre :
        - chemin : le chemin du fichier audio à analyser.

        Retour :
        - Aucun (affiche directement les résultats dans la console).
    """
    def extraire_et_afficher_tag(self, chemin: str) -> None:
        # Méthode qui extrait et affiche les métadonnées d'un fichier audio donné.

        audio = None
        # Initialise une variable audio à None, qui sera utilisée pour stocker l'objet audio.

        if chemin.endswith('.mp3'):
            # Vérifie si le chemin du fichier se termine par '.mp3'.
            audio = MP3(chemin, ID3=EasyID3)
            # Si c'est un fichier MP3, crée un objet MP3 à partir du chemin en utilisant EasyID3 pour lire les tags.

        elif chemin.endswith('.flac'):
            # Vérifie si le chemin du fichier se termine par '.flac'.
            audio = FLAC(chemin)
            # Si c'est un fichier FLAC, crée un objet FLAC à partir du chemin.

        # Récupération des métadonnées audio
        # Utilisation de valeurs par défaut si elles sont absentes "blabla inconnu"
        # Utilisation [0] pour éviter d'afficher par exemple ['titre de l'audio'] ou ['artiste de l'audio']
        titre = audio.get('title', ['Titre inconnu'])[0]
        # Extrait le titre, ou retourne 'Titre inconnu' s'il n'est pas trouvé.

        artiste = audio.get('artist', ['Artiste inconnu'])[0]
        # Extrait l'artiste, ou retourne 'Artiste inconnu' s'il n'est pas trouvé.

        album = audio.get('album', ['Album inconnu'])[0]
        # Extrait l'album, ou retourne 'Album inconnu' s'il n'est pas trouvé.

        genre = audio.get('genre', ['Genre inconnu'])[0]
        # Extrait le genre, ou retourne 'Genre inconnu' s'il n'est pas trouvé.

        date = audio.get('date', ['Date inconnu'])[0]
        # Extrait la date, ou retourne 'Date inconnu' s'il n'est pas trouvé.

        organization = audio.get('organization', ['Organization: inconnu'])[0]
        # Extrait l'organisation, ou retourne 'Organization: inconnu' s'il n'est pas trouvé.

        # Affichage des informations extraites dans la console.
        print(f"Titre : {titre}")
        print(f"Artiste : {artiste}")
        print(f"Album : {album}")
        print(f"Genre : {genre}")
        print(f"Date : {date}")
        print(f"Organization : {organization}")

        duree = audio.info.length
        # Récupère la durée de l'audio en secondes.

        minutes, secondes = self.convertir_ms_en_minutes_secondes(duree)
        # Convertit la durée en minutes et secondes en appelant la méthode convertie.

        print(f"Durée : {minutes}:{int(secondes):02d}")
        # Affiche la durée au format 'minutes:secondes' avec les secondes formatées sur 2 chiffres.


    """
        Extrait et affiche la couverture (cover art) d'un fichier audio (MP3 ou FLAC).

        Paramètre :
        - chemin : le chemin du fichier audio à analyser.

        Retour :
        - Aucun (affiche directement la couverture via une fenêtre d'image).
    """
    def extraire_et_afficher_cover(self, chemin: str) -> None:
        # Méthode qui extrait et affiche la couverture d'un fichier audio donné.

        nom_fichier = os.path.basename(chemin)
        # Récupère le nom du fichier à partir du chemin donné.

        audio = None
        # Initialise une variable audio à None.

        if chemin.endswith('.mp3'):
            # Vérifie si le chemin du fichier se termine par '.mp3'.
            audio = MP3(chemin, ID3=ID3)
            # Si c'est un fichier MP3, crée un objet MP3 à partir du chemin en utilisant ID3 pour lire les tags.

        elif chemin.endswith('.flac'):
            # Vérifie si le chemin du fichier se termine par '.flac'.
            audio = FLAC(chemin)
            # Si c'est un fichier FLAC, crée un objet FLAC à partir du chemin.

        if isinstance(audio, MP3):
            # Vérifie si l'objet audio est une instance de MP3.
            for tag in audio.tags.values():
                # Parcourt tous les tags de l'audio.
                if isinstance(tag, APIC):
                    # Vérifie si le tag est de type APIC (Attached Picture).
                    print(f">> Cover art trouvée pour {nom_fichier}!")
                    # Indique que la couverture a été trouvée pour le fichier.

                    cover_data = tag.data
                    # Récupère les données de l'image de couverture.

                    image = Image.open(io.BytesIO(cover_data))
                    # Utilise PIL pour ouvrir l'image à partir des données en mémoire.

                    image.show()  # Affiche l'image.
                    # Montre l'image de couverture à l'utilisateur.

                    break  # Sort de la boucle après avoir trouvé et affiché l'image.
            else:
                # Si aucune image n'a été trouvée dans les tags.
                print(f">> Aucune couverture trouvée pour {nom_fichier}!")
                # Indique qu'il n'y a pas de couverture pour le fichier.

        elif isinstance(audio, FLAC):
            # Vérifie si l'objet audio est une instance de FLAC.
            for picture in audio.pictures:
                # Parcourt toutes les images jointes dans le fichier FLAC.
                if isinstance(picture, Picture):
                    # Vérifie si l'image est de type Picture.
                    print(f">> Cover art trouvée pour {nom_fichier}!")
                    # Indique que la couverture a été trouvée pour le fichier.

                    cover_data = picture.data
                    # Récupère les données de l'image de couverture.

                    image = Image.open(io.BytesIO(cover_data))
                    # Utilise PIL pour ouvrir l'image à partir des données en mémoire.

                    image.show()  # Affiche l'image.
                    # Montre l'image de couverture à l'utilisateur.

                    break  # Sort de la boucle après avoir trouvé et affiché l'image.
            else:
                # Si aucune image n'a été trouvée dans les images jointes.
                print(f">> Aucune couverture trouvée pour {nom_fichier}!")
                # Indique qu'il n'y a pas de couverture pour le fichier.


    """
        Extrait et affiche les métadonnées d'un fichier audio (MP3 ou FLAC).

        Paramètre :
        - chemin : le chemin du fichier audio à analyser.

        Retour :
        - Aucun (affiche directement les résultats dans la console).
    """
    def audio_extraire_et_afficher_tag(self, file_aud: str) -> None:

        # Initialisation de la variable fichier_audio à None
        fichier_audio = None
    
        # Création du chemin temporaire
        # Création du chemin temporaire
        # temp_chem = os.path.abspath(fr"Python_project\\muxic\\{file_aud}")
        temp_chem = os.path.abspath(fr"muxic\\{file_aud}")
        print(f"chemin pour le fichier : {temp_chem}")
        print("\n**********************************************\n")

        # Vérification de l'existence du chemin temporaire
        if os.path.isfile(temp_chem):
            # Si le chemin temporaire existe, on l'assigne à fichier_audio
            fichier_audio = temp_chem
        else:
            # Sinon, on utilise le chemin original
            fichier_audio = file_aud
        
        # Initialise une variable audio à None, qui sera utilisée pour stocker l'objet audio.
        audio = None
            
        # Vérifie si le chemin du fichier se termine par '.mp3'.
        if fichier_audio.endswith('.mp3'):            
            # Si c'est un fichier MP3, crée un objet MP3 à partir du chemin en utilisant EasyID3 pour lire les tags.
            audio = MP3(fichier_audio, ID3=EasyID3)

        # Vérifie si le chemin du fichier se termine par '.flac'.
        elif fichier_audio.endswith('.flac'):            
            # Si c'est un fichier FLAC, crée un objet FLAC à partir du chemin.
            audio = FLAC(fichier_audio)

        # Récupération des métadonnées audio
        # Utilisation de valeurs par défaut si elles sont absentes "blabla inconnu"
        # Utilisation [0] pour éviter d'afficher par exemple ['titre de l'audio'] ou ['artiste de l'audio']
        titre = audio.get('title', ['Titre inconnu'])[0]
        # Extrait le titre, ou retourne 'Titre inconnu' s'il n'est pas trouvé.

        artiste = audio.get('artist', ['Artiste inconnu'])[0]
        # Extrait l'artiste, ou retourne 'Artiste inconnu' s'il n'est pas trouvé.

        album = audio.get('album', ['Album inconnu'])[0]
        # Extrait l'album, ou retourne 'Album inconnu' s'il n'est pas trouvé.

        genre = audio.get('genre', ['Genre inconnu'])[0]
        # Extrait le genre, ou retourne 'Genre inconnu' s'il n'est pas trouvé.

        date = audio.get('date', ['Date inconnu'])[0]
        # Extrait la date, ou retourne 'Date inconnu' s'il n'est pas trouvé.

        organization = audio.get('organization', ['Organization: inconnu'])[0]
        # Extrait l'organisation, ou retourne 'Organization: inconnu' s'il n'est pas trouvé.

        # Affichage des informations extraites dans la console.
        print(f"Titre : {titre}")
        print(f"Artiste : {artiste}")
        print(f"Album : {album}")
        print(f"Genre : {genre}")
        print(f"Date : {date}")
        print(f"Organization : {organization}")

        duree = audio.info.length
        # Récupère la durée de l'audio en secondes.

        minutes, secondes = self.convertir_ms_en_minutes_secondes(duree)
        # Convertit la durée en minutes et secondes en appelant la méthode convertie.

        print(f"Durée : {minutes}:{int(secondes):02d}")
        # Affiche la durée au format 'minutes:secondes' avec les secondes formatées sur 2 chiffres.




# ad = Extraction()

# chemin = "RERD.mp3"

# ad.audio_extraire_et_afficher_tag(chemin)


