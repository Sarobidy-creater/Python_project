#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from lxml import etree
import os


"""
    Crée un fichier XSPF vide dans le dossier spécifié.

    Paramètre :
    - Aucun

    Retour :
    - Le chemin du fichier XSPF créé.
"""
def creerUnFichierxspf():  
    dossier = 'Python_project\\Playlist'
    # Vérifier si le dossier existe, sinon le créer
    if not os.path.exists(dossier):
        os.makedirs(dossier)

    # Création du fichier et écriture
    nom = os.path.join(dossier, 'fichierPlaylist.xspf')  # Spécifier le chemin complet
    fichier = open(nom, 'w')  # Ouverture du fichier en écriture

    # Écriture de plusieurs lignes dans le fichier
    fichier.write("<?xml version='1.0' encoding='UTF-8'?>\n""<playlist version=\"1\" xmlns=\"http://xspf.org/ns/0/\"></playlist>\n")

    fichier.close()  # Fermeture du fichier après écriture

    varfic = nom.replace("\\", "/")
    return varfic


"""
    Supprime le fichier XSPF spécifié.

    Paramètre :
    - chemin : Le chemin du fichier XSPF à supprimer.

    Retour :
    - Aucun
"""
def deleteUnFichierxspf(chemin : str): 
    os.remove(chemin)


"""
    Écrit une nouvelle piste dans le fichier XSPF existant.

    Paramètres :
    - cheminFichier : Le chemin du fichier XSPF à modifier.
    - cheminAudio : Le chemin du fichier audio à ajouter à la playlist.
    - titrePlay : Le titre de la chanson à ajouter.

    Retour :
    - Aucun
"""
def ecritureFichierxspf(cheminFichier: str, cheminAudio: str, titrePlay: str):
    """
    Parse le fichier .xspf existant
    """
    # Charge et analyse le fichier XML à partir du chemin donné
    tree = etree.parse(cheminFichier) 
    # Récupère l'élément racine du document XML (la balise <playlist>) 
    root = tree.getroot()  

    """
    Crée de nouveaux éléments (par exemple, une liste de pistes avec une seule piste)
    """
    # Crée un nouvel élément <trackList> qui contiendra les pistes
    tracklist = etree.Element("trackList") 
    # Crée un nouvel élément <track> pour une piste spécifique 
    track = etree.Element("track")  

    """
    Définit les détails de la piste
    """
    # Crée un élément <location> pour spécifier l'emplacement du fichier audio
    location = etree.Element("location")  
    # Remplace les antislashs par des barres obliques pour le chemin audio
    cheminVar = cheminAudio.replace("\\", "/")
    # Définit l'URL ou le chemin du fichier audio pour cette piste
    location.text = f"file:///{cheminVar}"  
    # Crée un élément <title> pour indiquer le titre de la chanson
    title = etree.Element("title") 
    # Définit le titre de la chanson 
    title.text = titrePlay 

    """
    Ajoute les détails de la piste à l'élément <track>
    """
    # Ajoute l'élément <location> comme enfant de <track>
    track.append(location)  
    # Ajoute l'élément <title> comme enfant de <track>
    track.append(title)  
    # Ajoute l'élément <track> à l'élément <trackList>
    tracklist.append(track)  

    """
    Ajoute la liste de pistes à la racine du document XML
    """
    # Ajoute l'élément <trackList> à l'élément racine <playlist>
    root.append(tracklist)  

    """
    Écrit le fichier XML mis à jour
    """
    # Ouvre le fichier en mode binaire (écriture)
    with open(cheminFichier, 'wb') as f:  
        # Écrit le contenu XML dans le fichier avec un formatage lisible, la déclaration XML et un encodage UTF-8
        f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='UTF-8'))




"""
Exemple d'utilisation
"""

# Crée d'abord le fichier XSPF vide
chemin_fichier = creerUnFichierxspf() 

# Définit le chemin vers le fichier audio à ajouter à la playlist
cheminA = r"c:\Chemin\vers\fichier"

# Demande à l'utilisateur de fournir un titre pour la playlist
titrePlay = str(input("Donner un titre à votre playlist : "))  

# Ajoute du contenu au fichier XSPF
# Appelle la fonction pour ajouter une piste à la playlist
ecritureFichierxspf(chemin_fichier, cheminA, titrePlay)  
