#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import base64
import json
import os
import time
import requests
from library.APIQueryType import APIQueryType
from urllib.parse import urlencode


class Fetcher:

    def __init__(self):
        """
        Initialise la classe avec l'ID client et le secret client.
        Puis tente d'autoriser le client avec l'API Spotify.
        """
        # Identifiants du client Spotify (nécessaires pour l'authentification)
        self.client_id = "45a8a345769d4ac0b91d95622d331f05"
        self.client_secret = "1fc622291bbd48f487b2375179fcbc23"
        self.authorization_token = None  # Token d'authentification pour accéder à l'API
        self.token_url = 'https://accounts.spotify.com/api/token'  # URL pour obtenir le token d'accès
        self.spotify_api_url = 'https://api.spotify.com/v1'  # URL de base pour interagir avec l'API Spotify

        # Chemins vers les fichiers JSON où les résultats de l'API seront sauvegardés localement
        self.chemin_artist_json = os.path.abspath(r"Python_project\\json_Dir\\artist_json.json")
        self.chemin_album_json = os.path.abspath(r"Python_project\\json_Dir\\album_json.json")
        self.chemin_track_json = os.path.abspath(r"Python_project\\json_Dir\\track_json.json")

        # Appel à la fonction pour vérifier la connexion Internet et tenter l'autorisation
        self.check_internet_and_authorize()

    def check_internet_and_authorize(self):
        """
        Vérifie si une connexion Internet est disponible et tente d'obtenir un jeton d'authentification si possible.
        """
        if self.is_internet_available():
            print("Connexion Internet détectée. Tentative d'autorisation...")
            self.authorize_client()  # Si Internet est disponible, tente d'obtenir un token d'autorisation
            return True
        else:
            print("Aucune connexion Internet. Impossible d'accéder à l'API Spotify.")
            return False
    
    def is_internet_available(self):
        """
        Vérifie si une connexion Internet est disponible en envoyant une requête à Google.
        """
        try:
            # Envoi d'une requête HTTP GET vers Google pour tester la connexion
            response = requests.get("https://www.google.com", timeout=5)
            return True  # Si la requête réussit, l'Internet est disponible
        except requests.ConnectionError:
            return False  # Si une erreur de connexion se produit, Internet n'est pas disponible

    def authorize_client(self) -> bool:
        """
            Fonction qui récupère un jeton d'authentification et autorise l'accès à l'API Spotify.
            Retourne un booléen indiquant si l'authentification a réussi.
            
            Paramètre :
            - 
            
            Retour :
            - bool : 
        """
        # Vérifie si un token valide est déjà en place (pas expiré)
        if self.authorization_token and self.token_is_valid():
            print("Token déjà valide")  # Si le token est valide, pas besoin d'authentification
            return True

        # Encodage des identifiants client en base64 pour l'authentification
        client_credentials = f'{self.client_id}:{self.client_secret}'
        client_credentials_b64 = base64.b64encode(client_credentials.encode())  # Encode l'ID et le secret

        # Paramètres nécessaires pour la requête de token (grant_type = client_credentials)
        token_data = {'grant_type': 'client_credentials'}
        token_headers = {'Authorization': f'Basic {client_credentials_b64.decode()}'}  # Ajout du header d'authentification

        # Envoi de la requête POST pour obtenir le jeton d'accès
        request = requests.post(url=self.token_url, data=token_data, headers=token_headers)

        # Vérification si la requête a échoué (code de statut HTTP en dehors de la plage 200-299)
        if request.status_code not in range(200, 299):
            raise Exception(f'Échec de l’authentification : code {request.status_code}')  # Si l'authentification échoue, une exception est levée

        # Traitement de la réponse JSON contenant le token et le temps d'expiration
        token_response_data = request.json()
        self.authorization_token = token_response_data['access_token']  # Récupère le token d'accès
        self.token_expiry_time = time.time() + token_response_data['expires_in']  # Calcul du temps d'expiration du token
        print(f'Client autorisé avec succès !')  # Affiche un message confirmant l'authentification
        return True  # Retourne True si l'authentification a réussi

    def token_is_valid(self):
        """
            Fonction qui 

            Paramètre :
            - 
            
            Retour :
            -  : 
        """
        return time.time() < self.token_expiry_time   # Retourne True si l'heure actuelle est avant l'heure d'expiration du token

    def search(self, query: str, query_type: APIQueryType) -> dict:
        """
            Fonction qui effectue une recherche dans l'API Spotify selon le type de requête.
            Gère les erreurs de connexion et réessaie si nécessaire.

            Paramètre :
            - 
            
            Retour :
            - dict : 
        """
        # Vérifie que le type de requête est valide en s'assurant qu'il s'agit d'un objet de type APIQueryType
        if not isinstance(query_type, APIQueryType):
            raise Exception('Type de requête invalide !')

        # Vérifie si un token d'autorisation est disponible, sinon l'accès à l'API échoue
        if not self.authorization_token:
            print("Erreur : Client non autorisé. Impossible de récupérer les informations.")
            return {}

        # Création des headers pour l'authentification avec le token d'autorisation
        headers = {'Authorization': f'Bearer {self.authorization_token}'}
        # Définition de l'URL de l'API pour effectuer une recherche
        endpoint = self.spotify_api_url + '/search?'
        # Encode la requête (terme de recherche) et le type de contenu à rechercher (par exemple, artiste, album, etc.)
        data = urlencode({'q': query, 'type': query_type.value})
        # Construction de l'URL complète pour la requête de recherche
        search_url = f'{endpoint}{data}'

        try:
            # Envoi de la requête GET à l'API Spotify pour effectuer la recherche
            request = requests.get(search_url, headers=headers)
            # Vérifie que la requête s'est bien déroulée (code HTTP entre 200 et 299)
            request.raise_for_status()  # Lève une exception si le code HTTP indique une erreur
        except requests.RequestException as e:
            # Gestion des erreurs réseau ou autres exceptions
            print(f"Erreur réseau : {e}")
            if not self.is_internet_available():
                print("Aucune connexion Internet. Impossible de poursuivre la recherche.")
            else:
                print("Tentative de réessayer après une courte pause...")
                time.sleep(5)  # Attente de 5 secondes avant de réessayer la requête
                return self.search(query, query_type)  # Appel récursif pour réessayer la recherche

        # Retourne les résultats de la recherche sous forme de dictionnaire JSON
        return request.json()
    
    def save_to_json(self, data: dict, filename: str) -> None:
        """
            Fonction qui enregistre les données dans un fichier JSON.

            Paramètre :
            - 
            
            Retour :
            - None : 
        """
        # Vérifie si le dossier contenant le fichier existe, et le crée si nécessaire
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Ouvre le fichier en mode écriture et sauvegarde les données sous forme de JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)  # Sérialisation des données en JSON
        print(f"Données enregistrées dans le fichier {filename}")  # Affiche un message de confirmation

    def get_artist_info(self, artist_name: str):
        """
            Fonction qui récupère les informations d’un artiste via l'API Spotify.

            Paramètre :
            - artist_name : str : Le nom de l’artiste à rechercher.

            Retour :
            - dict : Un dictionnaire contenant les informations de l’artiste, avec :
                - Clé : ID unique Spotify de l’artiste
                - Valeurs : Dictionnaire des informations (nom, popularité, followers, genres)
        """
        # Vérification que le nom de l'artiste est fourni
        if not artist_name:
            raise Exception('Un nom d’artiste valide doit être fourni')

        artist_data = {}

        # Appel à la fonction de recherche pour récupérer les données de l'artiste
        data = self.search(artist_name, APIQueryType.ARTIST)

        # Extraction des informations pertinentes à partir de la réponse de l'API
        for artist in data['artists']['items']:
            # Comparaison insensible à la casse pour trouver l'artiste exact
            if artist['name'].lower() == artist_name.lower():
                artist_info = {
                    'Artiste': artist['name'],
                    'popularity': artist['popularity'],
                    'type': artist['type'],
                    # Extraction du nombre de followers, avec une valeur par défaut si non disponible
                    'Followers': artist.get('followers', {}).get('total', 'Données non disponibles'),
                    'Genres': artist['genres']
                }
                # Ajout de l'artiste au dictionnaire avec son ID unique
                artist_data[artist['id']] = artist_info

        # Si aucune donnée n'est trouvée pour cet artiste, afficher un message
        if not artist_data:
            print('Aucune donnée sur cet artiste n’a été trouvée sur Spotify.')
            return {}

        # Sauvegarde des informations de l'artiste dans un fichier JSON
        self.save_to_json(artist_data, self.chemin_artist_json)

    def get_album_info(self, album_name: str):
        """
            Fonction qui récupère les informations d’un album via l'API Spotify.

            Paramètre :
            - album_name : str : Le nom de l’album à rechercher.

            Retour :
            - dict : Un dictionnaire contenant les informations de l’album, avec :
                - Clé : ID unique Spotify de l’album
                - Valeurs : Titre de l’album, artiste, date de sortie
        """
        # Vérification que le nom de l'album est fourni
        if not album_name:
            raise Exception('Un nom d’album valide doit être fourni')

        album_data = {}

        # Appel à la fonction de recherche pour récupérer les données de l'album
        data = self.search(album_name, APIQueryType.ALBUM)

        # Extraction des informations pertinentes à partir de la réponse de l'API
        for album in data['albums']['items']:
            # Comparaison insensible à la casse pour trouver l'album exact
            if album['name'].lower() == album_name.lower():
                album_info = {
                    'Album': album['name'],
                    'Artiste': album['artists'][0]['name'],
                    'Date de sortie': album['release_date']
                }
                # Ajout de l'album au dictionnaire avec son ID unique
                album_data[album['id']] = album_info

        # Si aucune donnée n'est trouvée pour cet album, afficher un message
        if not album_data:
            print('Aucune donnée sur cet album n’a été trouvée sur Spotify.')
            return {}

        # Sauvegarde des informations de l'album dans un fichier JSON
        self.save_to_json(album_data, self.chemin_album_json)

    def get_track_info(self, track_name: str):
        """
            Fonction qui récupère les informations d’un titre via l'API Spotify.

            Paramètre :
            - track_name : str : Le nom du titre à rechercher.

            Retour :
            - dict : Un dictionnaire contenant les informations du titre, avec :
                - Clé : ID unique Spotify du titre
                - Valeurs : Titre, artiste, album
        """
        # Vérification que le nom du titre est fourni
        if not track_name:
            raise Exception('Un nom de titre valide doit être fourni')

        track_data = {}

        # Appel à la fonction de recherche pour récupérer les données du titre
        data = self.search(track_name, APIQueryType.TRACK)

        # Extraction des informations pertinentes à partir de la réponse de l'API
        for track in data['tracks']['items']:
            # Comparaison insensible à la casse pour trouver le titre exact
            if track['name'].lower() == track_name.lower():
                track_info = {
                    'Titre': track['name'],
                    'Artiste': track['artists'][0]['name'],
                    'Album': track['album']['name']
                }
                # Ajout du titre au dictionnaire avec son ID unique
                track_data[track['id']] = track_info

        # Si aucune donnée n'est trouvée pour ce titre, afficher un message
        if not track_data:
            print('Aucune donnée sur ce titre n’a été trouvée sur Spotify.')
            return {}

        # Sauvegarde des informations du titre dans un fichier JSON
        self.save_to_json(track_data, self.chemin_track_json)

    def lire_fichier_json(self, filename: str) -> dict:
        """
            Fonction qui lit les données d'un fichier JSON et les retourne sous forme de dictionnaire.

            Paramètre :
            - filename : str : 

            Retour :
            - dict : Dictionnaire contenant les données du fichier JSON.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Le fichier {filename} n'existe pas.")
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Données chargées depuis le fichier {filename}")
        return data

    def afficher_artiste_infos(self) -> str:
        """
            Fonction qui récupère et retourne les informations sur les artistes depuis un fichier JSON.

            Paramètre :
            - 

            Retour :
            - str : Une chaîne contenant les informations des artistes ou un message d'erreur.
        """
        try:
            # Lecture des données JSON depuis le fichier
            data = self.lire_fichier_json(self.chemin_artist_json)
            
            # Liste pour accumuler les informations des artistes
            artiste_infos_list = []
            
            # Collecte des informations de chaque artiste
            for item_id, info in data.items():
                # Formater les genres en liste numérotée
                genres = info.get("Genres", [])
                genres_list = "\n\t".join(f"{i + 1}. {genre}" for i, genre in enumerate(genres))

                artiste_infos = {
                    "\n\n**************": "**************",
                    "\n\nArtiste": info.get('Artiste', 'N/A'),
                    "\n\nPopularité": info.get('popularity', 'N/A'),
                    "\n\nType": info.get('type', 'N/A'),
                    "\n\nFollowers": info.get('Followers', 'N/A'),
                    "\n\nGenres": "\n\t" + genres_list  # Utiliser la liste numérotée pour les genres
                }
                artiste_infos_list.append(artiste_infos)

            # Formater les informations pour le retour
            artiste_infos_str = "\n\n".join(
                "\n".join(f"{key} : {value}" for key, value in artiste.items()) for artiste in artiste_infos_list
            )
            
            return artiste_infos_str  # Retourne les informations des artistes en chaîne formatée
                
        except FileNotFoundError as e:
            return f"Erreur : {str(e)}"
        except json.JSONDecodeError:
            return "Erreur : Le fichier JSON est corrompu ou mal formaté."

    def afficher_album_infos(self) -> str:
        """
            Fonction qui récupère et retourne les informations sur les albums depuis un fichier JSON.

            Paramètre :
            - 

            Retour :
            - str : Une chaîne contenant les informations des albums ou un message d'erreur.
        """
        try:
            # Lecture des données JSON depuis le fichier
            data = self.lire_fichier_json(self.chemin_album_json)
            
            # Liste pour stocker les informations des albums
            album_infos_list = []
            
            # Collecte des informations de chaque album
            for album_id, album_info in data.items():
                album_infos = {
                    "\n\n**************":"**************",
                    "\n\nAlbum": album_info.get('Album', 'N/A'),
                    "\n\nArtiste": album_info.get('Artiste', 'N/A'),
                    "\n\nDate de sortie": album_info.get('Date de sortie', 'N/A')
                }
                album_infos_list.append(album_infos)

            # Formater les informations pour le retour
            album_infos_str = "\n\n".join(
                "\n".join(f"{key} : {value}" for key, value in album.items()) for album in album_infos_list
            )
            
            return album_infos_str  # Retourne les informations des albums en chaîne formatée
                
        except FileNotFoundError as e:
            return f"Erreur : {str(e)}"
        except json.JSONDecodeError:
            return "Erreur : Le fichier JSON est corrompu ou mal formaté."

    def afficher_track_infos(self) -> str:
        """
            Fonction qui récupère et retourne les informations sur les pistes depuis un fichier JSON.

            Paramètre :
            - 

            Retour :
            - str : Une chaîne contenant les informations des pistes ou un message d'erreur.
        """
        try:
            # Lecture des données JSON depuis le fichier
            data = self.lire_fichier_json(self.chemin_track_json)
            
            # Liste pour stocker les informations des pistes
            track_infos_list = []
            
            # Collecte des informations de chaque piste
            for track_id, track_info in data.items():
                track_infos = {
                    "\n\n**************":"**************",
                    "\n\nTitre": track_info.get('Titre', 'N/A'),
                    "\n\nArtiste": track_info.get('Artiste', 'N/A'),
                    "\n\nAlbum": track_info.get('Album', 'N/A')
                }
                track_infos_list.append(track_infos)

            # Formater les informations pour le retour
            track_infos_str = "\n\n".join(
                "\n".join(f"{key} : {value}" for key, value in track.items()) for track in track_infos_list
            )
            
            return track_infos_str  # Retourne les informations des pistes en chaîne formatée
                
        except FileNotFoundError as e:
            return f"Erreur : {str(e)}"
        except json.JSONDecodeError:
            return "Erreur : Le fichier JSON est corrompu ou mal formaté."

"""
if __name__ == "__main__":
    # Exemple d’utilisation : création d’une instance et appel de méthodes
    fetcher = Fetcher()

    # Récupération d’informations sur un artiste (par exemple)
    # artist_info = fetcher.get_artist_info("DRAKE")
    # album_info = fetcher.get_album_info("ASTROWORLD")
    track_info = fetcher.get_track_info("WITHOUT ME")
    print("********************************************************************")
    # fetcher.afficher_Artiste_infos()
    # print("********************************************************************")
    # fetcher.afficher_Album_infos()
    # print("********************************************************************")
    fetcher.afficher_track_infos()
    print("********************************************************************")


"""