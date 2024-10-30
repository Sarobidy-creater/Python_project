from mutagen.mp3 import MP3
from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3, ID3NoHeaderError, APIC, TIT2, TPE1, TALB, TCON
import mimetypes

class Editer:
    def creation_meta_donnees(self, titre:str, artiste:str, album:str, genre:str, ladate:str, organisation:str):
        meta_donnees = {
            "title": titre,
            "artist": artiste,
            "album": album,
            "genre": genre,
            "date": ladate,
            "organisation": organisation
        }
        return meta_donnees

    def afficher_et_modifier_metadata(self, chemin_audio:str, chemin_image:str, titre:str, artiste:str, album:str, genre:str, ladate:str, organisation:str):
        """Détecte le format du fichier et gère l'affichage et la modification des métadonnées."""
        meta_donnees = self.creation_meta_donnees(titre, artiste, album, genre, ladate, organisation)
        if chemin_audio.endswith(".mp3"):
            self._afficher_et_modifier_meta_mp3(chemin_audio,meta_donnees,chemin_image)
        elif chemin_audio.endswith(".flac"):
            self._afficher_et_modifier_meta_flac(chemin_audio,meta_donnees,chemin_image)
        else:
            print("Format audio non pris en charge.")
    
    def _afficher_et_modifier_meta_mp3(self, chemin_audio:str, meta_donnees:str, chemin_image:str):
        """Affiche et modifie les métadonnées d'un fichier MP3."""
        try:
            audio = MP3(chemin_audio, ID3=ID3)
        except ID3NoHeaderError:
            audio = MP3(chemin_audio)
            audio.add_tags()

        # Afficher les métadonnées existantes
        print("Métadonnées MP3 existantes :")
        print("Titre :", audio.tags.get("TIT2", "Non défini"))
        print("Artiste :", audio.tags.get("TPE1", "Non défini"))
        print("Album :", audio.tags.get("TALB", "Non défini"))
        print("Genre :", audio.tags.get("TCON", "Non défini"))

        # Modifier les métadonnées
        audio.tags["TIT2"] = TIT2(encoding=3, text=meta_donnees["title"])
        audio.tags["TPE1"] = TPE1(encoding=3, text=meta_donnees["artist"])
        audio.tags["TALB"] = TALB(encoding=3, text=meta_donnees["album"])
        audio.tags["TCON"] = TCON(encoding=3, text=meta_donnees["genre"])

        # Ajouter une image de couverture si spécifiée
        if chemin_image:
            with open(chemin_image, "rb") as img:
                audio.tags.add(
                    APIC(
                        encoding=3,
                        mime='image/jpeg',
                        type=3,
                        desc='Cover',
                        data=img.read()
                    )
                )

        # Sauvegarder les modifications
        audio.save()
        print("\nNouvelles métadonnées MP3 mises à jour avec succès !\n")

    def _afficher_et_modifier_meta_flac(self, chemin_audio:str, meta_donnees:str, chemin_image:str):
        """Affiche et modifie les métadonnées d'un fichier FLAC."""
        audio = FLAC(chemin_audio)

        # Afficher les métadonnées existantes
        print("Métadonnées FLAC existantes :")
        print("Titre :", audio.get("title", ["Non défini"])[0])
        print("Artiste :", audio.get("artist", ["Non défini"])[0])
        print("Album :", audio.get("album", ["Non défini"])[0])
        print("Genre :", audio.get("genre", ["Non défini"])[0])

        # Modifier les métadonnées
        audio["title"] = meta_donnees["title"]
        audio["artist"] = meta_donnees["artist"]
        audio["album"] = meta_donnees["album"]
        audio["genre"] = meta_donnees["genre"]

        # Ajouter une image de couverture si spécifiée
        if chemin_image:
            with open(chemin_image, "rb") as img:
                picture = Picture()
                picture.data = img.read()
                picture.type = 3  # Couverture (Cover Front)
                picture.mime = mimetypes.guess_type(chemin_image)[0] or "image/jpeg"
                audio.clear_pictures()
                audio.add_picture(picture)

        # Sauvegarder les modifications
        audio.save()
        print("\nNouvelles métadonnées FLAC mises à jour avec succès !\n")

""" 
    # Exemple d'utilisation de la classe AudioMetaManager
    chemin_mp3 = r"c:\Users\nelly\Documents\L3-info\S5-2024-2025\S5\PYTHON\Imagine Dragons  Bad Liar.mp3"
    chemin_flac = r"c:\Users\nelly\Documents\L3-info\S5-2024-2025\S5\PYTHON\sample4.flac"
    chemin_image = r"c:\Users\nelly\Documents\L3-info\S5-2024-2025\S5\PYTHON\09 - RER D_cover.jpg"

    # Nouvelles métadonnées
    meta_donnees = {
        "title": "Belle Chanson",
        "artist": "Super Artiste",
        "album": "Album A",
        "genre": "Pop"
    }

    # Gérer le fichier MP3
    manager_mp3 = Editer(chemin_mp3, meta_donnees, chemin_image)
    manager_mp3.afficher_et_modifier_metadata()

    # Gérer le fichier FLAC
    manager_flac = Editer(chemin_flac, meta_donnees, chemin_image)
    manager_flac.afficher_et_modifier_metadata()
""" 