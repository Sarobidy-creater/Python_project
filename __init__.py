# __init__.py

# Initialisation du package
print("Le package Python_project-DataAudio a été initialisé")

# Importer des classes pour un accès facile
# Cela permet de simplifier l'accès à ces classes lors de l'importation du package.
from .library.audioTagExtraction import Extraction  # Importation de la classe Extraction pour extraire les métadonnées audio.
from .library.constitutionPlaylist import Playlist  # Importation de la classe Playlist pour générer des playlists.
from .library.explorationDossier import Explorer  # Importation de la classe Explorer pour explorer les dossiers de fichiers audio.
from .library.ecouterAudio import Ecouter # Importation de la classe Ecouter pour ecouter les dossiers de fichiers audio.
from .gui import Interface # Importation de la
from .cli import Console
from .library.APIQueryType import APIQueryType
from .library.fetcher import Fetcher
from .library.audioMetaEdite import Editer
# from .apiRequest import AudioPlayerApp # Importation de la

# Variables ou constantes du package
version = "1.0.0"  # Déclaration de la version du package, utile pour la gestion des versions.
