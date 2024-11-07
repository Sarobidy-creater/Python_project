#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Importation des modules nécessaires
from mutagen.easyid3 import EasyID3  # Pour lire et écrire les métadonnées ID3 dans les fichiers MP3.
from mutagen.mp3 import MP3  # Pour gérer les fichiers audio MP3 et accéder à leurs métadonnées.
from mutagen.id3 import ID3, APIC  # Pour manipuler les balises ID3 et gérer les images intégrées comme les couvertures d'album.
from mutagen.flac import FLAC, Picture  # Pour travailler avec les fichiers audio FLAC et gérer les images intégrées.
import mimetypes  # Pour déterminer le type MIME des fichiers en fonction de leur extension.
import os  # Pour interagir avec le système de fichiers.


class Explorer():
    """
    Une classe qui permet d'explorer des dossiers et de gérer les fichiers audio.
    """

    def _explorer_dossier_audio(self, chemin, fichier_sortie):
        """
        Explore le dossier spécifié et enregistre les chemins des fichiers audio (MP3, FLAC) dans un fichier.

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
                        audio = None  # Initialise une variable audio à None.

                        # Vérifie l'extension du fichier pour le traitement audio.
                        if chemin_complet.endswith('.mp3'):
                            try:
                                audio = MP3(chemin_complet, ID3=EasyID3)  # Crée un objet MP3 pour lire le fichier.
                            except Exception as e:
                                print(f"Erreur lors de la lecture du fichier MP3 {chemin_complet}: {e}")

                        elif chemin_complet.endswith('.flac'):
                            try:
                                audio = FLAC(chemin_complet)  # Crée un objet FLAC pour lire le fichier.
                            except Exception as e:
                                print(f"Erreur lors de la lecture du fichier FLAC {chemin_complet}: {e}")

                        # Vérifie que l'audio a été chargé correctement.
                        if audio:
                            type_mime, _ = mimetypes.guess_type(chemin_complet)  # Détermine le type MIME du fichier.
                            if type_mime in ['audio/mpeg', 'audio/x-flac']:  # Vérifie que le type MIME est valide.
                                f.write(f"{chemin_complet}\n")  # Écrit le chemin du fichier dans le fichier de sortie.

            return fichier_sortie  # Retourne le chemin du fichier de sortie.
        except Exception as e:
            print(f"Une erreur est survenue lors de l'écriture dans le fichier : {e}")
            return None  # Retourne None en cas d'erreur.

    def explorer_dossier_console(self, chemin_name):
        """
        Explore un dossier donné et affiche les chemins des fichiers audio (MP3, FLAC) dans la console.

        Paramètre :
        - chemin_name : str : Le chemin du dossier à explorer. Utilisez "." pour indiquer le répertoire courant.

        Retourne :
        - None : Cette méthode n'a pas de retour, elle affiche les chemins dans la console.
        """
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
                            print(f"{chemin_complet}\n")  # Affiche le chemin du fichier dans la console.
        except Exception as e:
            print(f"Une erreur est survenue lors de l'exploration du dossier : {e}")

    def explorer_dossier_interface(self, chemin) -> str:
        """
        Explore un dossier donné et enregistre les chemins des fichiers audio (MP3, FLAC) dans un fichier temporaire.

        Paramètre :
        - chemin : str : Le chemin du dossier à explorer.

        Retourne :
        - str : Le chemin du fichier temporaire contenant les chemins des fichiers audio, ou None en cas d'erreur.
        """
        fichier_sortie = os.path.abspath(r'FichierTemp\TempFile.txt')
        print("fichier_sortie**********************************************************************")
        print(fichier_sortie)
        print("**********************************************************************") 
         
        return self._explorer_dossier_audio(chemin, fichier_sortie)  # Appelle la méthode d'exploration des fichiers audio.

    def explorer_dossier(self, chemin_name):
        """
        Explore un dossier donné et retourne le chemin du premier fichier audio (MP3, FLAC) trouvé.

        Paramètre :
        - chemin_name : str : Le chemin du dossier à explorer. Utilisez "." pour indiquer le répertoire courant.

        Retourne :
        - str : Le chemin complet du premier fichier audio trouvé, ou None en cas d'erreur.
        """
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

    def explorer_dossier_gui(self, chemin) -> str:
        """
        Explore un dossier donné et enregistre les chemins des fichiers audio (MP3, FLAC) dans un fichier temporaire.

        Paramètre :
        - chemin : str : Le chemin du dossier à explorer.

        Retourne :
        - str : Le chemin du fichier temporaire contenant les chemins des fichiers audio, ou None en cas d'erreur.
        """
        fichier_sortie = os.path.abspath(r'Python_project-DataAudio\FichierTemp\TempFile.txt')  
        return self._explorer_dossier_audio(chemin, fichier_sortie)  # Appelle la méthode d'exploration des fichiers audio.
