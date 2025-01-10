import sqlite3

class ConnectionStatusManager:
    def __init__(self, db_path='connection_status.db'):
        """
        Initialise la base de données et crée la table si elle n'existe pas.
        :param db_path: Chemin de la base de données SQLite.
        """
        self.db_path = db_path
        self._create_database()

    def _create_database(self):
        """Crée la table pour stocker l'état de connexion."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS connection_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    is_connected BOOLEAN DEFAULT FALSE
                );
            ''')
            # Insérer une valeur par défaut si elle n'existe pas encore
            cursor.execute('''
                INSERT OR IGNORE INTO connection_status (id, is_connected)
                VALUES (1, FALSE);
            ''')
            conn.commit()

    def set_connection_status(self, status):
        """
        Met à jour l'état de connexion.
        :param status: Nouvel état de connexion (True ou False).
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE connection_status
                SET is_connected = ?
                WHERE id = 1;
            ''', (status,))
            conn.commit()

        print(f"État de connexion mis à jour à {status}.")

    def get_connection_status(self):
        """
        Récupère l'état de connexion actuel.
        :return: True si connecté, sinon False.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT is_connected
                FROM connection_status
                WHERE id = 1;
            ''')
            result = cursor.fetchone()
            return result[0] if result else False
        


class ConnectionUserManager:
    def __init__(self, db_path='connection_user.db'):
        """
        Initialise la base de données et crée la table si elle n'existe pas.
        :param db_path: Chemin de la base de données SQLite.
        """
        self.db_path = db_path
        self._create_database()

    def _create_database(self):
        """Crée la table pour stocker l'état de connexion."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS connection_user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT DEFAULT ''
                );
            ''')
            cursor.execute('''
                INSERT OR IGNORE INTO connection_user (id, user)
                VALUES (1, '');
            ''')
            conn.commit()
    def set_connection_user(self, user):
        """
        Met à jour l'état de connexion.
        :param status: Nouvel état de connexion (True ou False).
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE connection_user
                SET user = ?
                WHERE id = 1;
            ''', (user,))
            conn.commit()
        print(f"user mis à jour à {user}.")

    def get_connection_user(self):
        """
        Récupère l'état de connexion actuel.
        :return: True si connecté, sinon False.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user
                FROM connection_user
                WHERE id = 1;
            ''')
            result = cursor.fetchone()
            return result[0] if result else False
        

# Exemple d'utilisation
if __name__ == "__main__":
    manager = ConnectionUserManager()
    manager.set_connection_user('uchiwa')
    # Vérification initiale de l'état
    print("État initial :", manager.get_connection_user())


