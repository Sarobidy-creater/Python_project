#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from mutagen.easyid3 import EasyID3  # Pour les fichiers MP3
from mutagen.flac import FLAC  # Pour les fichiers FLAC
import sys

class EditeurMetadonnees:
    """Classe principale pour gérer les métadonnées audio."""

    def __init__(self, fichier=None):
        self.fichier = fichier
        self.audio = None

    def charger_metadonnees(self):
        """Charge les métadonnées du fichier audio."""
        if not self.fichier:
            raise ValueError("Aucun fichier n'a été fourni.")
        
        try:
            # Détecter le type de fichier
            if self.fichier.endswith(".mp3"):
                self.audio = EasyID3(self.fichier)
            elif self.fichier.endswith(".flac"):
                self.audio = FLAC(self.fichier)
            else:
                raise ValueError("Format non supporté.")

            # Récupérer les métadonnées avec des valeurs par défaut
            return {
                'title': self.audio.get('title', ['Titre inconnu'])[0],
                'artist': self.audio.get('artist', ['Artiste inconnu'])[0],
                'album': self.audio.get('album', ['Album inconnu'])[0],
                'genre': self.audio.get('genre', ['Genre inconnu'])[0],
                'date': self.audio.get('date', ['Date inconnue'])[0],
                'organization': self.audio.get('organization', ['Organisation inconnue'])[0],
            }
        except Exception as e:
            raise RuntimeError(f"Impossible de charger les métadonnées : {e}")

    def sauvegarder_metadonnees(self, nouvelles_metadonnees):
        """Enregistre les nouvelles métadonnées dans le fichier."""
        if not self.audio:
            raise RuntimeError("Aucun fichier audio chargé.")

        try:
            # Mise à jour des métadonnées
            for cle, valeur in nouvelles_metadonnees.items():
                self.audio[cle] = valeur
            self.audio.save()
            print("Les métadonnées ont été mises à jour avec succès.")
        except Exception as e:
            raise RuntimeError(f"Erreur lors de la sauvegarde : {e}")

# --- Fonction console pour l'utilisation sans GUI ---
def interface_console(fichier):
    """Interface en ligne de commande pour modifier les métadonnées."""
    editeur = EditeurMetadonnees(fichier)

    # Chargement des métadonnées
    try:
        metadonnees = editeur.charger_metadonnees()
    except Exception as e:
        print(f"Erreur : {e}")
        sys.exit(1)

    # Afficher les métadonnées actuelles
    print("\nMétadonnées actuelles :")
    for cle, valeur in metadonnees.items():
        print(f"{cle.capitalize()} : {valeur}")

    # Demander à l'utilisateur de saisir de nouvelles valeurs
    print("\nLaissez vide pour conserver la valeur actuelle.")
    nouvelles_metadonnees = {}
    for cle, valeur in metadonnees.items():
        entree = input(f"{cle.capitalize()} [{valeur}] : ").strip()
        if entree:
            nouvelles_metadonnees[cle] = entree
        else:
            nouvelles_metadonnees[cle] = valeur

    # Enregistrer les nouvelles métadonnées
    try:
        editeur.sauvegarder_metadonnees(nouvelles_metadonnees)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage : python dataEdition.py <chemin_du_fichier_audio>")
        sys.exit(1)

    chemin_fichier = sys.argv[1]
    interface_console(chemin_fichier)
