#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import base64
import json
import requests
from APIQueryType import APIQueryType
from urllib.parse import urlencode


class Fetcher:
    # Variables de classe pour les requêtes
    client_id = "45a8a345769d4ac0b91d95622d331f05"
    client_secret = "1fc622291bbd48f487b2375179fcbc23"
    authorization_token = None
    token_url = 'https://accounts.spotify.com/api/token'
    spotify_api_url = 'https://api.spotify.com/v1'

    def __init__(self, client_id: str, client_secret: str):
        """
        Initialise la classe avec l'ID client et le secret client.
        Puis tente d'autoriser le client avec l'API Spotify.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.authorize_client()


    def authorize_client(self) -> bool:
        """
            Récupère un jeton d'authentification et autorise l'accès à l'API Spotify.
            Retourne un booléen indiquant si l'authentification a réussi.

            :return: True si le client est autorisé, False en cas d'échec.
        """
        # Création des identifiants client encodés en base64
        client_credentials = f'{self.client_id}:{self.client_secret}'
        client_credentials_b64 = base64.b64encode(client_credentials.encode())

        # Données et en-têtes pour la requête d'authentification
        token_data = {'grant_type': 'client_credentials'}
        token_headers = {'Authorization': f'Basic {client_credentials_b64.decode()}'}

        # Envoi de la requête pour obtenir le jeton d'accès
        request = requests.post(url=self.token_url, data=token_data, headers=token_headers)

        # Vérification du statut de la réponse
        if request.status_code not in range(200, 299):
            raise Exception(f'Échec de l’authentification : code {request.status_code}')

        # Stockage du jeton d'accès
        token_response_data = request.json()
        self.authorization_token = token_response_data['access_token']
        print(f'Client autorisé avec succès !')
        return True


    def search(self, query: str, query_type: APIQueryType) -> dict:
        """
            Effectue une recherche dans l'API Spotify selon le type de requête.

            :param query: La chaîne de recherche (artiste, album ou titre).
            :param query_type: Le type de recherche {'artist', 'album', 'track'}.
            :return: Les résultats de la recherche au format JSON.
        """
        if not isinstance(query_type, APIQueryType):
            raise Exception('Type de requête invalide !')

        # Configuration de la requête avec les en-têtes d’autorisation
        headers = {'Authorization': f'Bearer {self.authorization_token}'}
        endpoint = self.spotify_api_url + '/search?'
        data = urlencode({'q': query, 'type': query_type.value})
        search_url = f'{endpoint}{data}'

        # Envoi de la requête et retour des résultats en JSON
        request = requests.get(search_url, headers=headers)
        if request.status_code not in range(200, 299):
            raise Exception(f'Requête échouée avec le code : {request.status_code}')

        return request.json()


    def get_artist_info(self, artist_name: str) -> dict:
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
                    'Followers': artist.get('followers', {}).get('total', 'Données non disponibles'),
                    'Genres': artist['genres']
                }
                artist_data[artist['id']] = artist_info

        if not artist_data:
            print('Aucune donnée sur cet artiste n’a été trouvée sur Spotify.')
            return {}
        
        varArtist = str(artist_data).replace("'", "\"")

        return varArtist


    def get_album_info(self, album_name: str) -> dict:
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
        varAlbum = str(album_data).replace("'", "\"")

        return varAlbum


    def get_track_info(self, track_name: str) -> dict:
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
        varTrack= str(track_data).replace("'", "\"")

        return varTrack


if __name__ == "__main__":
    # Exemple d’utilisation : création d’une instance et appel de méthodes
    fetcher = Fetcher("45a8a345769d4ac0b91d95622d331f05", "1fc622291bbd48f487b2375179fcbc23")

    # Récupération d’informations sur un artiste (par exemple)
    artist_info = fetcher.get_artist_info("EMINEM")
    album_info = fetcher.get_album_info("DISSIMULATION")
    track_info = fetcher.get_track_info("WITHOUT ME")
    print("track_info*********************************************************")
    print(track_info)
    print("album_info*********************************************************")
    print(album_info)
    print("artist_info*********************************************************")
    print(artist_info)
    print("********************************************************************")

