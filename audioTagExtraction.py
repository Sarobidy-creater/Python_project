#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from mutagen.flac import FLAC, Picture
from PIL import Image
import io
import os

"""
    Convertit une durée millisecondes en minutes et secondes.

    Paramètre :
    - ms : la durée en millisecondes.

    Retour :
    - Un tuple (minutes, secondes).
"""
def convertir_ms_en_minutes_secondes(ms) -> int:
    # Calcul des minutes en divisant la durée totale par 60
    minutes = int(ms // 60)
    # Calcul des secondes restantes après division par 60
    secondes = int(ms % 60)
    return minutes, secondes


"""
    Extrait et affiche les métadonnées d'un fichier audio (MP3 ou FLAC).

    Paramètre :
    - chemin : le chemin du fichier audio à analyser.

    Retour :
    - Aucun (affiche directement les résultats dans la console).
"""
def extraire_et_afficher_tag(chemin : str) -> None:
    audio = None
    if chemin.endswith('.mp3'):
        audio = MP3(chemin, ID3=EasyID3)
    elif chemin.endswith('.flac'):
        audio = FLAC(chemin)
    
    # Récupération des métadonnées audio
    # Utilisation de valeurs par défaut si elles sont absentes "blabla inconnu"
    # Utilisation [0] pour éviter d'afficher par exemple ['titre de l'audio'] ou ['artiste de l'audio']
    titre = audio.get('title', ['Titre inconnu'])[0]
    artiste = audio.get('artist', ['Artiste inconnu'])[0]
    album = audio.get('album', ['Album inconnu'])[0]
    genre = audio.get('genre', ['Genre inconnu'])[0]
    date = audio.get('date', ['Date inconnu'])[0]
    organization = audio.get('organization', ['Organization: inconnu'])[0]  
    
    # Affichage des informations extraites
    print(f"Titre : {titre}")
    print(f"Artiste : {artiste}")
    print(f"Album : {album}")
    print(f"Genre : {genre}")
    print(f"Date : {date}")
    print(f"Organization : {organization}")
    
    # Extraction et affichage de la durée de l'audio en minutes et secondes
    duree = audio.info.length
    minutes, secondes = convertir_ms_en_minutes_secondes(duree)
    print(f"Durée : {minutes}:{int(secondes):02d}")


"""
    Extrait et affiche la couverture (cover art) d'un fichier audio (MP3 ou FLAC).

    Paramètre :
    - chemin : le chemin du fichier audio à analyser.

    Retour :
    - Aucun (affiche directement la couverture via une fenêtre d'image).
"""
def extraire_et_afficher_cover(chemin : str) -> None:
    # Pour récupérer uniquement le nom du fichier à partir du chemin donné
    nom_fichier = os.path.basename(chemin)
    
    audio = None
    if chemin.endswith('.mp3'):
        audio = MP3(chemin, ID3=ID3)
    elif chemin.endswith('.flac'):
        audio = FLAC(chemin)

    if isinstance(audio, MP3):
        # Parcourt les tags pour trouver un tag de type APIC (Attached Picture)
        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                # Si une image est trouvée, récupère les données de l'image
                print(f">> Cover art trouvée pour {nom_fichier}!")
                cover_data = tag.data
                
                # Utilise PIL pour ouvrir et afficher l'image
                image = Image.open(cover_data)
                image.show()  # Affiche l'image

                break
        else:
            print(f">> Aucune couverture trouvée pour {nom_fichier}!")

    elif isinstance(audio, FLAC):
        # Parcourt les images jointes pour trouver la couverture
        for picture in audio.pictures:
            if isinstance(picture, Picture):
                # PICTURE = Frame for cover art in FLAC
                print(f">> Cover art trouvée pour {nom_fichier}!")
                cover_data = picture.data
                
                # Utilise PIL pour ouvrir et afficher l'image
                image = Image.open(io.BytesIO(cover_data))
                image.show()  # Affiche l'image

                break
        else:
            print(f">> Aucune couverture trouvée pour {nom_fichier}!")




# Chemin vers le fichier audio à analyser (remplacez-le par le fichier de votre  mp3 ou flac)
chemin = r"c:\Chemin\vers\fichier"

print(f"***************************************************************")
# Appel de la fonction pour extraire et afficher les métadonnées
extraire_et_afficher_tag(chemin)

# Appel de la fonction pour extraire et afficher la couverture
extraire_et_afficher_cover(chemin)
print(f"***************************************************************")
