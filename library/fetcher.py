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
        
        # Variables de classe pour les requêtes
        self.client_id = "45a8a345769d4ac0b91d95622d331f05"
        self.client_secret = "1fc622291bbd48f487b2375179fcbc23"
        self.authorization_token = None
        self.token_url = 'https://accounts.spotify.com/api/token'
        self.spotify_api_url = 'https://api.spotify.com/v1'

        # Chemins vers les fichiers JSON où les données seront sauvegardées
        self.chemin_artist_json = os.path.abspath(r"Python_project\\json_Dir\\artist_json.json")
        self.chemin_album_json = os.path.abspath(r"Python_project\\json_Dir\\album_json.json")
        self.chemin_track_json = os.path.abspath(r"Python_project\\json_Dir\\track_json.json")

        # Vérification si la connexion Internet est disponible au démarrage
        self.check_internet_and_authorize()

    def check_internet_and_authorize(self):
        """
        Vérifie si une connexion Internet est disponible et tente d'obtenir un jeton d'authentification si possible.
        """
        if self.is_internet_available():
            print("Connexion Internet détectée. Tentative d'autorisation...")
            self.authorize_client()
        else:
            print("Aucune connexion Internet. Impossible d'accéder à l'API Spotify.")
    
    def is_internet_available(self):
        """
        Vérifie si une connexion Internet est disponible en envoyant une requête à Google.
        """
        try:
            response = requests.get("https://www.google.com", timeout=5)
            return True
        except requests.ConnectionError:
            return False

    def authorize_client(self) -> bool:
        """
        Récupère un jeton d'authentification et autorise l'accès à l'API Spotify.
        Retourne un booléen indiquant si l'authentification a réussi.
        """
        if self.authorization_token and self.token_is_valid():
            print("Token déjà valide")
            return True

        client_credentials = f'{self.client_id}:{self.client_secret}'
        client_credentials_b64 = base64.b64encode(client_credentials.encode())

        token_data = {'grant_type': 'client_credentials'}
        token_headers = {'Authorization': f'Basic {client_credentials_b64.decode()}'}

        request = requests.post(url=self.token_url, data=token_data, headers=token_headers)

        if request.status_code not in range(200, 299):
            raise Exception(f'Échec de l’authentification : code {request.status_code}')

        token_response_data = request.json()
        self.authorization_token = token_response_data['access_token']
        self.token_expiry_time = time.time() + token_response_data['expires_in']  # Store expiry time
        print(f'Client autorisé avec succès !')
        return True

    def token_is_valid(self):
        return time.time() < self.token_expiry_time


    def search(self, query: str, query_type: APIQueryType) -> dict:
        """
        Effectue une recherche dans l'API Spotify selon le type de requête.
        Gère les erreurs de connexion et réessaie si nécessaire.
        """
        if not isinstance(query_type, APIQueryType):
            raise Exception('Type de requête invalide !')

        if not self.authorization_token:
            print("Erreur : Client non autorisé. Impossible de récupérer les informations.")
            return {}

        headers = {'Authorization': f'Bearer {self.authorization_token}'}
        endpoint = self.spotify_api_url + '/search?'
        data = urlencode({'q': query, 'type': query_type.value})
        search_url = f'{endpoint}{data}'

        try:
            request = requests.get(search_url, headers=headers)
            request.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
        except requests.RequestException as e:
            print(f"Erreur réseau : {e}")
            if not self.is_internet_available():
                print("Aucune connexion Internet. Impossible de poursuivre la recherche.")
            else:
                print("Tentative de réessayer après une courte pause...")
                time.sleep(5)  # Attente avant réessayer
                return self.search(query, query_type)  # Réessayer la recherche

        return request.json()
    
    def save_to_json(self, data: dict, filename: str) -> None:
        """
        Enregistre les données dans un fichier JSON.
        """
        # Vérifie si le dossier existe et le crée si nécessaire
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Données enregistrées dans le fichier {filename}")

    def get_artist_info(self, artist_name: str) :
        """
            Récupère les informations d’un artiste via l'API Spotify.

            :param artist_name: Le nom de l’artiste à rechercher.
            :return: Un dictionnaire contenant les informations de l’artiste :
                    - Clé : ID unique Spotify.
                    - Valeurs : Nom de l’artiste, nombre de followers, genres.
        """
        if not artist_name:
            raise Exception('Un nom d’artiste valide doit être fourni')

        artist_data = {}

        # Appel à la fonction de recherche
        data = self.search(artist_name, APIQueryType.ARTIST)

        # Extraction des informations pertinentes
        for artist in data['artists']['items']:
            if artist['name'].lower() == artist_name.lower():
                artist_info = {
                    'Artiste': artist['name'],
                    'popularity': artist['popularity'],
                    'type': artist['type'],
                    'Followers': artist.get('followers', {}).get('total', 'Données non disponibles'),
                    'Genres': artist['genres']
                }
                artist_data[artist['id']] = artist_info

        if not artist_data:
            print('Aucune donnée sur cet artiste n’a été trouvée sur Spotify.')
            return {}
        
        # varArtist = str(artist_data).replace("'", "\"")
        self.save_to_json(artist_data,self.chemin_artist_json)
        # return varArtist

    def get_album_info(self, album_name: str):
        """
            Récupère les informations d’un album via l'API Spotify.

            :param album_name: Le nom de l’album à rechercher.
            :return: Un dictionnaire contenant les informations de l’album :
                    - Clé : ID unique Spotify.
                    - Valeurs : Titre de l’album, artiste, date de sortie.
        """
        if not album_name:
            raise Exception('Un nom d’album valide doit être fourni')

        album_data = {}

        # Appel à la fonction de recherche
        data = self.search(album_name, APIQueryType.ALBUM)

        # Extraction des informations pertinentes
        for album in data['albums']['items']:
            if album['name'].lower() == album_name.lower():
                album_info = {
                    'Album': album['name'],
                    'Artiste': album['artists'][0]['name'],
                    'Date de sortie': album['release_date']
                }
                album_data[album['id']] = album_info

        if not album_data:
            print('Aucune donnée sur cet album n’a été trouvée sur Spotify.')
            return {}
        # varAlbum = str(album_data).replace("'", "\"")
        self.save_to_json(album_data,self.chemin_album_json)
        # return varAlbum

    def get_track_info(self, track_name: str):
        """
            Récupère les informations d’un titre via l'API Spotify.

            :param track_name: Le nom du titre à rechercher.
            :return: Un dictionnaire contenant les informations du titre :
                    - Clé : ID unique Spotify.
                    - Valeurs : Titre, artiste, album.
        """
        if not track_name:
            raise Exception('Un nom de titre valide doit être fourni')

        track_data = {}

        # Appel à la fonction de recherche
        data = self.search(track_name, APIQueryType.TRACK)

        # Extraction des informations pertinentes
        for track in data['tracks']['items']:
            if track['name'].lower() == track_name.lower():
                track_info = {
                    'Titre': track['name'],
                    'Artiste': track['artists'][0]['name'],
                    'Album': track['album']['name']
                }
                track_data[track['id']] = track_info

        if not track_data:
            print('Aucune donnée sur ce titre n’a été trouvée sur Spotify.')
            return {}
        # varTrack= str(track_data).replace("'", "\"")
        self.save_to_json(track_data,self.chemin_track_json)
        # return varTrack

    def lire_fichier_json(self, filename: str) -> dict:
        """
        Lit les données d'un fichier JSON et les retourne sous forme de dictionnaire.
        
        :return: Dictionnaire contenant les données du fichier JSON.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Le fichier {filename} n'existe pas.")
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Données chargées depuis le fichier {filename}")
        return data

    def afficher_artiste_infos(self) -> str:
        """
        Récupère et retourne les informations sur les artistes depuis un fichier JSON.

        :return: Une chaîne contenant les informations des artistes ou un message d'erreur.
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
        Récupère et retourne les informations sur les albums depuis un fichier JSON.
        
        :return: Une chaîne contenant les informations des albums ou un message d'erreur.
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
        Récupère et retourne les informations sur les pistes depuis un fichier JSON.
        
        :return: Une chaîne contenant les informations des pistes ou un message d'erreur.
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
