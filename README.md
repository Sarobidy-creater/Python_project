# Audio Metadata Extractor

Ce projet est un script Python permettant d'explorer des dossiers à la recherche de fichiers audio (MP3 et FLAC), d'en extraire les métadonnées (titre, artiste, album, etc.) et d'afficher la couverture (cover art) si elle est présente. C'est un outil utile pour analyser et organiser des fichiers audio, notamment dans des collections musicales ou des bibliothèques audio.

## Fonctionnalités

### 1. **Exploration d'un dossier pour détecter les fichiers audio (MP3 et FLAC)**

- **But** : Parcourir un dossier et ses sous-dossiers pour rechercher et identifier les fichiers audio au format MP3 et FLAC.
- **Validation** : Le script vérifie non seulement l'extension du fichier (.mp3 ou .flac), mais aussi son type MIME, garantissant que seuls les fichiers réellement audio sont détectés.

### 2. **Extraction et affichage des métadonnées audio**

- **But** : Extraire et afficher les informations clés d'un fichier audio :
  - Titre
  - Artiste
  - Album
  - Genre
  - Date de sortie
  - Organisation (le label ou la maison de disque)
  - Durée du fichier (en minutes et secondes)
  
### 3. **Affichage de la couverture (Cover Art)**

- **But** : Si une couverture (cover art) est incluse dans le fichier audio (MP3 ou FLAC), elle est extraite et affichée dans une fenêtre. La couverture peut être une image de type JPEG ou PNG intégrée dans les métadonnées du fichier.

### 4. **Conversion de la durée d'un fichier audio**

- **But** : Convertir la durée d'un fichier audio, qui est souvent exprimée en millisecondes, en un format plus compréhensible (minutes et secondes).

### 5. **Création de playlists au format XSPF**

- **But** : Le script permet également de créer et de gérer des playlists au format XSPF (XML Shareable Playlist Format). Ce format est largement utilisé pour décrire des listes de lecture audio.
- **Fonctionnalités** :
  - **Création d'un fichier playlist** : Le script génère un fichier XSPF vide dans un dossier spécifié.
  - **Ajout de pistes audio** : L'utilisateur peut ajouter des fichiers audio à la playlist en fournissant le chemin du fichier et le titre de la piste. Le script crée un élément `<track>` dans le fichier XSPF pour chaque piste ajoutée.
  - **Gestion des fichiers** : Il inclut des fonctions pour supprimer un fichier XSPF si nécessaire.

### Utilisation de la fonctionnalité de playlist

1. **Créer un fichier playlist** : La fonction `creer_un_fichier_xspf` crée un fichier XSPF vide dans le dossier `Python_project/Playlist`. Si le dossier n'existe pas, il est créé automatiquement.
2. **Ajouter des pistes** : L'utilisateur peut ajouter des pistes audio à la playlist en appelant la fonction `ecritureFichierxspf` et en spécifiant le chemin du fichier audio et le titre de la piste.
3. **Supprimer une playlist** : Utilisez la fonction `delete_un_fichier_xspf` pour supprimer une playlist existante en spécifiant le chemin du fichier.

## Prérequis

Avant d'exécuter ce script, vous devez installer les bibliothèques suivantes :

- [mutagen](https://mutagen.readthedocs.io/en/latest/installation.html) : Bibliothèque utilisée pour extraire les métadonnées des fichiers MP3 et FLAC.
- [Pillow](https://python-pillow.org/) : Bibliothèque Python pour manipuler et afficher des images, utilisée ici pour afficher la couverture des fichiers audio.

Pour installer les dépendances, exécutez la commande suivante dans votre terminal :

```bash
pip install mutagen Pillow
