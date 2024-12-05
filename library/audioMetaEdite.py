from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3 
from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3, ID3NoHeaderError, APIC, TIT2, TPE1, TALB, TCON, TDRC, COMM
import mimetypes

class Editer:

    def creation_meta_donnees(self, titre:str, artiste:str, album:str, genre:str, ladate:int, organisation:str) -> dict:
        """
            Fonction qui créer la méta donnée d'un fichier audio.

            Paramètre :
            - titre : str : Le titre du fichier audio.
            - artiste : str : Le nom de l'artiste.
            - album : str : Le nom de l'album.
            - genre : str : Le genre de la musique.
            - ladate : int : La date du fichier audio.
            - organisation : str : L' organisation ou le label.

            Retour :
            - Dict : renvoie une dictionaire de données.
        """
        meta_donnees = {
            # Initialisation d'un dictionnaire pour stocker les métadonnées.
            "title": titre,  # Ajoute le titre à la clé "title".
            "artist": artiste,  # Ajoute le nom de l'artiste à la clé "artist".
            "album": album,  # Ajoute le nom de l'album à la clé "album".
            "genre": genre,  # Ajoute le genre musical à la clé "genre".
            "date": ladate,  # Ajoute l'année de sortie/production à la clé "date".
            "organization": organisation  # Ajoute le nom de l'organisation ou du label à la clé "organization".
        }
        return meta_donnees

    def afficher_et_modifier_metadata(self, chemin_audio:str, chemin_image:str, titre:str, artiste:str, album:str, genre:str, ladate:int, organisation:str) -> None:
        """
            Fonction qui détecte le format du fichier et gère l'affichage et la modification des métadonnées.

            Paramètre :
            - titre : str : Le titre du fichier audio.
            - artiste : str : Le nom de l'artiste.
            - album : str : Le nom de l'album.
            - genre : str : Le genre de la musique.
            - ladate : int : La date du fichier audio.
            - organisation : str : L' organisation ou le label.

            Retour :
            - None : Aucune valeur de retour.
        """
        # Génère un dictionnaire de métadonnées basé sur les informations fournies.
        meta_donnees = self.creation_meta_donnees(titre, artiste, album, genre, ladate, organisation)

        if chemin_audio.endswith(".mp3"):
            # Vérifie si le fichier audio a une extension ".mp3".
            if meta_donnees != None:
                # Si des métadonnées sont présentes, modifie les métadonnées MP3.
                self._afficher_et_modifier_meta_mp3(chemin_audio, meta_donnees)
            if chemin_image != None:
                # Si un chemin d'image est fourni, modifie l'image de couverture MP3.
                self.modify_mp3_cover(chemin_audio, chemin_image)

        elif chemin_audio.endswith(".flac"):
            # Vérifie si le fichier audio a une extension ".flac".
            self._afficher_et_modifier_meta_flac(chemin_audio, meta_donnees, chemin_image)
            # Modifie les métadonnées FLAC et potentiellement la couverture.

        else:
            # Gère les formats non pris en charge.
            print("Format audio non pris en charge.")

    def _afficher_et_modifier_meta_mp3(self, chemin_audio:str, meta_donnees:dict) -> None:
        """
            Fonction qui affiche et modifie les métadonnées d'un fichier MP3.

            Paramètre :
            - chemin_audio : str : Le chemin du dossier contenant le fichier audio.
            - meta_donnees : dict : Dictionnaire de méta donnée.

            Retour :
            - None : Aucune valeur de retour.
        """
        try:
            audio = MP3(chemin_audio, ID3=EasyID3)
            # Tente de charger les métadonnées ID3 du fichier MP3 avec EasyID3.
        except ID3NoHeaderError:
            # Si aucune entête ID3 n'est présente, en crée une nouvelle.
            audio = MP3(chemin_audio)
            audio.add_tags()

        # Modifier les métadonnées
        audio["title"] = meta_donnees["title"]
        audio["artist"] = meta_donnees["artist"]
        audio["album"] = meta_donnees["album"]
        audio["genre"] = meta_donnees["genre"]
        audio["date"] = meta_donnees["date"]
        audio["organization"] = meta_donnees["organization"]
        # Met à jour chaque champ de métadonnées avec les données du dictionnaire.

        audio.save()
        # Sauvegarde les modifications.
        print("\nNouvelles métadonnées MP3 mises à jour avec succès !\n")

    def modify_mp3_cover(self,chemin_audio:str, cover_image_path:str) -> None:
        """
            Fonction qui modifie la couverture d'un fichier MP3.

            Paramètre :
            - chemin_audio : str : Le chemin du dossier contenant le fichier audio.
            - cover_image_path : str : Le chemin du cover pour remplacer l'ancien.

            Retour :
            - None : Aucune valeur de retour.
        """
        audio_cover = MP3(chemin_audio, ID3=ID3)
        # Charge le fichier MP3 avec prise en charge des balises ID3.

        if chemin_audio:
            # Si le fichier audio est valide, lit l'image de couverture.
            with open(cover_image_path, "rb") as cover_file:
                cover_data = cover_file.read()
                # Charge les données binaires de l'image.

            cover = APIC(
                encoding=3,  # Encodage UTF-8.
                mime="image/jpeg",  # Type MIME de l'image (JPG dans cet exemple).
                type=3,  # Type de couverture (3 correspond à une couverture d'album).
                desc="Front cover",  # Description de l'image.
                data=cover_data,  # Données binaires de l'image.
            )
            audio_cover.tags.add(cover)
            # Ajoute la nouvelle image de couverture au fichier MP3.

            audio_cover.save()
            # Sauvegarde les modifications.

    def _afficher_et_modifier_meta_flac(self, chemin_audio:str, meta_donnees:dict, chemin_image:str) -> None:
        """
            Fonction qui affiche et modifie les métadonnées d'un fichier FLAC.

            Paramètre :
            - chemin_audio : str : Le chemin du dossier contenant le fichier audio.
            - meta_donnees : dict : Dictionnaire de méta donnée.
            - chemin_image : str : Le chemin du cover pour remplacer l'ancien.

            Retour :
            - None : Aucune valeur de retour.
        """
        
        audio = FLAC(chemin_audio)
        # Charge le fichier FLAC pour manipulation.

        # Modifier les métadonnées
        audio["title"] = meta_donnees["title"]
        audio["artist"] = meta_donnees["artist"]
        audio["album"] = meta_donnees["album"]
        audio["genre"] = meta_donnees["genre"]
        audio["date"] = meta_donnees["date"]
        audio["organization"] = meta_donnees["organization"]
        # Met à jour chaque champ des métadonnées.

        if chemin_image:
            # Si une image est spécifiée, la lit et l’ajoute en tant que couverture.
            with open(chemin_image, "rb") as img:
                picture = Picture()
                picture.data = img.read()
                picture.type = 3  # Couverture avant (Front Cover).
                picture.mime = mimetypes.guess_type(chemin_image)[0] or "image/jpeg"
                # Détecte le type MIME de l'image ou utilise "image/jpeg" par défaut.
                audio.clear_pictures()
                # Supprime les anciennes images de couverture.
                audio.add_picture(picture)
                # Ajoute la nouvelle image de couverture.

        audio.save()
        # Sauvegarde les modifications dans le fichier FLAC.
        print("\nNouvelles métadonnées FLAC mises à jour avec succès !\n")
