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
     # if the request is invalid handle failure
        if request.status_code not in range(200, 299):
            raise Exception(f'Failed to authenticate client with error code: {request.status_code}')