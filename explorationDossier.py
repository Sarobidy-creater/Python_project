#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import mimetypes

"""
    Explore un dossier et ses sous-dossiers pour afficher les chemins des fichiers audio (MP3 ou FLAC).

    Paramètre :
    - chemin : le chemin du dossier à explorer.

    Retour :
    - Aucun (affiche directement les chemins des fichiers audio trouvés).
"""
def explorer_dossier(chemin):
    print(f"\n\nDossier racine : {chemin}\n")

    # Boucle à travers les dossiers, sous-dossiers et fichiers à partir du chemin donné
    for racine, sous_dossiers, fichiers in os.walk(chemin):
        
        # Boucle à travers chaque fichier dans la liste des fichiers du dossier courant
        for fichier in fichiers:

            # Construit le chemin complet du fichier en combinant le chemin du dossier courant et le nom du fichier
            chemin_complet = os.path.join(racine, fichier)
            nom = os.path.basename(chemin_complet)
            
            # Vérifie si le nom du fichier se termine par '.mp3' ou '.flac' 
            if nom.endswith(".mp3") or nom.endswith(".flac"):
                
                # Vérifie le type MIME du fichier
                type_mime, _ = mimetypes.guess_type(chemin_complet)

                # Vérifie même si un fichier a l'extension correcte, il doit également être de type audio valide
                if type_mime in ['audio/mpeg', 'audio/flac']:
                    print(f" - {chemin_complet}")


# Utiliser la fonction en passant le chemin du dossier à explorer
chemin_dossier = r"c:\Chemin\vers\fichier"

# Appel de la fonction pour afficher les chemins des fichiers audio (MP3 ou FLAC).
explorer_dossier(chemin_dossier)
