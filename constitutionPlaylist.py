#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from lxml import etree
import os
import datetime
from explorationDossier import Explorer

class Playlist():

    """
        Crée un fichier XSPF vide dans le dossier spécifié.

        Paramètre :
        - Aucun

        Retour :
        - Le chemin du fichier XSPF créé.
    """
    def creerUnFichierxspf(self):  
        dossier = 'Python_project\\Playlist'
        try:
            # Vérifier si le dossier existe, sinon le créer
            os.makedirs(dossier, exist_ok=True)

            # Spécifier le chemin complet
            nom = os.path.join(dossier, 'fichierPlaylist.xspf')

            # Écrire le contenu initial du fichier
            with open(nom, 'w', encoding='utf-8') as fichier:
                fichier.write("<?xml version='1.0' encoding='UTF-8'?>\n")
                fichier.write("<playlist version=\"1\" xmlns=\"http://xspf.org/ns/0/\"></playlist>\n")

            return nom.replace("\\", "/")
        
        except OSError as e:
            print(f"Erreur lors de la création du fichier : {e}")
            return None

    
    """
        Crée un fichier XSPF vide dans le dossier spécifié.

        Paramètre :
        - Aucun

        Retour :
        - Le chemin du fichier XSPF créé.
    """
    def creation_specifique_fichier_xspf(self, fichier_name: str):  
        # Utilisation de 'os.path.join' pour construire le chemin
        dossier = os.path.abspath('Playlist')  # Utilisation de '/' au lieu de '\\'
        
        # Vérifier si le dossier existe et le créer s'il n'existe pas
        if not os.path.exists(dossier):
            os.makedirs(dossier)
        # print(f"Analyse du dossier : {dossier}")
        # print(f"Analyse du fichier_name : {fichier_name}")

        chem = os.path.join(dossier, fichier_name)  # Spécifier le chemin complet
        # print(f"Analyse du chem : {chem}")
        nom = os.path.abspath(chem)
        # print(f"Analyse du nom : {nom}")
        
        # Utilisation de 'with' pour gérer le fichier, ce qui assure une bonne fermeture
        with open(nom, 'w', encoding='utf-8') as fichier:  # Ouverture du fichier en écriture
            # Écriture de plusieurs lignes dans le fichier
            fichier.write("<?xml version='1.0' encoding='UTF-8'?>\n")
            fichier.write("<playlist version=\"1\" xmlns=\"http://xspf.org/ns/0/\"></playlist>\n")

        varfic = nom.replace("\\", "/")
        return varfic


    def ecritureFichierxspf(self,dossier_muxic: str,out_Fichier_nom: str):
        chemin_file = None
        if out_Fichier_nom == None: 
            chemin_file = self.creerUnFichierxspf()
        else:
            chemin_file = self.creation_specifique_fichier_xspf(out_Fichier_nom)
        
        # print(f"Analyse du chemin_file : {chemin_file}")
        
            
        """
        Parse le fichier .xspf existant
        """
        # Charge et analyse le fichier XML à partir du chemin donné
        tree = etree.parse(chemin_file) 
        # Récupère l'élément racine du document XML (la balise <playlist>) 
        root = tree.getroot() 
        # Crée un élément <title> pour indiquer le titre de la chanson
        date = etree.Element("date") 
        # Définit le titre de la chanson 
        date.text = datetime.datetime.today().strftime('%d-%m-%y %H:%M:%S')  
        # Ajoute l'élément <title> comme enfant de <track>
        root.append(date) 

        """
        Crée de nouveaux éléments (par exemple, une liste de pistes avec une seule piste)
        """
        # Crée un nouvel élément <trackList> qui contiendra les pistes
        tracklist = etree.Element("trackList") 
        # 
        explorer = Explorer()
        # 
        d_save = os.path.abspath(f"{dossier_muxic}") 
        dossier_save = d_save.replace("\\", "/")
        # print(f"Analyse du dossier_save : {dossier_save}")

        # lire_fiche =explorer.explorer_dossier_interface(dossier_save)
        # Chemin du fichier  temp
        fichier_lire_chemin = explorer.explorer_dossier_interface(dossier_save)
        # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        # print(f"Analyse du fichier_lire_chemin : {fichier_lire_chemin}")
        # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

        with open(fichier_lire_chemin, 'r', encoding='utf-8') as f:
            for ligne in f:
                chemin_Audi = ligne.strip()
                # Crée un nouvel élément <track> pour une piste spécifique 
                track = etree.Element("track")  
                """
                Définit les détails de la piste
                """
                # Crée un élément <location> pour spécifier l'emplacement du fichier audio
                location = etree.Element("location")  
                # Obtenir le chemin absolu du fichier
                cheminAudio = os.path.abspath(chemin_Audi)
                # Remplace les antislashs par des barres obliques pour le chemin audio
                cheminVar = cheminAudio.replace("\\", "/")
                # Définit l'URL ou le chemin du fichier audio pour cette piste
                location.text = f"file:///{cheminVar}" 
                # Ajoute l'élément <location> comme enfant de <track>
                track.append(location)  
                # Ajoute l'élément <title> comme enfant de <track>
                #track.append(title)  
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
        with open(chemin_file, 'wb') as f:  
            # Écrit le contenu XML dans le fichier avec un formatage lisible, la déclaration XML et un encodage UTF-8
            f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='UTF-8'))



# out_cheminFichier = "muxic"
# in_cheminFichier = "MyoooooPlaylist.xspf"

# playlist = Playlist()

# playlist.ecritureFichierxspf(out_cheminFichier,in_cheminFichier)





