#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests

class Fetcher:
    def __init__(self):
        self.client_id = "45a8a345769d4ac0b91d95622d331f05"
        self.client_secret = "1fc622291bbd48f487b2375179fcbc23"
    

    def getclientid(self):
        return self.client_id
    
    def  getclientsecret(self):
        return self.client_secret
    
    def get_acces_token(self):
        """Fonction get_acess_token
        renvoie un string qui correspondra au jeton de l'api pour faire les requêtes valable 1h"""
        url = 'https://accounts.spotify.com/api/token' #url d'entrée pour la requête
        data = {'grant_type': 'client_credentials', 'client_id' : '45a8a345769d4ac0b91d95622d331f05', 'client_secret' : '1fc622291bbd48f487b2375179fcbc23'} #paramêtres de la requête
        headers = {'Content-Type' : 'application/x-www-form-urlencoded'} #contenu du header pour le type de données
        response = requests.post(url=url, headers=headers, data=data) #requête du jeton d'authentification
        status = response.status_code #renvoie le status de la requête 200 si tout va bien
        if status == 200: #verifie que la requête s'est bien passé
            response  = response.json() #renvoie reponse en format json
        access_token = response['access_token'] #recupère uniquement le jeton d'authentification
        return access_token #renvoie le jeton d'authentification
    
    def necessaryId(name: str, type : str):
        """Fonction qui vérifie bien si on a l'id de l'album ou du titre dont on veut récupérer les données
        Sinon demander à  l'utilisateur de preciser ou de données un nom de titre"""
        if type == 'album':
            return True
        elif type == 'song':
            return False
        else:
            return 'Not a song or an Album'

if __name__ == "__main__":
    data = Fetcher()
    d = data.get_acces_token()
    print(d)