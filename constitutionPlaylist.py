#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Importation des modules nécessaires
from lxml import etree  # Pour manipuler les fichiers XML
import os  # Importe la bibliothèque os pour interagir avec le système de fichiers
import datetime  # Pour gérer les dates et heures
from explorationDossier import Explorer  # Importe la classe Explorer du module explorationDossier pour explorer les dossiers


"""
    Une classe qui gère la création et l'écriture de fichiers de playlist au format XSPF.
"""
class Playlist():


    """
        Fonction qui crée un fichier XSPF par défaut dans le dossier spécifié.

        Paramètre :
        - Aucun

        Retour :
        - str : Le chemin du fichier XSPF créé, ou None en cas d'erreur.
    """
    def creerUnFichierxspf(self):  
        dossier = 'Python_project/Playlist'  # Définition du chemin du dossier où le fichier sera créé
        try:
            # Vérifier si le dossier existe, sinon le créer
            os.makedirs(dossier, exist_ok=True)

            # Spécifier le chemin complet du fichier XSPF
            nom = os.path.join(dossier, 'maPlaylist.xspf')

            # Écrire le contenu initial du fichier
            with open(nom, 'w', encoding='utf-8') as fichier:
                # Écriture de la déclaration XML et de la balise <playlist> dans le fichier
                fichier.write("<?xml version='1.0' encoding='UTF-8'?>\n")
                fichier.write("<playlist version=\"1\" xmlns=\"http://xspf.org/ns/0/\"></playlist>\n")

            # Retourner le chemin du fichier créé avec les barres obliques correctes
            return nom.replace("\\", "/")
        
        except OSError as e:
            # Gestion des erreurs lors de la création du dossier ou du fichier
            print(f"Erreur lors de la création du fichier : {e}")
            return None


    """
        Fonction qui crée un fichier XSPF avec un nom spécifié dans le dossier de playlists.

        Paramètre :
        - fichier_name : str : Le nom du fichier XSPF à créer.

        Retour :
        - str : Le chemin du fichier XSPF créé, ou None en cas d'erreur.
    """
    def creation_specifique_fichier_xspf(self, fichier_name: str):  
        # Utilisation du chemin absolu pour le dossier
        dossier = os.path.abspath('Playlist') 
        
        try:

            # Spécifier le chemin complet du fichier
            chem = os.path.join(dossier, fichier_name) 
            nom = os.path.abspath(chem)  # Obtenir le chemin absolu
            
            # Utilisation de 'with' pour gérer le fichier, ce qui assure une bonne fermeture
            with open(nom, 'w', encoding='utf-8') as fichier:
                # Écriture de la déclaration XML et de la balise <playlist>
                fichier.write("<?xml version='1.0' encoding='UTF-8'?>\n")
                fichier.write("<playlist version=\"1\" xmlns=\"http://xspf.org/ns/0/\"></playlist>\n")

            # Retourner le chemin du fichier créé avec les barres obliques correctes
            return nom.replace("\\", "/")
        
        except OSError as e:
            # Gestion des erreurs lors de la création du fichier spécifique
            print(f"Erreur lors de la création du fichier spécifique : {e}")
            return None


    """
        Fonction qui écrit les informations d'une playlist dans un fichier XSPF.

        Paramètre :
        - dossier_music : str : Le chemin du dossier contenant les fichiers musicaux.
        - out_Fichier_nom : str : Le nom du fichier de sortie XSPF (peut être None pour un fichier par défaut).

        Retour :
        - None : Cette méthode n'a pas de retour, elle effectue des opérations d'écriture dans un fichier.
    """
    def ecritureFichierxspf(self, dossier_music: str, out_Fichier_nom: str):
        try:
            chemin_file = None  # Initialisation de la variable pour le chemin du fichier
            # Si aucun nom de fichier de sortie n'est donné, créer un fichier par défaut
            if out_Fichier_nom is None: 
                chemin_file = self.creerUnFichierxspf()
            else:
                chemin_file = self.creation_specifique_fichier_xspf(out_Fichier_nom)
            

            # Charger et analyser le fichier XML à partir du chemin donné
            tree = etree.parse(chemin_file)  # Parser le fichier XML
            root = tree.getroot()  # Récupérer l'élément racine du document XML (la balise <playlist>)
            
            # Créer un élément <date> pour indiquer la date actuelle
            date = etree.Element("date") 
            date.text = datetime.datetime.today().strftime('%d-%m-%y %H:%M:%S')  # Définir le texte de la date
            root.append(date)  # Ajouter l'élément <date> à l'élément racine

            # Créer un nouvel élément <trackList> pour contenir les pistes
            tracklist = etree.Element("trackList") 
            explorer = Explorer()  # Créer une instance de la classe Explorer
            d_save = os.path.abspath(dossier_music)  # Obtenir le chemin absolu du dossier de musique
            dossier_save = d_save.replace("\\", "/")  # Remplacer les antislashs par des barres obliques
            

            # Obtenir le chemin du fichier à lire à partir de l'exploration du dossier
            fichier_lire_chemin = explorer.explorer_dossier_interface(dossier_save)

            # Ouvrir le fichier pour lire les chemins des fichiers audio
            with open(fichier_lire_chemin, 'r', encoding='utf-8') as f:
                for ligne in f:
                    chemin_Audi = ligne.strip()  # Supprimer les espaces autour du chemin
                    track = etree.Element("track")  # Créer un nouvel élément <track> pour chaque piste
                    location = etree.Element("location")  # Créer un élément <location> pour spécifier l'emplacement
                    cheminAudio = os.path.abspath(chemin_Audi)  # Obtenir le chemin absolu du fichier audio
                    cheminVar = cheminAudio.replace("\\", "/")  # Remplacer les antislashs par des barres obliques
                    location.text = f"file:///{cheminVar}"  # Définir l'URL ou le chemin du fichier audio
                    track.append(location)  # Ajouter l'élément <location> à <track>
                    tracklist.append(track)  # Ajouter l'élément <track> à <trackList> 

            # Ajouter la liste de pistes à l'élément racine <playlist>
            root.append(tracklist)  

            # Ouvrir le fichier en mode binaire pour l'écriture
            with open(chemin_file, 'wb') as f:  
                # Écrire le contenu XML dans le fichier avec un formatage lisible, la déclaration XML et un encodage UTF-8
                f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
        
        except etree.XMLSyntaxError as e:
            # Gestion des erreurs de parsing XML
            print(f"Erreur de parsing XML : {e}")
        except FileNotFoundError as e:
            # Gestion des erreurs d'ouverture de fichier non trouvé
            print(f"Erreur lors de l'ouverture du fichier : {e}")
        except OSError as e:
            # Gestion des erreurs lors de l'écriture dans le fichier
            print(f"Erreur lors de l'écriture dans le fichier : {e}")
        except Exception as e:
            # Gestion de toutes les autres erreurs inattendues
            print(f"Une erreur inattendue s'est produite : {e}")


    """
        Fonction qui crée un fichier XSPF par défaut dans le dossier spécifié.

        Paramètre :
        - Aucun

        Retour :
        - str : Le chemin du fichier XSPF créé, ou None en cas d'erreur.
    """
    def defaultUnFichierxspf(self):  
        dossier = 'Python_project/Playlist'  # Définition du chemin du dossier où le fichier sera créé
        try:
            # Vérifier si le dossier existe, sinon le créer
            os.makedirs(dossier, exist_ok=True)

            # Spécifier le chemin complet du fichier XSPF
            nom = os.path.join(dossier, 'maPlaylist.xspf')

            # Écrire le contenu initial du fichier
            with open(nom, 'w', encoding='utf-8') as fichier:
                # Écriture de la déclaration XML et de la balise <playlist> dans le fichier
                fichier.write("<?xml version='1.0' encoding='UTF-8'?>\n")
                fichier.write("<playlist version=\"1\" xmlns=\"http://xspf.org/ns/0/\"></playlist>\n")

            # Retourner le chemin du fichier créé avec les barres obliques correctes
            return nom.replace("\\", "/")
        
        except OSError as e:
            # Gestion des erreurs lors de la création du dossier ou du fichier
            print(f"Erreur lors de la création du fichier : {e}")
            return None


    """
        Fonction qui crée un fichier XSPF avec un nom spécifié dans le dossier de playlists.

        Paramètre :
        - fichier_name : str : Le nom du fichier XSPF à créer.

        Retour :
        - str : Le chemin du fichier XSPF créé, ou None en cas d'erreur.
    """
    def specifiqueName_fichier_xspf(self, fichier_name: str):  
        # Utilisation du chemin absolu pour le dossier
        dossier = os.path.abspath('Python_project/Playlist')  
        
        try:
            # Vérifier si le dossier existe et le créer s'il n'existe pas
            if not os.path.exists(dossier):
                os.makedirs(dossier)
            fichier_name = f"{fichier_name}.xspf"
            # Spécifier le chemin complet du fichier
            chem = os.path.join(dossier, fichier_name) 
            nom = os.path.abspath(chem)  # Obtenir le chemin absolu
            
            # Utilisation de 'with' pour gérer le fichier, ce qui assure une bonne fermeture
            with open(nom, 'w', encoding='utf-8') as fichier:
                # Écriture de la déclaration XML et de la balise <playlist>
                fichier.write("<?xml version='1.0' encoding='UTF-8'?>\n")
                fichier.write("<playlist version=\"1\" xmlns=\"http://xspf.org/ns/0/\"></playlist>\n")

            # Retourner le chemin du fichier créé avec les barres obliques correctes
            return nom.replace("\\", "/")
        
        except OSError as e:
            # Gestion des erreurs lors de la création du fichier spécifique
            print(f"Erreur lors de la création du fichier spécifique : {e}")
            return None


    """
        Fonction qui écrit les informations d'une playlist dans un fichier XSPF.

        Paramètre :
        - dossier_music : str : Le chemin du dossier contenant les fichiers musicaux.
        - out_Fichier_nom : str : Le nom du fichier de sortie XSPF (peut être None pour un fichier par défaut).

        Retour :
        - None : Cette méthode n'a pas de retour, elle effectue des opérations d'écriture dans un fichier.
    """
    def gui_ecritureFichierxspf(self, dossier_music: str, out_Fichier_nom: str):
        chemin_file = None  # Initialisation de la variable pour le chemin du fichier
        try:
            # Si aucun nom de fichier de sortie n'est donné, créer un fichier par défaut
            if out_Fichier_nom is None: 
                chemin_file = self.defaultUnFichierxspf()
            else:
                chemin_file = self.specifiqueName_fichier_xspf(out_Fichier_nom)

            # Charger et analyser le fichier XML à partir du chemin donné
            tree = etree.parse(chemin_file)  # Parser le fichier XML
            root = tree.getroot()  # Récupérer l'élément racine du document XML (la balise <playlist>)
            
            # Créer un élément <date> pour indiquer la date actuelle
            date = etree.Element("date") 
            date.text = datetime.datetime.today().strftime('%d-%m-%y %H:%M:%S')  # Définir le texte de la date
            root.append(date)  # Ajouter l'élément <date> à l'élément racine

            # Créer un nouvel élément <trackList> pour contenir les pistes
            tracklist = etree.Element("trackList") 
            explorer = Explorer()  # Créer une instance de la classe Explorer
            d_save = os.path.abspath(dossier_music)  # Obtenir le chemin absolu du dossier de musique
            dossier_save = d_save.replace("\\", "/")  # Remplacer les antislashs par des barres obliques

            # Obtenir le chemin du fichier à lire à partir de l'exploration du dossier
            fichier_lire_chemin = explorer.explorer_dossier_gui(dossier_save) 

            # Ouvrir le fichier pour lire les chemins des fichiers audio
            with open(fichier_lire_chemin, 'r', encoding='utf-8') as f:
                for ligne in f:
                    chemin_Audi = ligne.strip()  # Supprimer les espaces autour du chemin
                    track = etree.Element("track")  # Créer un nouvel élément <track> pour chaque piste
                    location = etree.Element("location")  # Créer un élément <location> pour spécifier l'emplacement
                    cheminAudio = os.path.abspath(chemin_Audi)  # Obtenir le chemin absolu du fichier audio
                    cheminVar = cheminAudio.replace("\\", "/")  # Remplacer les antislashs par des barres obliques
                    location.text = f"file:///{cheminVar}"  # Définir l'URL ou le chemin du fichier audio
                    track.append(location)  # Ajouter l'élément <location> à <track>
                    tracklist.append(track)  # Ajouter l'élément <track> à <trackList> 

            # Ajouter la liste de pistes à l'élément racine <playlist>
            root.append(tracklist)  

            # Ouvrir le fichier en mode binaire pour l'écriture
            with open(chemin_file, 'wb') as f:  
                # Écrire le contenu XML dans le fichier avec un formatage lisible, la déclaration XML et un encodage UTF-8
                f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='UTF-8'))
        
        except etree.XMLSyntaxError as e:
            # Gestion des erreurs de parsing XML
            print(f"Erreur de parsing XML : {e}")
        except FileNotFoundError as e:
            # Gestion des erreurs d'ouverture de fichier non trouvé
            print(f"Erreur lors de l'ouverture du fichier : {e}")
        except OSError as e:
            # Gestion des erreurs lors de l'écriture dans le fichier
            print(f"Erreur lors de l'écriture dans le fichier : {e}")
        except Exception as e:
            # Gestion de toutes les autres erreurs inattendues
            print(f"Une erreur inattendue s'est produite : {e}")
