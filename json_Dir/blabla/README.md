
# Lecteur de Musique et Gestionnaire de Playlist

Ce projet est un lecteur de musique simple avec gestion de playlists. Il utilise Tkinter pour l'interface graphique et Pygame pour la lecture audio. Il prend en charge les fichiers audio au format MP3 et FLAC.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés:

- Python 3.x
- Les bibliothèques Python suivantes :
  - `tkinter`
  - `mutagen`
  - `pygame`
  - `Pillow`
  - `lxml`

Vous pouvez installer les bibliothèques manquantes avec pip:

```bash
pip install mutagen pygame Pillow lxml
```

## Installation

1. Clonez ce dépôt ou téléchargez les fichiers source.
2. Exécutez le script Python `main.py` pour démarrer l'application.

```bash
python main.py
```

## Utilisation

1. **Explorer les fichiers audio**: Cliquez sur le bouton "Explorer" pour sélectionner un dossier contenant des fichiers audio (MP3 ou FLAC). Les fichiers audio seront listés dans l'interface.

2. **Sélectionner un fichier audio**: Cliquez sur un fichier dans la liste pour afficher ses métadonnées (titre et artiste) ainsi que la couverture de l'album, si disponible.

3. **Contrôles audio**:
   - **Lecture**: Cliquez sur le bouton "Lecture" pour commencer la lecture de la musique sélectionnée.
   - **Pause**: Cliquez sur le bouton "Pause" pour mettre la musique en pause.
   - **Reprendre**: Cliquez sur le bouton "Reprendre" pour reprendre la lecture de la musique.
   - **Arrêter**: Cliquez sur le bouton "Arrêter" pour arrêter la musique.

4. **Créer une playlist**: Cliquez sur le bouton "Créer Playlist" pour enregistrer une nouvelle playlist au format XSPF.

5. **Ajouter à la playlist**: Sélectionnez une playlist et ajoutez le fichier audio sélectionné à cette playlist.

## Contribuer

Les contributions sont les bienvenues! N'hésitez pas à soumettre un pull request.

## License

Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus de détails.
