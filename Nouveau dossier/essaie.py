import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from PyPDF2 import PdfFileReader

class FileCard(BoxLayout, ButtonBehavior):
    def __init__(self, file_id, file_name, file_path, file_type, **kwargs):
        super().__init__(**kwargs)
        self.file_id = file_id
        self.file_path = file_path
        self.file_type = file_type
        self.orientation = "vertical"
        self.size_hint = (1, None)
        self.height = dp(80)

        # Créer une instance de MDCard
        self.card = MDCard(orientation="vertical", padding=dp(10), size_hint=(1, None), height=dp(80))
        
        # Afficher le nom du fichier sur la carte
        label = MDLabel(
            text=file_name,
            halign="center",
            valign="middle",
            size_hint_y=None,
            font_style="Subtitle1"
        )
        self.card.add_widget(label)
        self.add_widget(self.card)

        # Rendre la carte cliquable
        self.card.bind(on_release=self.on_press)

    def on_press(self, *args):
        if self.file_type in ['png', 'jpg', 'jpeg']:
            self.show_image()
        elif self.file_type == 'pdf':
            self.show_pdf()
        else:
            self.show_text()
    

    def show_image(self):
        from kivymd.uix.boxlayout import MDBoxLayout  # Import nécessaire pour le conteneur personnalisé
        try:
            # Créer un conteneur pour l'image
            content = MDBoxLayout(
                orientation="vertical",
                size_hint=(1, None),
                height=dp(400)
            )
            content.bind(minimum_height=content.setter("height"))  # Ajuster la taille du conteneur si nécessaire

            # Ajouter l'image au conteneur
            image = Image(
                source=self.file_path,
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(1, None),
                height=dp(400)
            )
            content.add_widget(image)

            # Créer le MDDialog
            dialog = MDDialog(
                title="Image",
                type="custom",
                content_cls=content,
                size_hint=(0.8, 0.8),
                buttons=[
                    MDFlatButton(text="FERMER", on_release=lambda x: dialog.dismiss())
                ]
            )
            dialog.open()
        except Exception as e:
            print(f"Erreur lors de l'affichage de l'image: {e}")


    def show_pdf(self):
        try:
            with open(self.file_path, 'rb') as f:
                pdf_document = PdfFileReader(f)
                pdf_page = pdf_document.getPage(0)
                output = pdf_page.extractText()

            dialog = MDDialog(
                title="Contenu du PDF",
                text=output,
                size_hint=(0.8, 0.8),
                buttons=[
                    MDFlatButton(text="FERMER", on_release=lambda x: dialog.dismiss())
                ]
            )
            dialog.open()
        except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier PDF: {e}")
    def show_text(self):
        try:
            with open(self.file_path, 'r') as file:
                content = file.read()

            # Créer un Label MDLabel avec le contenu du fichier
            label = MDLabel(
                text=content,
                size_hint_y=None,
                text_size=(dp(300), None),
                halign="left",
                valign="top"
            )
            label.bind(texture_size=label.setter('size'))  # Ajuster la taille au contenu

            # Placer le Label dans un ScrollView
            scroll = ScrollView(size_hint=(1, None), height=dp(400))
            scroll.add_widget(label)

            # Créer un MDDialog avec le ScrollView comme contenu
            dialog = MDDialog(
                title="Contenu du fichier",
                type="custom",
                content_cls=scroll,
                size_hint=(0.8, 0.8),
                buttons=[
                    MDFlatButton(text="FERMER", on_release=lambda x: dialog.dismiss())
                ]
            )
            dialog.open()
        except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier texte: {e}")



class FileList(BoxLayout):
    def __init__(self, files, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # ScrollView pour la liste des fichiers
        scroll_view = ScrollView()
        file_list = MDList()

        # Ajouter les fichiers au MDList
        for file in files:
            file_id = file["id"]
            file_name = file["name"]
            file_path = os.path.join(os.getcwd(), file["path"])  # Construire le chemin complet
            file_type = file["type"]
            item = FileCard(file_id, file_name, file_path, file_type)
            file_list.add_widget(item)

        scroll_view.add_widget(file_list)
        self.add_widget(scroll_view)

class FileListScreen(Screen):
    def __init__(self, files, **kwargs):
        super().__init__(**kwargs)
        file_list = FileList(files)
        self.add_widget(file_list)

        # Bouton pour revenir au menu principal
        self.add_widget(MDIconButton(
            icon="arrow-left",
            pos_hint={"center_x": 0.1, "center_y": 0.955},
            height=dp(20),
            on_release=lambda x: self.switch_screen("menu_screen")
        ))

    def switch_screen(self, screen_name):
        self.manager.current = screen_name

def get_files_from_current_directory():
    files = []
    for file_name in os.listdir(os.getcwd()):
        if os.path.isfile(file_name):
            file_type = file_name.split('.')[-1].lower()
            files.append({"id": len(files) + 1, "name": file_name, "path": file_name, "type": file_type})
    return files

# Exemple d'application
class FileListApp(MDApp):
    def build(self):
        # Récupérer les fichiers du répertoire courant
        files_from_server = get_files_from_current_directory()
        return FileListScreen(files=files_from_server)

if __name__ == "__main__":
    FileListApp().run()
