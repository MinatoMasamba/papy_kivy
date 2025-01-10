import requests


class UserStatus:
    """
    Classe pour vérifier l'état de connexion de l'utilisateur.
    """
    def __init__(self, token):
        self.base_url = 'http://127.0.0.1:8000/api/status/'  # URL de l'API
        self.token = token  # Jeton d'authentification de l'utilisateur

    def is_connected(self):
        """
        Vérifie si l'utilisateur est connecté.
        Retourne un dictionnaire avec les informations de connexion.
        """
        headers = {
            'Authorization': f'Token {self.token}'  # Ajoute le jeton dans les en-têtes
        }
        try:
            response = requests.get(self.base_url, headers=headers)
            if response.status_code == 200:
                return response.json()  # Retourne la réponse JSON
            else:
                return {
                    "connected": False,
                    "message": f"Erreur : {response.status_code} - {response.reason}"
                }
        except requests.RequestException as e:
            return {"connected": False, "message": f"Erreur de requête : {e}"}

import requests
import json

class CREAT:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.register_user()

    def register_user(self):
        data = {
            "username": self.username,
            "password": self.password,
            "email": f"{self.username}@example.com",  # Un email par défaut pour cet exemple
            "first_name": self.username,
            "last_name": "Test",
            "promotion": "2024"
        }
        url = "http://127.0.0.1:8000/api/enregistrer/"
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(url, headers=headers, json=data)
            print(f"Requête envoyée : {json.dumps(data, indent=2)}")
            print(f"Statut de la réponse : {response.status_code}")
            print(f"Contenu de la réponse : {response.content.decode('utf-8')}")
            if response.status_code == 200:
                return response.json()
            else:
                return {"success": False, "message": "Erreur de connexion"}
        except requests.RequestException as e:
            print(f"Erreur lors de l'envoi de la requête : {e}")
            return {"success": False, "message": f"Erreur : {e}"}




import requests

class Logout:
    def __init__(self, token):
        """
        Initialise la classe avec le jeton d'authentification de l'utilisateur.
        :param token: Le jeton d'authentification de l'utilisateur (string)
        """
        self.token = token

    def logout(self):
        """
        Envoie une requête POST au serveur pour se déconnecter.
        :return: Réponse du serveur sous forme de dictionnaire.
        """
        logout_url = 'http://127.0.0.1:8000/api/se-deconnecter/'
        headers = {'Authorization': f'Token {self.token}'}

        try:
            response = requests.post(logout_url, headers=headers)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                return {"success": False, "message": "Déconnexion impossible, jeton invalide ou session expirée."}
            else:
                return {"success": False, "message": "Erreur de déconnexion. Réessayez plus tard."}
        except requests.RequestException as e:
            return {"success": False, "message": f"Erreur de connexion au serveur : {e}"}

        

import requests
import requests
import requests

class UserProfile:
    def __init__(self, token):
        """
        Initialiser la classe avec un jeton d'authentification.
        :param token: Jeton d'authentification pour l'utilisateur.
        """
        self.token = token
        self.headers = {"Authorization": f"Token {self.token}"}
        self.api_base_url = "http://127.0.0.1:8000/api/profile/"

    def get_profile(self):
        """
        Récupérer le profil de l'utilisateur connecté.
        :return: Dictionnaire contenant les données du profil ou un message d'erreur.
        """
        url = f"{self.api_base_url}"
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                print(f'profile reçu du sereveur {response.json()}')
                return response.json()
            else:
                return {"success": False, "message": f"Erreur: {response.status_code} {response.text}"}
        except requests.RequestException as e:
            return {"success": False, "message": f"Erreur réseau : {e}"}

    def update_profile(self, profile_data=None, photo_file=None):
        """
        Met à jour le profil utilisateur avec les données fournies et éventuellement une photo de profil.
        :param profile_data: Dictionnaire contenant les données du profil.
        :param photo_file: Chemin vers le fichier photo à télécharger.
        :return: Réponse JSON du serveur si succès, None sinon.
        """
        update_profile_url = 'http://127.0.0.1:8000/api/profile/'
        headers = self.headers
        data = profile_data if profile_data else {}

        try:
            if photo_file:
                print('Un fichier est choisi pour être envoyé.')
                with open(photo_file, "rb") as file:
                    files = {'photo': file}
                    print(f"Envoi du fichier {photo_file} avec les données du profil.")
                    response = requests.put(update_profile_url, headers=headers, data=data, files=files)
            else:
                response = requests.put(update_profile_url, headers=headers, data=data)

            #print(f"Statut de la réponse: {response.status_code}")
            #print(f"Texte de la réponse: {response.text}")

            if response.status_code == 200:
                print("Profil mis à jour avec succès.")
                return response.json()
            else:
                print(f"Erreur : {response.status_code} - {response.text}")
        except FileNotFoundError:
            print("Erreur : Fichier non trouvé.")
        except Exception as e:
            print(f"Erreur : {e}")
        return None



import requests

class PostManager:
    BASE_URL = "http://127.0.0.1:8000/posts/"  # Remplacez par l'URL de votre API
    from creat import UserProfile
    from userdata import UserDatabase
    from connection import ConnectionUserManager

    get_token = UserDatabase('local_storage.db')
    nom = ConnectionUserManager()
    user = nom.get_connection_user()
    token = get_token.get_user_token(user)
    print(f'token {token}')

    def __init__(self, auth_token=None):
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def get_posts(self):
        """
        Récupère tous les posts disponibles depuis l'API.
        """
        try:
            response = requests.get(self.BASE_URL, headers=self.headers)
            if response[0]!={}:
                response.raise_for_status()  # Lève une exception pour les codes d'erreur HTTP
                return response.json()  # Convertir la réponse en JSON
            else:
                return 'en_attente'
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la récupération des posts : {e}")
            return None

    def create_post(self, title, content, file_path=None, is_public=True):

        """
        Crée un nouveau post avec un fichier via l'API.
        """
        data = {
            "title": title,
            "content": content,
            "is_public": is_public
        }
        files = {}

        if file_path:
            # Ajoute le fichier à la requête
            try:
                file = open(file_path, 'rb')
                files['file'] = (file_path.split('/')[-1], file)
            except FileNotFoundError:
                print(f"Le fichier '{file_path}' est introuvable.")
                return None

        try:
            response = requests.post(self.BASE_URL, headers=self.headers, data=data, files=files)
            response.raise_for_status()  # Lève une exception pour les erreurs HTTP
            return response.json()  # Convertir la réponse en JSON
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la création du post : {e}")
            return None
        finally:
            # Ferme le fichier s'il existe
            if files:
                file.close()

