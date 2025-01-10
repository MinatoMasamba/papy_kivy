import requests
import json
import sqlite3
from datetime import datetime, timedelta
from creat import CREAT,UserProfile,Logout,UserStatus  # Import de la classe CREAT
import os
import psutil
import os
from userdata import UserDatabase
from connection import ConnectionUserManager
def is_file_in_use(file_path):
    """Vérifie si le fichier est utilisé par un autre processus."""
    for proc in psutil.process_iter(attrs=['pid', 'name', 'open_files']):
        try:
            for file in proc.info['open_files'] or []:
                if file_path == file.path:
                    return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False
class UserAuth:
    def __init__(self):
        self.base_des_donnes = 'local_storage.db'
        self.db = sqlite3.connect(self.base_des_donnes)
        self.token = None
        self.create_tables()
        self.logout_compte()
        self.add_column_email()
        self.add_column_token_expiration()  # Appel de la méthode pour ajouter la colonne
        self.add_column_logged_in()

        # Vérifiez l'état de connexion au démarrage


    def verify_login_status(self):
        user_data = self.get_stored_credentials()
        if user_data and user_data['logged_in']:
            print("Utilisateur connecté : ", user_data['username'])
            return True
        else:
            print("Aucun utilisateur connecté.")
            return False

    def create_tables(self):
        with self.db:
            self.db.execute('''
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,  
                    password TEXT,
                    token TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    token_expiration DATETIME DEFAULT '1970-01-01 00:00:00',
                    logged_in BOOLEAN DEFAULT 0
                );

            ''')

        #print("Les données de la table 'user' ont été réinitialisées.")


    def add_column_token_expiration(self):
        # Ajouter la colonne token_expiration si elle n'existe pas déjà
        with self.db:
            try:
                self.db.execute('ALTER TABLE user ADD COLUMN token_expiration DATETIME')
            except sqlite3.OperationalError:
                pass  # La colonne existe déjà

    def add_column_logged_in(self):
        # Ajouter la colonne logged_in si elle n'existe pas déjà
        with self.db:
            try:
                self.db.execute('ALTER TABLE user ADD COLUMN logged_in BOOLEAN DEFAULT False')
                self.db.commit()
            except sqlite3.OperationalError:
                pass  # La colonne existe déjà

    def login(self, username, password):
        login_url = 'http://127.0.0.1:8000/api/se-connecter/'
        data = {'username': username, 'password': password}
        response = requests.post(login_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            response_data = response.json()
            self.token = response_data.get('token')
            print('Token reçu du serveur:', self.token)
            first_name = response_data.get('first_name')
            last_name = response_data.get('last_name')
            token_expiration = datetime.now() + timedelta(hours=1)  # Supposons que le token expire dans 1 heure

            if self.token:
                with self.db:
                    # Remplace les données existantes pour l'utilisateur
                    self.db.execute('''
                        INSERT INTO user (username, password, token, first_name, last_name, token_expiration, logged_in)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(username) DO UPDATE SET 
                            password = excluded.password,
                            token = excluded.token,
                            first_name = excluded.first_name,
                            last_name = excluded.last_name,
                            token_expiration = excluded.token_expiration,
                            logged_in = excluded.logged_in
                    ''', (username, password, self.token, first_name, last_name, token_expiration, True))
                    self.login_compte()
                    user = ConnectionUserManager()
                    user.set_connection_user(username)
                return True

        return False






    def logout(self):
        get_token = UserDatabase('local_storage.db')
        nom = ConnectionUserManager()
        user = nom.get_connection_user()
        token = get_token.get_user_token(user)
        """Déconnecte l'utilisateur et supprime la base de données."""
        with self.db:
            self.db.execute('''
                UPDATE user 
                SET token = NULL, token_expiration = NULL, logged_in = False
            ''')
            self.db.commit()

            if token :
                Logout_user = Logout(token)
                Logout_user.logout()


        
        print("Utilisateur déconnecté avec succès.")


    def is_logged_in(self):
        """
        Vérifie si un utilisateur est actuellement connecté.
        """
        credentials = self.get_stored_credentials() 
        #etat = UserStatus(credentials['token'])
        if credentials:
            print(credentials)
        else:
            print(f'etat non scriptable')
        #print(etat.is_connected())
        #user_data = etat.is_connected()
        return None
    def login_compte(self): 
        """ Mettre à jour la colonne logged_in à True. """ 
        with self.db: 
            self.db.execute(''' UPDATE user SET logged_in = True ''')
            self.db.commit()

    def logout_compte(self): 
        """ Mettre à jour la colonne logged_in à False. """ 
        with self.db: 
            self.db.execute(''' UPDATE user SET logged_in = False ''')


    def get_stored_credentials(self):
        with self.db:
            cursor = self.db.cursor()
            cursor.execute('SELECT username, password, token, first_name, last_name, token_expiration, logged_in FROM user')
            user_data = cursor.fetchone()
            
  # Vérifie ce que tu récupères

            if user_data:
                token_expiration = user_data[5] if user_data[5] else '1970-01-01 00:00:00'
                return {
                    'username': user_data[0],
                    'password': user_data[1],
                    'token': user_data[2],
                    'first_name': user_data[3],
                    'last_name': user_data[4],
                    'token_expiration': token_expiration,
                    'logged_in': bool(user_data[6])
                }
            return None




    def refresh_token_if_needed(self):
        user_data = self.get_stored_credentials()
        if user_data and user_data.get('logged_in'):
            try:
                # Essayer de convertir avec fractions de secondes
                token_expiration = datetime.strptime(user_data['token_expiration'], '%Y-%m-%d %H:%M:%S.%f')
            except ValueError:
                # Revenir au format sans fractions de secondes
                token_expiration = datetime.strptime(user_data['token_expiration'].split('.')[0], '%Y-%m-%d %H:%M:%S')
            
            # Vérifier si le token a expiré
            if datetime.now() >= token_expiration:
                return self.login(user_data['username'], user_data['password'])
        return False


    def creat(self, username, password):
        # Créer une instance de CREAT
        creat_instance = CREAT(username, password)

            # Connecter l'utilisateur automatiquement après la création du compte
        self.login(username, password)
        print("Utilisateur et profil créés avec succès.")
        return {"success": True, "message": "Utilisateur et profil créés avec succès."}



    def list_users(self):
        """ Liste tous les utilisateurs dans la base de données locale. """ 
        with self.db: 
            cursor = self.db.cursor() 
            cursor.execute('SELECT username FROM user') 
            users = cursor.fetchall()
            if users:
                return users
    def get_profile(self):
        get_token = UserDatabase('local_storage.db')
        nom = ConnectionUserManager()
        user = nom.get_connection_user()
        token = get_token.get_user_token(user)
        if token: 
            profile_manager = UserProfile(token) 
            return profile_manager.get_profile() 
         
        return {"success": False, "message": "Utilisateur non connecté"}
                
    def update_profile(self, profile_data, photo_file=None):
        get_token = UserDatabase('local_storage.db')
        nom = ConnectionUserManager()
        user = nom.get_connection_user()
        token = get_token.get_user_token(user)
        """ Mettre à jour le profil de l'utilisateur connecté. """ 
        credentials = self.get_stored_credentials() 
        if token: 
            profile_manager = UserProfile(token)
            result = profile_manager.update_profile(profile_data, photo_file) 
            if result: # Mettre à jour les informations du profil dans la base de données locale 
                with self.db: self.db.execute(''' UPDATE user SET first_name = ?, last_name = ?, email = ? WHERE username = ? ''', 
                                            (profile_data.get('first_name', credentials['first_name']), 
                                            profile_data.get('last_name', credentials['last_name']), 
                                            profile_data.get('email', ''), credentials['username'])) 
                self.db.commit()

            return result 
        return {"success": False, "message": "Utilisateur non connecté ou informations d'identification manquantes."}
    
    def add_column_email(self): # Ajouter la colonne email si elle n'existe pas déjà 
        with self.db: 
            try: 
                self.db.execute('ALTER TABLE user ADD COLUMN email TEXT') 
            except sqlite3.OperationalError: 
                pass

    def recreate_tables(self):
        with self.db:
            self.db.execute('DROP TABLE IF EXISTS user')
            
data = {

            'numero_whatsapp': '0851597918'
        }
# Exemple d'utilisation
user_auth = UserAuth()
credentials=user_auth.get_stored_credentials()
#if user_auth.list_users():
    #print(f'{user_auth.list_users()}')
#else:
    #print('rien')
# Vérification de l'état de connexion
profile = UserProfile('1f5582b1977944b2f78e988932ef3e588a4d6cc6')
#profile_data = profile.update_profile(profile_data=None,photo_file='car1.jpg')
#if profile:
#    print(f"profile{profile}")
#else:
#    print("Aucun profile trouver.")

# Connexion
#if user_auth.login("minato", "123456789"):
#    print("Connecté avec succès.")
#else:
#    print('non connecter')

# Déconnexion
#user_auth.logout()


import requests

class PostsAndSocialInteractions:
    def __init__(self, auth):
        """
        Initialise la classe avec une instance d'authentification.
        :param auth: Instance pour gérer l'authentification et les tokens utilisateur.
        """
        self.auth = auth if auth else UserAuth()

    def create_post(self, detail, file_path=None):
        from creat import UserProfile
        from userdata import UserDatabase
        from connection import ConnectionUserManager

        get_token = UserDatabase('local_storage.db')
        nom = ConnectionUserManager()
        user = nom.get_connection_user()
        token = get_token.get_user_token(user)
        """
        Crée un nouveau post avec ou sans fichier.
        :param detail: Contenu du post.
        :param file_path: Chemin vers le fichier à joindre (optionnel).
        :return: JSON de la réponse si succès, None sinon.
        """
        user_data = self.auth.get_stored_credentials()
        print(f'authentification ok ')
        if user_data:
            self.auth.refresh_token_if_needed()
            create_post_url = 'http://127.0.0.1:8000/api/post/'
            headers = {'Authorization': f"Token {token}"}
            post_data = {"content": detail}

            try:
                if file_path:
                    print('un fichier est choisi pour etre envoyer')
                    with open(file_path, "rb") as file:
                        files = {'file': file}
                        response = requests.post(create_post_url, data=post_data, files=files, headers=headers)
                else:
                    response = requests.post(create_post_url, data=post_data, headers=headers)

                # Debugging output
                print(f"Status Code: {response.status_code}")
                print(f"Response Text: {response.text}")

                if response.status_code == 201:
                    return response.json()
                else:
                    print(f"Erreur : {response.status_code} - {response.text}")
            except FileNotFoundError:
                print("Erreur : Fichier non trouvé.")
            except Exception as e:
                print(f"Erreur : {e}")
        return None


    def add_to_favorites(self, post_id):
        get_token = UserDatabase('local_storage.db')
        nom = ConnectionUserManager()
        user = nom.get_connection_user()
        token = get_token.get_user_token(user)
        """
        Ajoute un post aux favoris de l'utilisateur.
        :param post_id: ID du post.
        :return: JSON de la réponse si succès, None sinon.
        """
        user_data = self.auth.get_stored_credentials()
        send = self.auth.get_profile()
        send_data = {
            'favorite':''
        }
        if user_data:
            self.auth.refresh_token_if_needed()
            add_fav_url = f'http://127.0.0.1:8000/api/post/{post_id}/favorite/'
            headers = {'Authorization': f"Token {token}"}
            response = requests.post(add_fav_url, headers=headers,data=send_data)
            if response.status_code == 200:
                return response.json()
        return None

    def comment_on_post(self, post_id, comment):
        """
        Ajoute un commentaire à un post.
        :param post_id: ID du post.
        :param comment: Texte du commentaire.
        :return: JSON de la réponse si succès, None sinon.
        """
        user_data = self.auth.get_stored_credentials()
        if user_data:
            self.auth.refresh_token_if_needed()
            comment_url = f'http://127.0.0.1:8000/api/post/{post_id}/comment/'
            headers = {'Authorization': f"Token {user_data['token']}"}
            comment_data = {"content": comment}
            response = requests.post(comment_url, data=comment_data, headers=headers)
            if response.status_code == 201:
                return response.json()
        return None

    def share_post(self, post_id):
        """
        Partage un post en récupérant un lien de partage.
        :param post_id: ID du post.
        :return: JSON contenant le lien de partage si succès, None sinon.
        """
        user_data = self.auth.get_stored_credentials()
        if user_data:
            self.auth.refresh_token_if_needed()
            share_url = f'http://127.0.0.1:8000/api/posts/{post_id}/share/'
            headers = {'Authorization': f"Token {user_data['token']}"}
            response = requests.get(share_url, headers=headers)
            if response.status_code == 200:
                return response.json()
        return None

    def get_all_posts(self):
        get_token = UserDatabase('local_storage.db')
        nom = ConnectionUserManager()
        user = nom.get_connection_user()
        token = get_token.get_user_token(user)
        #print(f'le nom a recuperer pour le token {nom[0]}')
        #token = get_token.get_user_token(nom[0])
        """
        Récupère tous les posts disponibles.
        :return: JSON contenant les posts si succès, None sinon.
        """
        user_data = self.auth.get_stored_credentials()
        #print(f'token de la base des données ',{token})
        if user_data:
            try:
                self.auth.refresh_token_if_needed()
                posts_url = 'http://127.0.0.1:8000/api/post/'
                headers = {'Authorization': f"Token {token}"}
                response = requests.get(posts_url, headers=headers)
                if response.status_code == 200:
                    #print(response.text)
                    return response.json()
            except requests.exceptions.RequestException as e:
                print(f"Erreur lors de la récupération des posts : {e}")
                return None
        return None



import os
import requests


class CoursesAndFiles:
    def __init__(self, base_directory=None, server_url="http://127.0.0.1:8000/api"):
        """
        Initialise la classe avec les informations nécessaires.
        :param auth: Instance de gestion d'authentification.
        :param base_directory: Répertoire local principal.
        :param server_url: URL de base pour récupérer les fichiers du serveur.
        """
        self.auth =UserAuth()
        self.base_directory = base_directory or os.getcwd()
        self.server_url = server_url
        self.category_endpoints = {
            "TP": "tp/",        # Correct : correspond à /api/files/tp/
            "Exams": "examen/",       # Correct : correspond à /api/examen/
            "Notes": "note/",      # Correct : correspond à /api/interro/
            "Courses": "courses/",     # Assurez-vous que ce chemin existe
            "Interro": "interro/"
        }
        # Définir les sous-dossiers pour chaque type de fichiers
        self.sub_directories = {
            "TP": os.path.join(self.base_directory, "TP"),
            "Exams": os.path.join(self.base_directory, "Exams"),
            "Notes": os.path.join(self.base_directory, "Notes"),
            "Courses": os.path.join(self.base_directory, "Courses"),
            "Interro": os.path.join(self.base_directory, "Interro")
        }

        # Créer les dossiers s'ils n'existent pas
        self._create_directories()

    def _create_directories(self):
        """Crée les dossiers pour TP, Exams, Notes et Courses s'ils n'existent pas."""
        for folder in self.sub_directories.values():
            os.makedirs(folder, exist_ok=True)


    def _fetch_server_files(self, category):
        get_token = UserDatabase('local_storage.db')
        nom = ConnectionUserManager()
        user = nom.get_connection_user()
        token = get_token.get_user_token(user)
        """
        Récupère les fichiers d'une catégorie depuis le serveur.
        """

        if token:
            endpoint = self.category_endpoints.get(category)
            if not endpoint:
                raise ValueError(f"Aucun endpoint défini pour la catégorie : {category}")
            
            # Construire l'URL complète
            url = f"{self.server_url}/{endpoint}"
            headers = {'Authorization': f"Token {token}"}
            
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    return response.json()  # Supposé être une liste [{"name": "file.pdf", "url": "http://..."}]
                elif response.status_code == 404:
                    print(f"Erreur 404 : Endpoint introuvable ({url})")
                else:
                    print(f"Erreur {response.status_code} pour {url}: {response.text}")
            except requests.RequestException as e:
                print(f"Erreur réseau lors de la récupération des fichiers : {e}")
        return []

    def _list_local_files(self, category):
        """
        Récupère la liste des fichiers locaux pour une catégorie donnée avec leurs chemins complets.
        :param category: Catégorie (TP, Exams, Notes, Courses).
        :return: Liste des chemins des fichiers locaux pour cette catégorie.
        """
        folder_path = self.sub_directories[category]
        files = []
        for file_name in os.listdir(folder_path):
            full_path = os.path.join(folder_path, file_name)
            if os.path.isfile(full_path):
                files.append(full_path)  # Ajouter le chemin complet du fichier
        return files


    def _download_file(self, url, save_path):
        """
        Télécharge un fichier depuis une URL.
        :param url: URL du fichier à télécharger.
        :param save_path: Chemin où enregistrer le fichier localement.
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            #print(f"Fichier téléchargé avec succès : {save_path}")
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors du téléchargement du fichier depuis {url} : {e}")

    def _sync_files(self, category):
        """
        Synchronise les fichiers locaux et ceux du serveur pour une catégorie donnée.
        :param category: Catégorie (TP, Exams, Notes, Courses).
        """
        local_files = set(self._list_local_files(category))
       # print(f'local_files: {local_files}')
        
        server_files = self._fetch_server_files(category)
        folder_path = self.sub_directories[category]
        #print(f"Server files: {server_files}")
        
        if category == 'TP':
            # Parcourir chaque entrée dans 'server_files' pour traiter les fichiers TP
            for server_file in server_files:
                if 'TP' not in server_file:
                    continue  # Passer à l'élément suivant si 'TP' n'est pas dans cet élément
                
                # Extraire les fichiers de TP
                tp_files = server_file["TP"]
                for tp_file in tp_files:
                    file_url = tp_file["fichier"]
                    file_name = file_url.split("/")[-1]  # Extraire le nom du fichier à partir de l'URL
                    
                    #print(f"Nom du fichier: {file_name}")
                    #print(f"URL du fichier: http://127.0.0.1:8000{file_url}")
                    
                    # Vérifier si le fichier est déjà localement
                    if file_name not in local_files:
                        save_path = os.path.join(folder_path, file_name)
                        #print(f"Téléchargement de {file_name} dans {category}...")
                        self._download_file(f'http://127.0.0.1:8000{file_url}', save_path)

        elif category == 'Exams':

            for server_file in server_files:
                if 'examen' not in server_file:
                    continue  # Passer à l'élément suivant si 'TP' n'est pas dans cet élément
                
                # Extraire les fichiers de TP
                tp_files = server_file["examen"]
                for tp_file in tp_files:
                    file_url = tp_file["fichier"]
                    file_name = file_url.split("/")[-1]  # Extraire le nom du fichier à partir de l'URL
                    
                    print(f"Nom du fichier: {file_name}")
                    print(f"URL du fichier: http://127.0.0.1:8000{file_url}")
                    
                    # Vérifier si le fichier est déjà localement
                    if file_name not in local_files:
                        save_path = os.path.join(folder_path, file_name)
                        print(f"Téléchargement de {file_name} dans {category}...")
                        self._download_file(f'http://127.0.0.1:8000{file_url}', save_path)
        elif category == 'Courses':
            for server_file in server_files:
                if 'Cours' not in server_file:
                    continue  # Passer à l'élément suivant si 'TP' n'est pas dans cet élément
                
                # Extraire les fichiers de TP
                tp_files = server_file["Cours"]
                for tp_file in tp_files:
                    file_url = tp_file["fichier"]
                    file_name = file_url.split("/")[-1]  # Extraire le nom du fichier à partir de l'URL
                    
                    print(f"Nom du fichier: {file_name}")
                    print(f"URL du fichier: http://127.0.0.1:8000{file_url}")
                    
                    # Vérifier si le fichier est déjà localement
                    if file_name not in local_files:
                        save_path = os.path.join(folder_path, file_name)
                        print(f"Téléchargement de {file_name} dans {category}...")
                        self._download_file(f'http://127.0.0.1:8000{file_url}', save_path)

        elif category == 'Interro':
            for server_file in server_files:
                if 'interro' not in server_file:
                    continue  # Passer à l'élément suivant si 'TP' n'est pas dans cet élément
                
                # Extraire les fichiers de TP
                tp_files = server_file["interro"]
                for tp_file in tp_files:
                    file_url = tp_file["fichier"]
                    file_name = file_url.split("/")[-1]  # Extraire le nom du fichier à partir de l'URL
                    
                    print(f"Nom du fichier: {file_name}")
                    print(f"URL du fichier: http://127.0.0.1:8000{file_url}")
                    
                    # Vérifier si le fichier est déjà localement
                    if file_name not in local_files:
                        save_path = os.path.join(folder_path, file_name)
                        print(f"Téléchargement de {file_name} dans {category}...")
                        self._download_file(f'http://127.0.0.1:8000{file_url}', save_path)



    def get_files(self, category):
        """
        Récupère et synchronise les fichiers d'une catégorie, puis retourne la liste des fichiers locaux.
        :param category: Catégorie (TP, Exams, Notes, Courses).
        :return: Liste des fichiers locaux pour cette catégorie.
        """
        if category not in self.sub_directories:
            raise ValueError(f"Catégorie inconnue : {category}")
        self._sync_files(category)
        return self._list_local_files(category)

        

from userdata import UserDatabase
def main():
    # Créer une instance de UserAuth pour gérer l'authentification
    auth = UserAuth()

    # Connexion de l'utilisateur
    username = 'minato'
    password = '123456789'
    if auth.login(username, password):
        print("Connexion réussie.")


        # Créer une instance de PostsAndSocialInteractions pour gérer les publications et interactions sociales
        posts_interactions = PostsAndSocialInteractions(auth)
        #my = auth.get_profile()
        #print(my)
        # Créer une publication
        #detail = "Ceci est un nouveau post."
        #new_post = posts_interactions.create_post(detail,file_path='car1.jpg')
        #if new_post:
        #    print("Publication créée :", new_post)

        # Ajouter une publication aux favoris
        favorite_response = posts_interactions.get_all_posts()


        
        #print(f"ma photo {photo}")
        #print(favorite_response)
        # Commenter une publication
        comment = "Ceci est un commentaire."
        #comment_response = posts_interactions.comment_on_post(post_id, comment)
        #if comment_response:
        #    print("Commentaire ajouté :", comment_response)

        # Partager une publication
        #share_response = posts_interactions.share_post(post_id)
        #if share_response:
        #    print("Publication partagée :", share_response)
    else:
        print("Connexion échouée.")

#main()

if __name__ == "__main__":
        # Importez ou créez une classe Auth pour gérer les jetons
    server_url = "http://127.0.0.1:8000/api"  # Assurez-vous que l'URL de base est correcte

    manager = CoursesAndFiles(None, server_url=server_url)

    

    # Récupération et synchronisation des fichiers pour chaque catégorie
    print("Fichiers TP :", manager.get_files("TP"))
    #print("Fichiers Exams :", manager.get_files("Exams"))
    #print("Fichiers Notes :", manager.get_files("Notes"))
    #print("Fichiers Courses :", manager.get_files("Courses"))
