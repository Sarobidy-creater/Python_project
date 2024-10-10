#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Importation des modules nécessaires
import argparse  # Importe la bibliothèque argparse pour gérer les arguments en ligne de commande
import os  # Importe la bibliothèque os pour interagir avec le système de fichiers
from audioTagExtraction import Extraction  # Importe la classe Extraction du module audioTagExtraction pour extraire les métadonnées audio
from constitutionPlaylist import Playlist  # Importe la classe Playlist du module constitutionPlaylist pour générer des playlists
from explorationDossier import Explorer  # Importe la classe Explorer du module explorationDossier pour explorer les dossiers
from ecouterAudio import Ecouter # Importe la classe Ecouter du module ecouterAudio pour lire un fichier audio mp3 ou flac dans la console


"""
    Une classe qui gère les interactions en ligne de commande pour la gestion des fichiers musicaux.
"""
class Console:
    

    """
        Fonction qui affiche les instructions d'utilisation du programme.

        Paramètre :
        - None

        Retour :
        - None : Cette méthode n'a pas de retour, elle affiche l'aide dans la console.
    """
    def afficher_aide(self):
        aide = """
        Usage: python3 cli.py [OPTIONS]
        Options:
            -h, --help          Afficher cette aide
            -f, --file FILE     Spécifier un fichier MP3 ou FLAC pour extraire les métadonnées
            -d, --directory DIR Spécifier un dossier pour analyser et générer une playlist
            -o, --output FILE   Spécifier un fichier de sortie XSPF pour la playlist générée
            -l, --listen FILE   Spécifier un fichier audio pour lire dans la console
        """
        print(aide)  # Affiche le texte d'aide défini ci-dessus


    """
        Fonction principale qui gère l'analyse des arguments en ligne de commande et exécute les opérations appropriées.

        Paramètre :
        - None

        Retour :
        - None : Cette méthode n'a pas de retour, elle exécute les actions basées sur les arguments fournis.
    """
    def main(self):
        # Configuration de l'analyseur d'arguments en ligne de commande avec argparse
        parser = argparse.ArgumentParser(description='Gestionnaire de fichiers musicaux CLI')
        # Ajout de l'argument pour spécifier un fichier audio
        parser.add_argument('-f', '--file', type=str, help='Fichier pour afficher les métadonnées')
        # Ajout de l'argument pour spécifier un dossier à analyser
        parser.add_argument('-d', '--directory', type=str, help='Dossier à analyser pour les fichiers audio')
        # Ajout de l'argument pour spécifier un fichier de sortie pour la playlist générée
        parser.add_argument('-o', '--output', type=str, help='Fichier de sortie pour la playlist')
        # Ajout de l'argument pour spécifier un fichier audio à lire dans la console
        parser.add_argument('-l', '--listen', type=str, help='Fichier audio à lire')

        # Analyse les arguments fournis par l'utilisateur
        args = parser.parse_args()

        # Création des instances des classes Extraction, Explorer, et Playlist nécessaires pour les différentes fonctionnalités
        extraction = Extraction()  # Instance pour l'extraction des métadonnées audio
        explorer = Explorer()  # Instance pour explorer les dossiers
        playlist = Playlist()  # Instance pour générer une playlist
        ecouter = Ecouter() # Instance pour ecouter les audios mp3 et flac

        # Vérification si aucun argument n'a été fourni (valeurs None ou vides)
        if not any(vars(args).values()):
            self.afficher_aide()  # Si aucun argument n'est fourni, afficher l'aide
            return  # Arrêter l'exécution du programme

        # Assurer que l'utilisateur ne spécifie pas à la fois un fichier et un dossier, car c'est mutuellement exclusif
        if args.directory and args.file:
            print("Erreur: Utilisez uniquement une option '-d' ou '-f', pas les deux.")  # Message d'erreur si les deux sont fournis
            return  # Arrêter l'exécution du programme

        try:
            # Si un dossier est fourni, procéder à son analyse
            if args.directory:
                # Vérifier si le dossier existe
                if not os.path.isdir(args.directory):
                    # Si le dossier n'existe pas, lever une exception
                    raise FileNotFoundError(f"Le dossier '{args.directory}' n'existe pas ou n'est pas accessible.")
                print(f"Analyse du dossier : {args.directory}")  # Afficher le message indiquant l'analyse du dossier
                explorer.explorer_dossier_console(args.directory)  # Appel de la méthode pour explorer le dossier

            # Si un fichier est fourni, extraire et afficher ses métadonnées
            if args.file:
                # Vérifier si le fichier existe
                if not os.path.isfile(args.file):
                    # Si le fichier n'existe pas, lever une exception
                    raise FileNotFoundError(f"Le fichier '{args.file}' n'existe pas ou n'est pas accessible.")
                print(f"Affichage des métadonnées pour le fichier : {args.file}")  # Message indiquant le fichier analysé
                extraction.audio_extraire_et_afficher_tag(args.file)  # Extraire et afficher les métadonnées du fichier

            # Si un dossier et un fichier de sortie sont fournis, générer une playlist
            if args.directory and args.output:
                print(f"Génération de la playlist dans le fichier : {args.output}")  # Message indiquant la génération de la playlist
                playlist.ecritureFichierxspf(args.directory, args.output)  # Appel de la méthode pour écrire la playlist dans le fichier

        # Gestion des exceptions si le fichier ou dossier n'existe pas
        except FileNotFoundError as e:
            print(f"Erreur: {e}")  # Affiche un message d'erreur si le fichier/dossier est introuvable

        # Gestion des erreurs de permission lors de l'accès à des fichiers ou dossiers
        except PermissionError as e:
            print(f"Erreur de permission: {e}")  # Affiche un message si l'utilisateur n'a pas les permissions nécessaires

        # Gestion d'autres erreurs imprévues
        except Exception as e:
            print(f"Une erreur inattendue s'est produite : {e}")  # Affiche un message pour toute autre erreur inattendue


# Vérifie si le fichier est exécuté en tant que script principal
if __name__ == "__main__":
    console = Console()  # Crée une instance de la classe Console
    console.main()  # Exécute la méthode main pour démarrer le programme
