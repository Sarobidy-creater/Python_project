# __init__.py

# Initialisation du package
print("Le package Python_project a été initialisé")

# Importer des classes pour un accès facile
# Cela permet de simplifier l'accès à ces classes lors de l'importation du package.
from .audioTagExtraction import Extraction  # Importation de la classe Extraction pour extraire les métadonnées audio.
from .constitutionPlaylist import Playlist  # Importation de la classe Playlist pour générer des playlists.
from .explorationDossier import Explorer  # Importation de la classe Explorer pour explorer les dossiers de fichiers audio.

# Variables ou constantes du package
version = "1.0.0"  # Déclaration de la version du package, utile pour la gestion des versions.
