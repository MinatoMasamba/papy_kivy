import os

# Définir le chemin MEDIA_ROOT
media_root = r'C:\Users\MUKSOFT\projet_app\source_academia\media'

# Vérifier si le répertoire existe
if os.path.exists(media_root):
    print(f"Le répertoire {media_root} existe.")
else:
    print(f"Le répertoire {media_root} n'existe pas.")
