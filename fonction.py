from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.animation import Animation
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivy.uix.image import Image
from PyPDF2 import PdfFileReader
import os
from kivy.uix.checkbox import CheckBox
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget
from kivy.graphics import Color, Ellipse, Rectangle, StencilPush, StencilUse, StencilPop, StencilUnUse
from kivy.uix.widget import Widget
from kivy.core.image import Image as CoreImage
from kivy.properties import StringProperty
from data import PostsAndSocialInteractions
import requests


def truncate_text(text, max_length):
    if not isinstance(text, str):
        return "Texte non valide"
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


""""
 ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'Subtitle1', 'Subtitle2', 'Body1', 'Body2', 'Button', 'Caption', 'Overline', 'Icon']
"""
class compteItem(OneLineAvatarIconListItem):
    def __init__(self, file_path, **kwargs):
        super().__init__(**kwargs)
        self.file_path = file_path
        self.text = os.path.basename(file_path)
        self.font_style = 'Overline'
        self.halign= "center"
        self.font_size= 18

        # Ajouter l'icône et la checkbox
        icon = IconLeftWidget(icon="account-outline")
        self.add_widget(icon)

        self.checkbox = CheckBox(size_hint_x=None, width=50)
        self.add_widget(self.checkbox)

    def is_selected(self):
        return self.checkbox.active

class CompteList(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # ScrollView pour la liste des fichiers
        scroll_view = ScrollView()
        file_list = MDList()

        # Ajouter les fichiers au MDList
        for file_name in ['Minato','masamba','kakashi']:
            item = compteItem(file_name)
            file_list.add_widget(item)

        scroll_view.add_widget(file_list)
        self.add_widget(scroll_view)

    def get_selected_files(self):
        return [child.file_path for child in self.children[0].children if child.is_selected()]

class CompteListScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        file_list = CompteList()

        self.add_widget(MDIconButton(
            icon="arrow-left",
            pos_hint={"center_x": 0.1, "center_y": 0.955},
            height=dp(20),
            on_release=lambda x: self.switch_screen("menu_screen")
        ))
        self.add_widget(file_list)


class CustomSlideTransition(SlideTransition):
    def __init__(self, displacement=0.5, **kwargs):
        super().__init__(**kwargs)
        self.displacement = displacement

    def add_custom_behavior(self, manager, screen):
        """Ajoute une logique supplémentaire pour gérer les positions des écrans."""
        current_screen = manager.current_screen

        # Définir la position initiale de l'écran entrant
        if self.direction == 'left':
            screen.x = manager.width
        elif self.direction == 'right':
            screen.x = -manager.width

        # Ajouter le nouvel écran au gestionnaire
        manager.add_widget(screen)

        # Définir les animations
        anim_out = Animation(
            x=-manager.width * self.displacement if self.direction == 'left' else manager.width * self.displacement,
            duration=self.duration,
            t=self.transition_type
        )
        anim_in = Animation(x=0, duration=self.duration, t=self.transition_type)

        # Lier les animations
        anim_out.bind(on_complete=lambda *args: self.on_animation_complete(manager, current_screen))
        anim_out.start(current_screen)
        anim_in.start(screen)

    def on_animation_complete(self, manager, old_screen):
        """Nettoie après la transition."""
        manager.remove_widget(old_screen)


#from kivy.core.image import CoreImage
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Ellipse, Rectangle, StencilPush, StencilUse, StencilUnUse, StencilPop
from kivy.core.image import Image as CoreImage
import requests
from PIL import Image as PILImage, ExifTags  # Import corrigé depuis Pillow
import os
import io


class CircularProfileImage(ButtonBehavior, Widget):
    source = StringProperty("default.jpg")  # Chemin ou URL de l'image par défaut

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            # Étape 1: Activer le stencil pour dessiner uniquement dans un cercle
            StencilPush()
            Color(1, 1, 1, 1)  # Couleur blanche (neutre pour le stencil)
            self.circle = Ellipse(size=self.size, pos=self.pos)

            StencilUse()

            # Étape 2: Dessiner l'image
            self.image_texture = None
            self.image_rect = Rectangle(size=self.size, pos=self.pos)

            StencilUnUse()
            StencilPop()

        # Charger l'image et gérer les mises à jour
        self.bind(size=self.update_canvas, pos=self.update_canvas, source=self.update_image)
        self.update_image()

    def update_canvas(self, *args):
        """Mise à jour de la position et de la taille de l'image et du cercle."""
        size = min(self.width, self.height)  # Taille pour garder un cercle parfait
        self.circle.size = (size, size)
        self.circle.pos = (self.center_x - size / 2, self.center_y - size / 2)

        self.image_rect.size = (size, size)
        self.image_rect.pos = (self.center_x - size / 2, self.center_y - size / 2)

    def update_image(self, *args):
        """Chargement de l'image source (locale ou en ligne) et mise à jour de la texture."""
        try:
            image_path = self.source

            # Si l'image est une URL, téléchargez-la temporairement
            if self.source.startswith("http://") or self.source.startswith("https://"):
                response = requests.get(self.source, stream=True)
                if response.status_code == 200:
                    temp_image_path = "temp_image.jpg"
                    with open(temp_image_path, "wb") as f:
                        for chunk in response.iter_content(1024):
                            f.write(chunk)
                    image_path = temp_image_path
                else:
                    raise Exception(f"Erreur lors du téléchargement de l'image en ligne : {response.status_code}")

            # Charger l'image avec Pillow pour corriger l'orientation
            image = PILImage.open(image_path)  # Utiliser explicitement PILImage
            image = self.correct_orientation(image)

            # Charger la texture Kivy
            texture_data = io.BytesIO()
            image.save(texture_data, format="PNG")
            texture_data.seek(0)
            core_image = CoreImage(texture_data, ext="png")
            self.image_texture = core_image.texture

            # Calculer le facteur d'échelle pour correspondre au cercle tout en gardant les proportions
            texture_width = self.image_texture.width
            texture_height = self.image_texture.height
            circle_size = min(self.width, self.height)  # Taille du cercle (diamètre)
            scale = circle_size / max(texture_width, texture_height)  # Facteur d'échelle

            # Nouvelle taille redimensionnée
            new_width = texture_width * scale
            new_height = texture_height * scale

            # Centrer l'image dans le cercle
            self.image_rect.size = (new_width, new_height)
            self.image_rect.pos = (
                self.center_x - new_width / 2,
                self.center_y - new_height / 2,
            )

            # Appliquer la texture à l'image
            self.image_rect.texture = self.image_texture

            # Supprimer le fichier temporaire si créé
            if image_path == "temp_image.jpg" and os.path.exists(image_path):
                os.remove(image_path)

        except Exception as e:
            print(f"Erreur lors du chargement de l'image : {e}")

    def correct_orientation(self, image):
        """Corrige l'orientation de l'image à l'aide des métadonnées EXIF."""
        try:
            if hasattr(image, "_getexif"):  # Vérifiez si l'image contient des métadonnées EXIF
                exif = image._getexif()
                if exif is not None:
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation] == 'Orientation':
                            orientation_value = exif.get(orientation, 1)
                            # Applique les rotations en fonction des métadonnées EXIF
                            if orientation_value == 3:
                                image = image.rotate(180, expand=True)
                            elif orientation_value == 6:
                                image = image.rotate(270, expand=True)
                            elif orientation_value == 8:
                                image = image.rotate(90, expand=True)
        except Exception as e:
            print(f"Erreur lors de la correction de l'orientation EXIF : {e}")
        return image



class HeartButton(MDIconButton): 
    def __init__(self,post_id,verifi, **kwargs): 
        super().__init__(**kwargs) 
        self.icon = "heart-outline" 
        self.post_fovorie = PostsAndSocialInteractions(None)
        self.post_id = post_id
        self.verifi  = verifi['favorite_exists']['exists']
        self.md_bg_color_normal = (1, 1, 1, 1) 
        self.md_bg_color_active = (1, 0, 0, 1) # Rouge 
        if self.verifi:
            self.icon = "heart"   

    def on_release(self): 
        if self.icon != "heart" : 
            self.icon = "heart" 
            self.md_bg_color = self.md_bg_color_active 
            self.post_fovorie.add_to_favorites(self.post_id)
        else: 
            self.icon = "heart-outline" 
            self.md_bg_color = self.md_bg_color_normal
            self.post_fovorie.add_to_favorites(self.post_id)




from data import CoursesAndFiles

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from PyPDF2 import PdfFileReader
import os

class FileTP(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        classe = CoursesAndFiles()
        self.files =classe.get_files('TP')
        self.orientation = "vertical"
        self.dialog_img = None
        self.dialog_text = None
        self.dialog_pdf = None

        # ScrollView pour la liste des fichiers
        scroll_view = ScrollView(
            pos_hint={'top':0.94755,}
        )
        file_list = MDList(
            radius=[30],
            size_hint=(1, None),
            height=dp(100),
            padding=dp(10),
            spacing=dp(10),

            
        )
        file_list.add_widget(Widget(size_hint_x=None, height=160))
        # Ajouter les fichiers au MDList
        for file_path in self.files:
            file_name = os.path.basename(file_path)
            file_type = file_name.split('.')[-1].lower()  # Déduire le type du fichier à partir de l'extension
            item = self.create_file_card(file_name, file_path, file_type)
            file_list.add_widget(item)
        
        scroll_view.add_widget(file_list)
        self.add_widget(Widget(size_hint_x=None, height=160))
        self.add_widget(scroll_view)

        # Bouton pour revenir au menu principal
        self.add_widget(Widget(size_hint_x=None, height=160))
        self.add_widget(MDIconButton(
            icon="arrow-left",
            pos_hint={"center_x": 0.1, "center_y": 0.955},
            height=dp(20),
            on_release=lambda x: self.switch_screen("menu_screen")
        ))

    def create_file_card(self, file_name, file_path, file_type):
        """Créer une carte pour un fichier."""
        card = MDCard(orientation="vertical", padding=dp(10), size_hint=(1, None), height=dp(80))
        
        # Afficher le nom du fichier sur la carte
        label = MDLabel(
            text=file_name,
            halign="center",
            valign="middle",
            size_hint_y=None,
            font_style="Subtitle1"
        )
        card.add_widget(label)

        # Ajouter un événement clic
        card.bind(on_release=lambda x: self.handle_file_click(file_path, file_type))

        return card

    def handle_file_click(self, file_path, file_type):
        """Gérer le clic sur un fichier."""
        if file_type in ['png', 'jpg', 'jpeg']:
            self.show_image(file_path)
        elif file_type == 'pdf':
            self.show_pdf(file_path)
        else:
            self.show_text(file_path)

    def show_image(self, file_path):
        """Afficher une image."""
        try:
            content = MDBoxLayout(
                orientation="vertical",
                size_hint=(1, None),
                height=dp(400)
            )
            image = Image(
                source=file_path,
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(1, None),
                height=dp(400)
            )
            content.add_widget(image)

            self.dialog_img = MDDialog(
                title="Image",
                type="custom",
                content_cls=content,
                size_hint=(0.8, 0.8),
                buttons=[MDFlatButton(text="FERMER", on_release=lambda x: self.fermer(dialog=self.dialog_img))]
            )
            self.dialog_img.open()
        except Exception as e:
            print(f"Erreur lors de l'affichage de l'image: {e}")

    def show_pdf(self, file_path):
        """Afficher le contenu d'un PDF."""
        try:
            with open(file_path, 'rb') as f:
                pdf_document = PdfFileReader(f)
                pdf_page = pdf_document.getPage(0)
                output = pdf_page.extractText()

            self.dialog_pdf = MDDialog(
                title="Contenu du PDF",
                text=output,
                size_hint=(0.8, 0.8),
                buttons=[MDFlatButton(text="FERMER", on_release=lambda x: self.fermer(dialog=self.dialog_pdf))]
            )
            self.dialog_pdf.open()
        except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier PDF: {e}")

    def show_text(self, file_path):
        """Afficher le contenu d'un fichier texte."""
        try:
            with open(file_path, 'r') as file:
                content = file.read()

            label = MDLabel(
                text=content,
                size_hint_y=None,
                text_size=(dp(300), None),
                halign="left",
                valign="top"
            )
            label.bind(texture_size=label.setter('size'))

            scroll = ScrollView(size_hint=(1, None), height=dp(400))
            scroll.add_widget(label)

            self.dialog_text = MDDialog(
                title="Contenu du fichier",
                type="custom",
                content_cls=scroll,
                size_hint=(0.8, 0.8),
                buttons=[MDFlatButton(text="FERMER", on_release=lambda x: self.fermer(dialog=self.dialog_text))]
            )
            self.dialog_text.open()
        except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier texte: {e}")

    def switch_screen(self, screen_name):
        """Changer d'écran."""
        self.manager.current = screen_name
    def fermer(self,dialog):
        dialog.dismiss()


class FileInterro(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        classe = CoursesAndFiles()
        self.files = classe.get_files("Interro")
        self.orientation = "vertical"

        scroll_view = ScrollView(
            pos_hint={'top':0.94755,}
        )
        file_list = MDList()

        # Ajouter les fichiers au MDList
        for file_path in self.files:
            file_name = os.path.basename(file_path)
            file_type = file_name.split('.')[-1].lower()  # Déduire le type du fichier à partir de l'extension
            item = self.create_file_card(file_name, file_path, file_type)
            file_list.add_widget(item)

        scroll_view.add_widget(file_list)
        self.add_widget(scroll_view)

        # Bouton pour revenir au menu principal
        self.add_widget(MDIconButton(
            icon="arrow-left",
            pos_hint={"center_x": 0.1, "center_y": 0.955},
            height=dp(20),
            on_release=lambda x: self.switch_screen("menu_screen")
        ))

    def create_file_card(self, file_name, file_path, file_type):
        """Créer une carte pour un fichier."""
        card = MDCard(orientation="vertical", padding=dp(10), size_hint=(1, None), height=dp(80))
        
        # Afficher le nom du fichier sur la carte
        label = MDLabel(
            text=file_name,
            halign="center",
            valign="middle",
            size_hint_y=None,
            font_style="Subtitle1"
        )
        card.add_widget(label)

        # Ajouter un événement clic
        card.bind(on_release=lambda x: self.handle_file_click(file_path, file_type))

        return card

    def handle_file_click(self, file_path, file_type):
        """Gérer le clic sur un fichier."""
        if file_type in ['png', 'jpg', 'jpeg']:
            self.show_image(file_path)
        elif file_type == 'pdf':
            self.show_pdf(file_path)
        else:
            self.show_text(file_path)

    def show_image(self, file_path):
        """Afficher une image."""
        try:
            content = MDBoxLayout(
                orientation="vertical",
                size_hint=(1, None),
                height=dp(400)
            )
            image = Image(
                source=file_path,
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(1, None),
                height=dp(400)
            )
            content.add_widget(image)

            dialog = MDDialog(
                title="Image",
                type="custom",
                content_cls=content,
                size_hint=(0.8, 0.8),
                buttons=[MDFlatButton(text="FERMER", on_release=lambda x:self.fermer(dialog=dialog))]
            )
            dialog.open()
        except Exception as e:
            print(f"Erreur lors de l'affichage de l'image: {e}")

    def show_pdf(self, file_path):
        """Afficher le contenu d'un PDF."""
        try:
            with open(file_path, 'rb') as f:
                pdf_document = PdfFileReader(f)
                pdf_page = pdf_document.getPage(0)
                output = pdf_page.extractText()

            dialog = MDDialog(
                title="Contenu du PDF",
                text=output,
                size_hint=(0.8, 0.8),
                buttons=[MDFlatButton(text="FERMER", on_release=lambda x:self.fermer(dialog=dialog))]
            )
            dialog.open()
        except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier PDF: {e}")

    def show_text(self, file_path):
        """Afficher le contenu d'un fichier texte."""
        try:
            with open(file_path, 'r') as file:
                content = file.read()

            label = MDLabel(
                text=content,
                size_hint_y=None,
                text_size=(dp(300), None),
                halign="left",
                valign="top"
            )
            label.bind(texture_size=label.setter('size'))

            scroll = ScrollView(size_hint=(1, None), height=dp(400))
            scroll.add_widget(label)

            dialog = MDDialog(
                title="Contenu du fichier",
                type="custom",
                content_cls=scroll,
                size_hint=(0.8, 0.8),
                buttons=[MDFlatButton(text="FERMER", on_release=lambda x:self.fermer(dialog=dialog) )]
            )
            dialog.open()
        except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier texte: {e}")

    def switch_screen(self, screen_name):
        """Changer d'écran."""
        self.manager.current = screen_name
    def fermer(self,dialog):
        dialog.dismiss()


class FileExam(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        classe = CoursesAndFiles()
        self.files = classe.get_files("Exams")
        self.orientation = "vertical"
        self.dialog_img = None
        self.dialog_text = None
        self.dialog_pdf = None

        # ScrollView pour la liste des fichiers
        scroll_view = ScrollView(
            pos_hint={'top':0.94755,}
        )
        file_list = MDList()

        # Ajouter les fichiers au MDList
        for file_path in self.files:
            file_name = os.path.basename(file_path)
            file_type = file_name.split('.')[-1].lower()  # Déduire le type du fichier à partir de l'extension
            item = self.create_file_card(file_name, file_path, file_type)
            file_list.add_widget(item)

        scroll_view.add_widget(file_list)
        self.add_widget(scroll_view)

        # Bouton pour revenir au menu principal
        self.add_widget(MDIconButton(
            icon="arrow-left",
            pos_hint={"center_x": 0.1, "center_y": 0.955},
            height=dp(20),
            on_release=lambda x: self.switch_screen("menu_screen")
        ))

    def create_file_card(self, file_name, file_path, file_type):
        """Créer une carte pour un fichier."""
        card = MDCard(orientation="vertical", padding=dp(10), size_hint=(1, None), height=dp(80))
        
        # Afficher le nom du fichier sur la carte
        label = MDLabel(
            text=file_name,
            halign="center",
            valign="middle",
            size_hint_y=None,
            font_style="Subtitle1"
        )
        card.add_widget(label)

        # Ajouter un événement clic
        card.bind(on_release=lambda x: self.handle_file_click(file_path, file_type))

        return card

    def handle_file_click(self, file_path, file_type):
        """Gérer le clic sur un fichier."""
        if file_type in ['png', 'jpg', 'jpeg']:
            self.show_image(file_path)
        elif file_type == 'pdf':
            self.show_pdf(file_path)
        else:
            self.show_text(file_path)

    def show_image(self, file_path):
        """Afficher une image."""
        try:
            content = MDBoxLayout(
                orientation="vertical",
                size_hint=(1, None),
                height=dp(400)
            )
            image = Image(
                source=file_path,
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(1, None),
                height=dp(400)
            )
            content.add_widget(image)

            dialog = MDDialog(
                title="Image",
                type="custom",
                content_cls=content,
                size_hint=(0.8, 0.8),
                buttons=[MDFlatButton(text="FERMER", on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()
        except Exception as e:
            print(f"Erreur lors de l'affichage de l'image: {e}")

    def show_pdf(self, file_path):
        """Afficher le contenu d'un PDF."""
        try:
            with open(file_path, 'rb') as f:
                pdf_document = PdfFileReader(f)
                pdf_page = pdf_document.getPage(0)
                output = pdf_page.extractText()

            dialog = MDDialog(
                title="Contenu du PDF",
                text=output,
                size_hint=(0.8, 0.8),
                buttons=[MDFlatButton(text="FERMER", on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()
        except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier PDF: {e}")

    def show_text(self, file_path):
        """Afficher le contenu d'un fichier texte."""
        try:
            with open(file_path, 'r') as file:
                content = file.read()

            label = MDLabel(
                text=content,
                size_hint_y=None,
                text_size=(dp(300), None),
                halign="left",
                valign="top"
            )
            label.bind(texture_size=label.setter('size'))

            scroll = ScrollView(size_hint=(1, None), height=dp(400))
            scroll.add_widget(label)

            dialog = MDDialog(
                title="Contenu du fichier",
                type="custom",
                content_cls=scroll,
                size_hint=(0.8, 0.8),
                buttons=[MDFlatButton(text="FERMER", on_release=lambda x: dialog.dismiss())]
            )
            dialog.open()
        except Exception as e:
            print(f"Erreur lors de l'ouverture du fichier texte: {e}")

    def switch_screen(self, screen_name):
        """Changer d'écran."""
        self.manager.current = screen_name

