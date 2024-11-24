#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Importation des modules nécessaires
from mutagen.easyid3 import EasyID3  # Pour lire et écrire les métadonnées ID3 dans les fichiers MP3.
from mutagen.mp3 import MP3  # Pour gérer les fichiers audio MP3 et accéder à leurs métadonnées.
from mutagen.id3 import ID3, APIC  # Pour manipuler les balises ID3 et gérer les images intégrées comme les couvertures d'album.
from mutagen.flac import FLAC, Picture  # Pour travailler avec les fichiers audio FLAC et gérer les images intégrées.
import mimetypes  # Pour déterminer le type MIME des fichiers en fonction de leur extension.
import os  # Pour interagir avec le système de fichiers.
import xml.etree.ElementTree as ET


class Explorer():
    """
        Une classe qui permet d'explorer des dossiers et de gérer les fichiers audio.
    """

    def _explorer_dossier_audio(self, chemin, fichier_sortie):
        """
            Fonction qui explore le dossier spécifié et enregistre les chemins des fichiers audio (MP3, FLAC) dans un fichier.

            Paramètres :
            - chemin : str : Le chemin du dossier à explorer.
            - fichier_sortie : str : Le chemin du fichier de sortie où enregistrer les chemins audio.

            Retourne :
            - str : Le chemin du fichier de sortie, ou None en cas d'erreur.
        """
        out_dir = fichier_sortie.replace("\\", "/")  # Normalise le chemin du fichier de sortie.
        try:
            with open(out_dir, 'w', encoding='utf-8') as f:  # Ouvre le fichier de sortie en mode écriture.
                for racine, sous_dossiers, fichiers in os.walk(chemin):  # Parcours les fichiers dans le répertoire.
                    for fichier in fichiers:
                        chemin_coplt = os.path.join(racine, fichier)  # Construit le chemin complet du fichier.
                        chemin_complet = chemin_coplt.replace("\\", "/")
                        nom = os.path.basename(chemin_complet)  # Récupère le nom du fichier.
                        # Vérifie si le nom du fichier se termine par '.mp3' ou '.flac'.
                        if nom.endswith(".mp3") or nom.endswith(".flac"):
                            type_mime, _ = mimetypes.guess_type(chemin_complet)  # Détermine le type MIME du fichier.
                            if type_mime in ['audio/mpeg', 'audio/x-flac']:  # Vérifie que le type MIME est valide.
                                f.write(f"{chemin_complet}\n")  # Écrit le chemin du fichier dans le fichier de sortie.

            return fichier_sortie  # Retourne le chemin du fichier de sortie.
        except Exception as e:
            print(f"Une erreur est survenue lors de l'écriture dans le fichier : {e}")
            return None  # Retourne None en cas d'erreur.

    def explorer_dossier_console(self, chemin_name):
        """
            Fonction qui explore un dossier donné et affiche les chemins des fichiers audio (MP3, FLAC) dans la console.

            Paramètre :
            - chemin_name : str : Le chemin du dossier à explorer. Utilisez "." pour indiquer le répertoire courant.

            Retourne :
            - None : Aucune valeur de retour.
        """
        try:
            # os.getcwd() : Cette fonction renvoie le répertoire de travail actuel (current working directory)
            chemin = os.getcwd() if chemin_name == "." else os.path.abspath(chemin_name)  # Définit le chemin à explorer.
            for racine, sous_dossiers, fichiers in os.walk(chemin):  # Parcours les fichiers dans le répertoire.
                for fichier in fichiers:
                    chemin_complet = os.path.join(racine, fichier)  # Construit le chemin complet du fichier.
                    nom = os.path.basename(chemin_complet)  # Récupère le nom du fichier.

                    # Vérifie si le nom du fichier se termine par '.mp3' ou '.flac'.
                    if nom.endswith(".mp3") or nom.endswith(".flac"):
                        type_mime, _ = mimetypes.guess_type(chemin_complet)  # Détermine le type MIME du fichier.
                        if type_mime in ['audio/mpeg', 'audio/flac']:  # Vérifie que le type MIME est valide.
                            print(f"{chemin_complet}\n")  # Affiche le chemin du fichier dans la console.
        except Exception as e:
            print(f"Une erreur est survenue lors de l'exploration du dossier : {e}")

    def explorer_dossier_gui(self, chemin) -> str:
        """
            Fonction qui explore un dossier donné et enregistre les chemins des fichiers audio (MP3, FLAC) dans un fichier temporaire.

            Paramètre :
            - chemin : str : Le chemin du dossier à explorer.

            Retourne :
            - str : Le chemin du fichier temporaire contenant les chemins des fichiers audio, ou None en cas d'erreur.
        """
        fichier_sortie = os.path.abspath(r'Python_project\FichierTemp\TempFile.txt')  
        return self._explorer_dossier_audio(chemin, fichier_sortie)  # Appelle la méthode d'exploration des fichiers audio.

    def explorer_Playlist(self):
        """
           Fonction qui recherche les fichiers de playlist .xspf dans le répertoire courant.

            Paramètre :
            - None : Aucune valeur en paramètre.

            Retourne :
            - str : Un tableau de chemin absolu de chaque fichier .xspf.
        """
        tableau_playlist = []
        chemin = os.getcwd()

        # Parcourt tous les fichiers dans le répertoire
        for racine, sous_dossiers, fichiers in os.walk(chemin):
            for fichier in fichiers:
                chemin_complet = os.path.join(racine, fichier)
                nom = os.path.basename(chemin_complet)

                # Vérifie si le fichier est une playlist .xspf
                if nom.endswith(".xspf"):
                    tableau_playlist.append(chemin_complet)

        return tableau_playlist
    
    def extraire_pistes_de_playlist(self, chemin_complet):
        """
           Fonction qui extrait les chemins audio d'une playlist .xspf donnée.

            Paramètre :
            - chemin_complet : str : Le chemin absolu d'un fichier .xspf.

            Retourne :
            - str : Une liste des chemins absolu de chaque fichier audio dans la playlist .xspf.
        """
        print(f"Chemin du fichier : {chemin_complet}")

        try:
            list_chemin_absolu = []  # Liste pour stocker les chemins audio
            tree = ET.parse(chemin_complet)
            root = tree.getroot()

            # Définir les espaces de noms
            namespaces = {'xspf': 'http://xspf.org/ns/0/'}

            # Parcours les éléments <track> dans <trackList>
            for track in root.findall(".//xspf:trackList/xspf:track", namespaces):
                location_elem = track.find('xspf:location', namespaces)

                # Vérifie si l'élément 'location' existe et contient du texte
                if location_elem is not None and location_elem.text:
                    chemin_absolu = location_elem.text.strip()

                    # Si le chemin commence par 'file://', on le nettoie pour obtenir un chemin standard
                    if chemin_absolu.startswith("file:///"):
                        chemin_absolu = chemin_absolu[8:]  # Supprimer le préfixe 'file://'

                    # Vérifie si le fichier existe avant d'ajouter le chemin
                    if os.path.exists(chemin_absolu):
                        list_chemin_absolu.append(chemin_absolu)
                    else:
                        print(f"Attention : le fichier {chemin_absolu} n'existe pas.")
                else:
                    print(f"Attention : une piste sans chemin 'location' dans {chemin_complet}")
            return list_chemin_absolu
        
        except ET.ParseError as e:
            print(f"Erreur lors du parsing du fichier XML {chemin_complet} : {e}")
        except FileNotFoundError:
            print(f"Erreur : le fichier {chemin_complet} est introuvable.")
        except Exception as e:
            print(f"Erreur inconnue pour le fichier {chemin_complet} : {e}")

    """
    def explorer_dossier_interface(self, chemin) -> str:
        
        Fonction qui explore un dossier donné et enregistre les chemins des fichiers audio (MP3, FLAC) dans un fichier temporaire.

        Paramètre :
        - chemin : str : Le chemin du dossier à explorer.

        Retourne :
        - str : Le chemin du fichier temporaire contenant les chemins des fichiers audio, ou None en cas d'erreur.
        
        fichier_sortie = os.path.abspath(r'FichierTemp\TempFile.txt')
        # print("fichier_sortie**********************************************************************")
        # print(fichier_sortie)
        # print("**********************************************************************") 
         
        return self._explorer_dossier_audio(chemin, fichier_sortie)  # Appelle la méthode d'exploration des fichiers audio.
    """

    """
    def explorer_dossier(self, chemin_name):
        
            Fonction qui explore un dossier donné et retourne le chemin du premier fichier audio (MP3, FLAC) trouvé.

            Paramètre :
            - chemin_name : str : Le chemin du dossier à explorer. Utilisez "." pour indiquer le répertoire courant.

            Retourne :
            - str : Le chemin complet du premier fichier audio trouvé, ou None en cas d'erreur.
        
        try:
            chemin = os.getcwd() if chemin_name == "." else os.path.abspath(chemin_name)  # Définit le chemin à explorer.
            for racine, sous_dossiers, fichiers in os.walk(chemin):  # Parcours les fichiers dans le répertoire.
                for fichier in fichiers:
                    chemin_complet = os.path.join(racine, fichier)  # Construit le chemin complet du fichier.
                    nom = os.path.basename(chemin_complet)  # Récupère le nom du fichier.

                    # Vérifie si le nom du fichier se termine par '.mp3' ou '.flac'.
                    if nom.endswith(".mp3") or nom.endswith(".flac"):
                        type_mime, _ = mimetypes.guess_type(chemin_complet)  # Détermine le type MIME du fichier.
                        if type_mime in ['audio/mpeg', 'audio/flac']:  # Vérifie que le type MIME est valide.
                            return chemin_complet  # Retourne le chemin du fichier trouvé.
        except Exception as e:
            print(f"Une erreur est survenue lors de l'exploration du dossier : {e}")
            return None  # Retourne None en cas d'erreur.
    """
    