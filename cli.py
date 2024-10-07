import argparse
from audioTagExtraction import Extraction
from constitutionPlaylist import Playlist
from explorationDossier import Explorer

class Console:
    def afficher_aide(self):
        aide = """
        Usage: python3 cli.py [OPTIONS]
        Options:
            -h, --help          Afficher cette aide
            -f, --file FILE     Spécifier un fichier MP3 ou FLAC pour extraire les métadonnées
            -d, --directory DIR Spécifier un dossier pour analyser et générer une playlist
            -o, --output FILE   Spécifier un fichier de sortie XSPF pour la playlist générée
        """
        print(aide)

    def main(self):
        parser = argparse.ArgumentParser(description='Gestionnaire de fichiers musicaux CLI')
        parser.add_argument('-f', '--file', type=str, help='Fichier pour afficher les métadonnées')
        parser.add_argument('-d', '--directory', type=str, help='Dossier à analyser pour les fichiers audio')
        parser.add_argument('-o', '--output', type=str, help='Fichier de sortie pour la playlist')

        args = parser.parse_args()

        # Création des instances nécessaires
        extraction = Extraction()
        explorer = Explorer()
        playlist = Playlist()

        # Aucun argument fourni
        if not any(vars(args).values()):
            self.afficher_aide()
            return

        # Assurer des arguments exclusifs pour file et directory
        if args.directory and args.file:
            print("Erreur: Utilisez uniquement une option '-d' ou '-f', pas les deux.")
            return

        # Analyse du dossier
        if args.directory:
            print(f"Analyse du dossier : {args.directory}")
            explorer.explorer_dossier_console(args.directory)

        # Extraction de métadonnées d'un fichier
        if args.file:
            print(f"Affichage des métadonnées pour le fichier : {args.file}")
            extraction.audio_extraire_et_afficher_tag(args.file)

        # Génération de playlist avec fichier de sortie
        if args.directory and args.output:
            print(f"Génération de la playlist dans le fichier : {args.output}")
            playlist.ecritureFichierxspf(args.directory, args.output)

if __name__ == "__main__":
    console = Console()
    console.main()
