import argparse
import os
from pathlib import Path
from audioTagExtraction import Extraction
from constitutionPlaylist import Playlist
from explorationDossier import Explorer

class Console():
    @staticmethod
    def main():
        parser = argparse.ArgumentParser(description='Gestionnaire de fichiers musicaux CLI')
        parser.add_argument('-d', '--dossier', type=str, help='Dossier à analyser pour les fichiers audio')
        parser.add_argument('-f', '--fichier', type=str, help='Fichier pour afficher les métadonnées')
        parser.add_argument('-o', '--sortie', type=str, help='Fichier de sortie pour la playlist')
        
        args = parser.parse_args()

        if not any(vars(args).values()):
            parser.print_help()
            return

        if args.dossier:
            print(f"Analyse du dossier : {args.dossier}")
            Explorer.explorer_dossier_console(args.dossier)

        if args.fichier:
            print(f"Affichage des métadonnées pour le fichier : {args.fichier}")
            Extraction.audio_extraire_et_afficher_tag(args.fichier)

        if args.dossier and args.sortie:
            print(f"Génération de la playlist depuis {args.dossier} et sauvegarde dans {args.sortie}")
            Playlist.ecritureFichierxspf(args.dossier, args.sortie)

    if __name__ == '__main__':
        main()
