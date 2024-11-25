# Audio Metadata Extractor

Ce projet est un script Python permettant d'explorer des dossiers à la recherche de fichiers audio (MP3 et FLAC), d'en extraire les métadonnées (titre, artiste, album, etc.) et d'afficher la couverture (cover art) si elle est présente. C'est un outil utile pour analyser et organiser des fichiers audio, notamment dans des collections musicales ou des bibliothèques audio.

## Classes du projet

## 1. Éditeur de Métadonnées Audio : Classe Editer()

Cette bibliothèque Python permet de créer, afficher, et modifier les métadonnées des fichiers audio au format **MP3** et **FLAC**. Elle offre également la possibilité d'ajouter ou de remplacer une image de couverture pour ces fichiers.

## 1.a Principales fonctionnalités

1. **Création de métadonnées** :
   - Génération d'un dictionnaire contenant des métadonnées comme le titre, l'artiste, l'album, etc.

2. **Modification des métadonnées** :
   - Ajout ou modification des métadonnées existantes dans les fichiers MP3 et FLAC.

3. **Gestion des images de couverture** :
   - Ajout ou remplacement de l'image de couverture des fichiers MP3 et FLAC.

4. **Affichage des métadonnées existantes** :
   - Lecture et affichage des métadonnées présentes dans les fichiers audio.

---

## 2. Extraction des Métadonnées Audio : Classe Extraction()

Cette classe Python permet d'extraire, d'afficher et de formater les métadonnées des fichiers audio au format **MP3** et **FLAC**. Elle gère également l'extraction des couvertures d'album.

## 2.a Principales fonctionnalités

1. **Extraction des métadonnées** :
   - Titre, Artiste, Album, Genre, Date, Organisation.
   - Format MP3 et FLAC pris en charge.

2. **Durée audio** :
   - Conversion et affichage de la durée en minutes et secondes.

3. **Gestion des fichiers audio** :
   - Validation des chemins des fichiers audio.
   - Gestion des erreurs pour les fichiers manquants ou les formats non pris en charge.

---

## 3. Documentation : Fonction `get_acces_token`

La fonction `get_acces_token` permet de récupérer un jeton d'authentification auprès de l'API Spotify. Ce jeton est requis pour effectuer des requêtes authentifiées et a une durée de validité d'une heure.

## 3.a Fonctionnalité

- **Objectif** : Obtenir un jeton d'accès (access token) pour l'API Spotify en utilisant le mécanisme d'authentification OAuth 2.0 basé sur les **client credentials**.
- **Durée de validité** : Le jeton est valide pendant **1 heure**.

---

## 4. Gestion des Playlists en Python : Classe Playlist()

Ce projet Python fournit une classe `Playlist` pour créer et gérer des fichiers de playlists au format XSPF. Il offre des fonctionnalités permettant :

- De créer des fichiers de playlists par défaut ou personnalisés.
- D'ajouter des pistes à partir d'un dossier ou d'une sélection de fichiers.
- D'intégrer des informations supplémentaires comme la date de création.

Le script utilise des bibliothèques standard et tierces pour manipuler les fichiers XML et interagir avec le système de fichiers.

## 4.a Principales fonctionnalités

1. **Créer un fichier par défaut** :
   - Crée un fichier `maPlaylist.xspf` dans le répertoire `Python_project/Playlist`.
   - Inclut une structure XML minimale.

2. **Créer un fichier spécifique** :
   - Permet de définir un nom personnalisé pour le fichier XSPF.
   - Le fichier est enregistré dans le répertoire `Python_project/Playlist`.

3. **Ajouter des pistes à une playlist** :
   - Ajoute une liste de pistes provenant d'un dossier ou d'une sélection manuelle.
   - Les pistes sont ajoutées avec leurs emplacements respectifs au format `file:///`.

## 2.b Manipulation de fichiers XML

- Utilise `lxml` pour créer et mettre à jour la structure XML des playlists.
- Ajoute des éléments comme `<date>` et `<trackList>` au fichier XSPF.

---

## 5. Lecteur Audio Polyvalent : Classe Ecouter()

Ce projet est une classe Python permettant de lire divers formats de fichiers audio tels que **MP3**, **FLAC**, et **WAV**. Elle utilise la bibliothèque **Pygame** pour la lecture audio et **Pydub** pour la conversion des fichiers FLAC en WAV afin de les rendre compatibles avec Pygame.

## 5.a Principales fonctionnalités  

1. **Lecture de fichiers MP3** :
   - Chargement et lecture directe des fichiers MP3.

2. **Lecture de fichiers FLAC** :
   - Conversion des fichiers FLAC en WAV temporaire pour permettre leur lecture.

3. **Lecture de fichiers WAV** :
   - Lecture directe des fichiers WAV.

4. **Gestion intelligente des fichiers audio** :
   - Identifie automatiquement le type de fichier audio basé sur son extension et appelle la méthode correspondante.

---

## 6. Explorateur de Fichiers Audio : Classe Explorer()

Ce projet fournit une classe Python pour explorer des dossiers, identifier les fichiers audio au format **MP3**, **FLAC**, et gérer des playlists au format **XSPF**. Il offre des fonctionnalités permettant de lister les fichiers dans la console, de créer des fichiers de sortie avec les chemins audio et d'extraire les pistes des playlists.

## 6.a Principales fonctionnalités  

1. **Exploration de dossiers audio** :
   - Identifie les fichiers MP3 et FLAC dans un répertoire donné.
   - Stocke les chemins des fichiers trouvés dans un fichier texte ou les affiche dans la console.

2. **Support des playlists XSPF** :
   - Recherche les fichiers de playlist **.xspf**.
   - Extrait les chemins des pistes des playlists.

3. **Gestion des fichiers temporaires** :
   - Génère des fichiers temporaires contenant les résultats d'exploration.

---

## 7. Spotify API Fetcher : Classe Fetcher()

Ce script permet de récupérer des informations sur des artistes, des albums et des pistes à partir de l'API Spotify, en utilisant un client autorisé via un token d'accès. Le script interagit avec l'API Spotify pour effectuer des recherches par nom d'artiste, album ou piste, puis sauvegarde les résultats sous forme de fichiers JSON. Il inclut également des fonctionnalités pour vérifier la connexion Internet et gérer les erreurs de connexion.

## 7.a Principales fonctionnalités  

1. **Vérification de la connexion Internet**

   - Avant d'interagir avec l'API Spotify, le script vérifie si une connexion Internet est disponible en    envoyant une requête à Google. Si la connexion échoue, l'accès à l'API Spotify sera impossible.

2. **Authentification via l'API Spotify**

   - Le script utilise le mécanisme d'authentification par client `client_credentials` de Spotify. Il encodera les identifiants du client en Base64 et enverra une requête à l'API pour obtenir un jeton d'accès. Ce jeton est utilisé pour authentifier les requêtes ultérieures vers l'API Spotify.

3. **Recherche sur l'API Spotify**

   - Le script permet de rechercher des artistes, des albums et des pistes via l'API Spotify. Vous pouvez effectuer une recherche en utilisant un terme de recherche, et spécifier si vous recherchez un artiste, un album ou une piste. Le type de requête est défini à l'aide de l'énumération `APIQueryType`.

4. **Sauvegarde des résultats dans un fichier JSON**

   - Une fois les données récupérées, elles sont sauvegardées dans des fichiers JSON locaux. Ces fichiers contiennent des informations sur les artistes, albums ou pistes, et peuvent être lus plus tard pour afficher ou analyser les données.

5. **Lecture et affichage des données JSON**

   - Les données enregistrées dans les fichiers JSON peuvent être lues et affichées de manière formatée. Le script fournit des méthodes pour afficher les informations sur les artistes, albums et pistes de manière lisible. Si un fichier JSON est manquant ou mal formaté, une erreur est renvoyée.

---

## 8. **Console** : Classe Console()

La classe `Console` sert d'interface utilisateur pour interagir avec le programme via la ligne de commande. Elle gère les options fournies par l'utilisateur et coordonne l'utilisation des autres classes :

- **`afficher_aide(self)`** : Affiche un message d'aide sur l'utilisation du programme.
- **`main(self)`** : Analyse les arguments de ligne de commande et appelle les méthodes appropriées des classes `Explorer`, `Extraction`, et `Playlist`.

## Importations

Le fichier `__init__.py` initialise le package `Python_project`. Il importe les classes suivantes pour un accès facile :

- **`Extraction`** : Importée depuis le module `audioTagExtraction`, elle permet d'extraire et d'afficher les métadonnées des fichiers audio.
- **`Playlist`** : Importée depuis le module `constitutionPlaylist`, elle gère la création et la modification des playlists au format XSPF.
- **`Explorer`** : Importée depuis le module `explorationDossier`, elle permet d'explorer les dossiers à la recherche de fichiers audio.

Les variables et constantes définies dans le fichier peuvent inclure la version du package, facilitant la gestion des mises à jour.

## Utilisation de la Console

Pour utiliser le script depuis la ligne de commande, assurez-vous d'abord d'être dans le dossier contenant le fichier `cli.py`. Ensuite, vous pouvez suivre les exemples ci-dessous :

- **Exécuter le script** :

    ```bash
    python3 cli.py
    ```

- **Afficher l'aide** :
  
    ```bash
    python3 cli.py -h
    ```

    ou

    ```bash
    python3 cli.py --help
    ```

- **Explorer le dossier courant** :
  
    ```bash
    python3 cli.py -d .
    ```

    ou

    ```bash
    python3 cli.py --directory .
    ```

- **Explorer un dossier spécifique** :
  
    ```bash
    python3 cli.py -d "chemin\vers\un\dossier"
    ```

    ou

    ```bash
    python3 cli.py --directory "chemin\vers\un\dossier"
    ```

- **Extraire les métadonnées d'un fichier audio dans le dossier music éxistant** :
  
    ```bash
    python3 cli.py -f music.mp3
    ```

    ou

    ```bash
    python3 cli.py --file music.mp3
    ```

- **Extraire les métadonnées d'un fichier audio en donnant un chemin spécifique** :
  
    ```bash
    python3 cli.py -f "chemin\vers\la\musique\music.mp3"
    ```

    ou

    ```bash
    python3 cli.py --file "chemin\vers\la\musique\music.mp3"
    ```

- **Générer une playlist à partir d'un dossier music éxistant et en spécifiant le nom de la playlist** :
  
    ```bash
    python3 cli.py -d ./music/ -o nom_de_votre_playlist.xspf
    ```

    ou
  
    ```bash
    python3 cli.py --directory ./music/ --output nom_de_votre_playlist.xspf
    ```

- **Générer une playlist à partir d'un dossier spécifique et en spécifiant le nom de la playlist** :
  
    ```bash
    python3 cli.py -d "chemin\vers\un\dossier" -o nom_de_votre_playlist.xspf
    ```

    ou

    ```bash
    python3 cli.py --directory "chemin\vers\un\dossier" --output nom_de_votre_playlist.xspf
    ```

- **Lancer l'interface graphique (si disponible)** :
  
    ```bash
    python3 gui.py
    ```

- **Ecouter un fichier audio donné** :
  
    ```bash
    python3 cli.py -l -f music.mp3
    ```

    ou

    ```bash
    python3 cli.py --listen --file music.mp3
    ```

- **Ecouter un fichier audio en donnant un chemin spécifique** :
  
    ```bash
    python3 cli.py -l -f "chemin\vers\la\musique\music.mp3"
    ```

    ou

    ```bash
    python3 cli.py --listen --file "chemin\vers\la\musique\music.mp3"
    ```

---

## 9. **Interface de gestion des fichiers audio** : Classe Interface()

Ce projet est une interface graphique qui permet d'explorer des fichiers audio sur votre ordinateur, d'en extraire les métadonnées, d'afficher la couverture d'album (cover art), et de créer des playlists. Il est conçu pour être simple d'utilisation grâce à des boutons et des fenêtres interactives.

## Introduction

Cette application de gestion de musique vous permet de rechercher, lire, et gérer vos fichiers audio de manière efficace. Ce document explique les différentes fenêtres et boutons de l'interface utilisateur.

## 1. Choix du dossier à explorer

- **But** : Sélectionner un dossier contenant des fichiers audio (MP3 et FLAC) sur votre ordinateur pour les analyser.
- **Fonctionnement** : Un explorateur de fichiers s'ouvre pour naviguer et choisir le dossier. Les fichiers audio trouvés sont ensuite listés dans l'interface.
- **Code associé** : La méthode `exploration_dossier()` ou `AZEexploration_dossier()` est utilisée pour parcourir le système de fichiers et charger les fichiers audio dans une Listbox.

## 2. Affichage des fichiers audio détectés

- **But** : Après avoir sélectionné un dossier, une liste de fichiers audio détectés (formats MP3 et FLAC) est affichée.
- **Fonctionnalité additionnelle** : L'utilisateur peut sélectionner un fichier audio pour afficher ses métadonnées.
- **Code associé** : La méthode `exploration_dossier()` peuple la Listbox avec les fichiers audio. La fonction `affiche_path_label()` extrait les informations du fichier sélectionné.

## 3. Extraction et affichage des métadonnées

- **But** : Afficher les métadonnées (titre, artiste, album, genre, etc.) des fichiers audio sélectionnés.
- **Fonctionnement** : Lorsqu'un fichier est cliqué dans la liste, ses métadonnées sont extraites et affichées dans l'interface.
- **Code associé** : La méthode `affiche_path_label()` appelle `extraction_et_afficher_tag()` pour extraire les métadonnées du fichier audio sélectionné.

## 4. Affichage de la couverture (Cover Art)

- **But** : Afficher l'image de couverture d'un fichier audio s'il en contient une.
- **Fonctionnement** : Si une image de couverture est détectée dans le fichier audio, elle est affichée dans une zone dédiée. Sinon, une image par défaut est utilisée.
- **Code associé** : La méthode `cover_image()` gère l'extraction et l'affichage de la couverture d'album.

## 5. Fenêtre Principale

À l'ouverture de l'application, vous verrez la fenêtre principale qui contient plusieurs sections et boutons. Voici les boutons disponibles :

- **Jouer** :
  - Bouton pour lire l'audio **▶**
  - Cliquez sur ce bouton pour lire l'audio sélectionné.

- **Pause / Reprendre** :
  - Bouton pour faire pause l'audio **⏸**
  - Bouton pour reprendre la lecture l'audio **■**
  - Utilisez ces boutons pour mettre en pause la lecture de l'audio ou reprendre la lecture après une pause.

- **Playlist** :
  - Bouton pour créer ou gérer vos playlists **Playlist**
  - Ce bouton ouvre une nouvelle fenêtre pour créer ou gérer vos playlists.

- **Parcourir** :
  - Bouton pour parcourir un dossier et ses sous-dossiers **Parcourir**
  - Permet de parcourir un dossier et ses sous-dossiers pour sélectionner des fichiers audio.

- **Ecouter** :
  - Bouton pour écouter une playlist sélectionée **Ecouter**
  - Permet la lecture des fichiers audio dans une playlist sélectionée.
  
- **Next** :
  - Bouton pour l'audio suivant **▶▶**
  - Passe à l'audio suivant dans la liste.

- **Prev** :
  - Bouton pour l'audio précédent **◀◀**
  - Revient à l'audio précédent dans la liste.

- **Modifier Métadonnées (:::)** :
  - Bouton pour modifier les métadonnées **:::**
  - Ouvre une fenêtre pour modifier les métadonnées d'un fichier audio.
  
- **Rechercher** :
  - Bouton pour utilise une API **Check**
  - Utilisez ce bouton pour rechercher un artiste, un album, ou une musique en utilisant une API.
  - Entrez votre recherche dans le champ de saisie (Entry).

### Fonctionnalité de Recherche de Musique

L'application utilise une API tierce pour effectuer des recherches de musique. Voici comment cela fonctionne :

#### 1. Saisie de la Recherche

L'utilisateur entre une commande dans le champ de recherche. Les commandes acceptées incluent :

- **artiste** : `artiste: Nom de l'artiste`
- **album** : `album: Nom de l'album`
- **music** : `music: Nom de la musique`

Ces commandes permettent à l'utilisateur de spécifier exactement ce qu'il recherche, facilitant ainsi l'accès aux résultats souhaités.

#### 2. Envoi de la Requête

Lorsque l'utilisateur clique sur le bouton **Check**, l'application envoie une requête à l'API avec les paramètres spécifiés. Cette requête est généralement formulée en utilisant une méthode HTTP (comme GET ou POST) pour récupérer des données. Cela permet à l'application d'interroger efficacement l'API et de récupérer des informations pertinentes sur la musique.

#### 3. Réception des Résultats

L'API renvoie les résultats de la recherche sous forme de données structurées, en format JSON. L'application traite ces données pour extraire les informations pertinentes, telles que les titres des morceaux, les noms des artistes et les albums associés.

#### 4. Affichage des Résultats

Les résultats de la recherche (artistes, albums, morceaux) sont ensuite affichés dans l'interface utilisateur.

## 6. Création de playlists

### 6.1 Playlist par défaut

- **But** : Créer une playlist par défaut qui contient une liste d'audio préétablie dans la Listbox.
- **Fonctionnalité** : Lors de l'initialisation de l'application, une playlist par défaut est chargée et affichée, permettant à l'utilisateur d'écouter facilement une sélection prédéfinie de fichiers audio.

### 6.2 Playlist spécifiée

- **But** : Permettre à l'utilisateur de spécifier une playlist par son nom et de sélectionner les audios à inclure dans cette playlist.
- **Fonctionnalité** : Une interface avec des cases à cocher est fournie pour que l'utilisateur puisse sélectionner les fichiers audio souhaités et les inclure dans une playlist personnalisée. L'utilisateur peut sauvegarder cette playlist sous un nom spécifique.
- **Code associé** : Les fonctions `open_new_fenetre()`, `par_defaut()`, et `specifier()` permettent la création, la spécification, et la réinitialisation des playlists. Le fichier est enregistré grâce à `gui_ecritureFichierxspf()`.

## 7. Fenêtre de Playlist

En cliquant sur le bouton **Playlist**, une nouvelle fenêtre s'ouvrira avec les options suivantes :

- **Annuler** :
  - Bouton pour annuler toutes les opérations **Annuler**
  - Annule toutes les opérations en cours et ferme la fenêtre de playlist sans sauvegarder les modifications.

- **Playlist par défaut** :
  - Bouton pour créer la playlist par défaut **par défaut**
  - Crée la playlist par défaut qui contient une liste d'audio préétablie dans la Listbox affichée sur l'interface. Cette playlist peut être utilisée pour une lecture rapide sans nécessiter de configuration supplémentaire.

- **Playlist spécifiée** :
  - Bouton pour spécifier une playlist **spécifier**
  - Permet de spécifier une playlist par son nom et de sélectionner les audios à inclure dans cette playlist à l'aide de cases à cocher (checkbox). L'utilisateur peut cocher les fichiers audio qu'il souhaite ajouter à sa playlist personnalisée.
  
- **Sélectionner toutes les checkboxes** :
  - Bouton pour sélectionner toutes les checkboxes **T-select**
  - Lorsqu’on clique sur le bouton T-select, toutes les checkboxes de la liste sont cochées.
  
- **Désélectionner toutes les checkboxes** :
  - Bouton pour désélectionner toutes les checkboxes **T-déselect**
  - En cliquant sur T-déselect, toutes les checkboxes de la liste sont décochées.

## 8. Fenêtre de Modification des Métadonnées

En cliquant sur le bouton **Modifier Métadonnées (:::)**, une nouvelle fenêtre apparaîtra, permettant à l'utilisateur de modifier les informations d'un fichier audio. Cette fenêtre est équipée de plusieurs champs et boutons pour faciliter la gestion des métadonnées.

### Labels et Zones de Saisie

La fenêtre de modification contient les champs suivants, chacun associé à un label explicite :

- **Titre** : Champ pour saisir ou modifier le titre de la piste audio.
- **Artiste** : Champ pour saisir ou modifier le nom de l'artiste.
- **Album** : Champ pour saisir ou modifier le nom de l'album.
- **Genre** : Champ pour saisir ou modifier le genre musical.
- **Date** : Champ pour saisir ou modifier la date de sortie.
- **Organisation** : Champ pour saisir ou modifier l'organisation ou le label musical.

Chaque champ contient par défaut les valeurs actuelles des métadonnées, facilitant ainsi la modification. Cela permet à l'utilisateur de garder les informations existantes tout en offrant la possibilité de les mettre à jour rapidement.

### Bouton Modifier la Couverture

Ce bouton ouvre un explorateur de fichiers pour choisir une nouvelle image de couverture pour l'audio. La couverture sélectionnée sera associée au fichier audio et affichée dans l'interface.

### Boutons d'Action

- **Annuler** :
  - Bouton pour annuler toutes les opérations **Annuler**
  - Ferme la fenêtre sans effectuer d'opérations sur les métadonnées.

- **Sélectionner une couverture** :
  - Bouton pour sélectionner une couverture **Sélectionner une couverture**
  - Ouvre un explorateur de fichiers pour choisir une image de couverture pour l'audio.

- **Enregistrer** :
  - Bouton pour sauvegarde les métadonnées **Enregistrer**
  - Sauvegarde les métadonnées saisies dans les champs de texte et la couverture si elle a été modifiée.

## 9. Contrôle de lecture (Play/Pause/Next/Previous)

- **But** : Contrôler la lecture des fichiers audio depuis l'interface.
- **Fonctionnalité** :
  - **Play/Pause** : Lire ou mettre en pause la chanson sélectionnée.
  - **Next/Previous** : Passer à la piste suivante ou précédente.
- **Code associé** :
  - `lire_audio()` pour la lecture.
  - `toggle_pause()` pour basculer entre pause et lecture.
  - `next_audio()` et `prev_audio()` pour changer de piste.

## 10. Navigation et interaction améliorée

- **But** : Permettre une navigation fluide entre les fichiers audio.
- **Fonctionnement** : Lorsqu'une nouvelle piste est sélectionnée, les informations affichées sont mises à jour, et les boutons "suivant" et "précédent" permettent de naviguer rapidement.
- **Code associé** : Les méthodes `next_item()` et `prev_item()` gèrent les changements de sélection dans la Listbox.

## Utilisation Générale

- **Lancer une recherche** :
  - Entrez une commande dans le champ de recherche et cliquez sur le bouton "Rechercher".
  - Les résultats s'afficheront en fonction de votre saisie.

- **Lire de la musique** :
  - Sélectionnez un morceau dans la liste et cliquez sur "Jouer" pour commencer la lecture.
  - Utilisez "Pause" pour mettre la musique en pause et "Reprendre" pour continuer la lecture.

- **Gérer les playlists** :
  - Cliquez sur le bouton "Playlist" pour ouvrir la fenêtre de gestion des playlists.
  - Vous pourrez y ajouter, supprimer ou modifier votre playlist.

- **Modifier les métadonnées** :
  - Cliquez sur "Modifier Métadonnées" pour ouvrir la fenêtre de modification.
  - Apportez vos changements, sélectionnez une couverture si besoin, puis cliquez sur "Enregistrer" pour sauvegarder.

## Conclusion

Cette application vous offre une interface simple et efficace pour gérer votre collection musicale. N'hésitez pas à explorer toutes les fonctionnalités disponibles et à personnaliser votre expérience.

## Prérequis

Avant d'exécuter ce script, vous devez installer les bibliothèques suivantes :

- [mutagen](https://mutagen.readthedocs.io/en/latest/installation.html) : Bibliothèque utilisée pour extraire les métadonnées des fichiers MP3 et FLAC.
- [Pillow](https://python-pillow.org/) : Bibliothèque Python pour manipuler et afficher des images.
- [Pygame](https://www.pygame.org/) : Bibliothèque pour créer des jeux en Python et jouer des fichiers audio.
- [Pydub](https://github.com/jiaaro/pydub) : Bibliothèque pour manipuler les fichiers audio.
- [lxml](https://...) : Bibliothèque pour...

Pour installer les dépendances, exécutez la commande suivante dans votre terminal :

```bash
pip install mutagen 
pip install Pillow 
pip install pygame
pip install pydub
pip install lxml
