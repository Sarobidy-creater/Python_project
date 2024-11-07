from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3 
from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3, ID3NoHeaderError, APIC, TIT2, TPE1, TALB, TCON, TDRC, COMM
import mimetypes

class Editer:

    def creation_meta_donnees(self, titre:str, artiste:str, album:str, genre:str, ladate:int, organisation:str):
        meta_donnees = {
            "title": titre,
            "artist": artiste,
            "album": album,
            "genre": genre,
            "date": ladate,  # str(ladate).zfill(4),  # Format de l'année pour TDRC
            "organization": organisation
        }
        return meta_donnees


    def afficher_et_modifier_metadata(self, chemin_audio:str, chemin_image:str, titre:str, artiste:str, album:str, genre:str, ladate:int, organisation:str):
        """Détecte le format du fichier et gère l'affichage et la modification des métadonnées."""
        meta_donnees = self.creation_meta_donnees(titre, artiste, album, genre, ladate, organisation)
        if chemin_audio.endswith(".mp3"):
            if meta_donnees != None:
                self._afficher_et_modifier_meta_mp3(chemin_audio, meta_donnees)
            if chemin_image != None:
                self.modify_mp3_cover(chemin_audio,chemin_image)
        elif chemin_audio.endswith(".flac"):
            self._afficher_et_modifier_meta_flac(chemin_audio, meta_donnees, chemin_image)
        else:
            print("Format audio non pris en charge.")


    def _afficher_et_modifier_meta_mp3(self, chemin_audio:str, meta_donnees:dict):
        """Affiche et modifie les métadonnées d'un fichier MP3."""
        try:
            audio = MP3(chemin_audio, ID3=EasyID3)
        except ID3NoHeaderError:
            audio = MP3(chemin_audio)
            audio.add_tags()

        # Afficher les métadonnées existantes
        # Afficher les métadonnées existantes
        # print("Métadonnées FLAC existantes :pppppppppppppppppppppppppppppppppppppppppp")
        # print("Titre :", audio.get("title", ["Non défini"])[0])
        # print("Artiste :", audio.get("artist", ["Non défini"])[0])
        # print("Album :", audio.get("album", ["Non défini"])[0])
        # print("Genre :", audio.get("genre", ["Non défini"])[0])
        # print("Date :", audio.get("date", ["Non défini"])[0])
        # print("Organization :", audio.get("organization", ["Non défini"])[0])

        # Modifier les métadonnées
        audio["title"] = meta_donnees["title"]
        audio["artist"] = meta_donnees["artist"]
        audio["album"] = meta_donnees["album"]
        audio["genre"] = meta_donnees["genre"]
        audio["date"] = meta_donnees["date"]
        audio["organization"] = meta_donnees["organization"]

        # Sauvegarder les modifications
        audio.save()
        print("\nNouvelles métadonnées MP3 mises à jour avec succès !\n")


    def modify_mp3_cover(self,chemin_audio:str, cover_image_path:str):
        """Modifie la couverture d'un fichier MP3."""
        # Charger le fichier MP3
        audio_cover = MP3(chemin_audio, ID3=ID3)

         # Ajouter une image de couverture si spécifiée
        if chemin_audio:
            # Lire l'image
            with open(cover_image_path, "rb") as cover_file:
                cover_data = cover_file.read()

            # Créer une balise APIC pour la couverture
            # "image/jpeg" pour une image JPG, ou "image/png" pour une image PNG
            cover = APIC(
                encoding=3,  # 3 signifie UTF-8
                mime="image/jpeg",  # Type MIME de l'image
                type=3,  # Type de couverture (3 correspond à l'album)
                desc="Front cover",  # Description de l'image
                data=cover_data,  # Les données de l'image
            )

            # Ajouter la couverture à l'ID3 du fichier MP3
            audio_cover.tags.add(cover)

            # Sauvegarder les modifications dans le fichier MP3
            audio_cover.save()


    def _afficher_et_modifier_meta_flac(self, chemin_audio:str, meta_donnees:dict, chemin_image:str):
        """Affiche et modifie les métadonnées d'un fichier FLAC."""
        audio = FLAC(chemin_audio)

        # Afficher les métadonnées existantes
        # print("Métadonnées FLAC existantes :")
        # print("Titre :", audio.get("title", ["Non défini"])[0])
        # print("Artiste :", audio.get("artist", ["Non défini"])[0])
        # print("Album :", audio.get("album", ["Non défini"])[0])
        # print("Genre :", audio.get("genre", ["Non défini"])[0])
        # print("Date :", audio.get("date", ["Non défini"])[0])
        # print("Organisation :", audio.get("organization", ["Non défini"])[0])

        # Modifier les métadonnées
        audio["title"] = meta_donnees["title"]
        audio["artist"] = meta_donnees["artist"]
        audio["album"] = meta_donnees["album"]
        audio["genre"] = meta_donnees["genre"]
        audio["date"] = meta_donnees["date"]
        audio["organization"] = meta_donnees["organization"]

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
