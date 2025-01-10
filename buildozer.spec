[app]

# Nom de votre application
title = My Application

# Nom du paquet (utilisé pour identifier l'application, sans espace ni caractères spéciaux)
package.name = myapp

# Domaine du paquet (doit être unique)
package.domain = org.test

# Répertoire où se trouve votre fichier main.py
source.dir = .

# Extensions des fichiers à inclure dans le projet
source.include_exts = py,png,jpg,kv,atlas

# Version de l'application
version = 1.0

# Liste des dépendances Python nécessaires à votre application
requirements = python3,kivy,pillow,requests

# Orientation supportée (portrait, landscape, etc.)
orientation = portrait

# Plein écran (1 = oui, 0 = non)
fullscreen = 1

# Couleur d'arrière-plan pendant le chargement (blanc ici)
android.presplash_color = #FFFFFF

# Autorisations Android nécessaires
android.permissions = android.permission.INTERNET,android.permission.WRITE_EXTERNAL_STORAGE

# Architecture ciblée pour Android
android.archs = arm64-v8a, armeabi-v7a

# Activer ou désactiver les sauvegardes automatiques sur Android (API 23+)
android.allow_backup = True

# Type de sortie pour le mode debug (apk ou aar)
android.debug_artifact = apk

# Type de sortie pour le mode release (apk ou aab)
android.release_artifact = apk

# Inclure l'icône personnalisée (assurez-vous que l'icône existe)
icon.filename = icon.icon

# Inclure une image de démarrage (facultatif)
presplash.filename = %(source.dir)s/splash.png

[buildozer]

# Niveau de journalisation (0 = erreurs seulement, 1 = infos, 2 = débogage)
log_level = 2

# Afficher un avertissement si Buildozer est exécuté en tant que root
warn_on_root = 1

android.api = 29  # Exemple pour Android 10
