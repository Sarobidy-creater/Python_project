#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import mimetypes

class Explorer():

    """
        Explore un dossier et ses sous-dossiers pour afficher les chemins des fichiers audio (MP3 ou FLAC).

        Paramètre :
        - chemin : le chemin du dossier à explorer.

        Retour :
        - Aucun (afficher directement les chemins des fichiers audio trouvés dans la console).
    """
    def explorer_dossier_console(self,chemin):

        # Boucle à travers les dossiers, sous-dossiers et fichiers à partir du chemin donné
        for racine, sous_dossiers, fichiers in os.walk(chemin):
            # Boucle à travers chaque fichier dans la liste des fichiers du dossier courant
            for fichier in fichiers:
                # Construit le chemin complet du fichier
                chemin_complet = os.path.join(racine, fichier)
                nom = os.path.basename(chemin_complet)
                
                # Vérifie si le nom du fichier se termine par '.mp3' ou '.flac' 
                if nom.endswith(".mp3") or nom.endswith(".flac"):
                    # Vérifie le type MIME du fichier
                    type_mime, _ = mimetypes.guess_type(chemin_complet)

                    # Vérifie que le type MIME est valide
                    if type_mime in ['audio/mpeg', 'audio/flac']:
                        # Écrit le chemin complet dans la console
                        print(f"{chemin_complet}\n")


    """
        Explore un dossier et ses sous-dossiers pour afficher les chemins des fichiers audio (MP3 ou FLAC).

        Paramètre :
        - chemin : le chemin du dossier à explorer.

        Retour :
        - Aucun (enregistre directement les chemins des fichiers audio trouvés dans un fichier texte).
    """
    def explorer_dossier_interface(self,chemin) -> str:
        # Chemin du fichier de sortie
        fichier_sortie = 'Python_project\\FichierTemp\\TempFile.txt'

        # Ouvre le fichier de sortie en mode écriture
        with open(fichier_sortie, 'w', encoding='utf-8') as f:
            # Boucle à travers les dossiers, sous-dossiers et fichiers à partir du chemin donné
            for racine, sous_dossiers, fichiers in os.walk(chemin):
                # Boucle à travers chaque fichier dans la liste des fichiers du dossier courant
                for fichier in fichiers:
                    # Construit le chemin complet du fichier
                    chemin_complet = os.path.join(racine, fichier)
                    nom = os.path.basename(chemin_complet)
                    
                    # Vérifie si le nom du fichier se termine par '.mp3' ou '.flac' 
                    if nom.endswith(".mp3") or nom.endswith(".flac"):
                        # Vérifie le type MIME du fichier
                        type_mime, _ = mimetypes.guess_type(chemin_complet)

                        # Vérifie que le type MIME est valide
                        if type_mime in ['audio/mpeg', 'audio/flac']:
                            # Écrit le chemin complet dans le fichier
                            f.write(f"{chemin_complet}\n")
        return fichier_sortie











# Utiliser la fonction en passant le chemin du dossier à explorer
chemin_dossier = r"C:\Users\nelly\Documents\L3-info\S5-2024-2025\S5\PYTHON"

# Appel de la fonction pour enregistrer les chemins des fichiers audio (MP3 ou FLAC).
Explorer().explorer_dossier_console(chemin_dossier)
