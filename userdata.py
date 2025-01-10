import sqlite3

class UserDatabase:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_user_token(self, username):
        """
        Récupère le token d'un utilisateur spécifique à partir de son username.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT token FROM user WHERE username = ?
                ''', (username,))
                result = cursor.fetchone()
                
                if result:
                    return result[0]  # Le token est dans la première colonne
                else:
                    print(f"Aucun utilisateur trouvé avec le username : {username}")
                    return None
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération du token : {e}")
            return None
    def get_user_is_conneted(self, username):
        """
        Récupère le token d'un utilisateur spécifique à partir de son username.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT logged_in FROM user WHERE username = ?
                ''', (username,))
                result = cursor.fetchone()
                
                if result:
                    return result[0]  # Le token est dans la première colonne
                else:
                    print(f"Aucun utilisateur trouvé avec le username : {username}")
                    return None
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération du token : {e}")
            return None

'''
# Exemple d'utilisation
db = UserDatabase('local_storage.db')  # Remplacez par le chemin de votre base de données
username = "uchiwa"
token = db.get_user_token(username)
is_logged = db.get_user_is_conneted(username)

if token:
    print(f"Token pour l'utilisateur '{username}': {token}")
else:
    print(f"Token non trouvé pour l'utilisateur '{username}'.")

if is_logged:
    print(f"Token pour l'utilisateur '{username}': {is_logged}")
else:
    print(f"Token non trouvé pour l'utilisateur '{username}'.")
    '''