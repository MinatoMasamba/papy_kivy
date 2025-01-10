from kivy import Config
Config.set('graphics', 'multisamples', '0')
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.lang import Builder
from kivy.lang import Builder
from kivy.core.image import Image as CoreImage
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from tkinter import filedialog
from kivymd.uix.button import MDFlatButton
from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.graphics import Ellipse, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, StencilPush, StencilUse, StencilPop, StencilUnUse
from kivy.core.image import Image as CoreImage
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.textfield import MDTextFieldRound
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivy.graphics import Color, RoundedRectangle

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from fonction import CircularProfileImage,truncate_text


from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from data import UserAuth
from kivymd.uix.label import MDLabel




class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_auth = UserAuth()  # Instance de UserAuth pour les opérations liées à l'utilisateur
        self.info = {}  # Initialiser les informations du profil

    def on_pre_enter(self):
        """Appelé automatiquement avant que l'écran ne devienne visible."""
        self.clear_widgets()
        self.info = self.load_profile()  # Charger les informations du profil
        if self.info:
            self.customprofile()  # Recréer l'interface utilisateur
        else:
            self.add_widget((MDIconButton(
                icon="arrow-left",
                pos_hint={"center_x": 0.1, "center_y": 0.955},
                height=dp(20),
                on_release=lambda x: self.switch_screen("feed_screen"))))
            self.add_widget(MDLabel(
                text="Veillez vous connecter svp",
                halign="center",
                font_style="H5"
            ))

    def customprofile(self):
        """Créer l'interface utilisateur pour l'écran du profil."""
        layout = BoxLayout(
            orientation='vertical',
            size=(400, 600),
            size_hint=(None, None),
            padding=10,
            spacing=10,
            pos_hint={"center_x": 0.5, "center_y": 0.578}
        )

        profile_card = MDCard(
            orientation="vertical",
            padding=20,
            spacing=10,
            size_hint=(None, None),
            size=(dp(250), dp(450)),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            md_bg_color=(0.65, 0.65, 0.95, 1),
            radius=[dp(20)]
        )
        profile = self.user_auth.get_profile()
        img = profile.get('author_name')
        # Ajouter l'image circulaire
        profile_image = CircularProfileImage(
            source=f'http://127.0.0.1:8000/{img[1]}',
            size_hint=(None, None),
            size=(dp(150), dp(150)),
            pos_hint={"center_x": 0.5}
        )
        profile_card.add_widget(profile_image)
        # Fonction appelée lors du clic
        def on_image_click(instance):
            self.show_add_post_dialog()

        profile_card.bind(on_release=on_image_click)
        profile_card.add_widget(Widget(size_hint_x=None, height=700))

        # Ajouter le label de bienvenue
        self.welcome_label = MDLabel(
            text="WELCOME",
            font_size=40,
            halign='center',
            size_hint_y=None,
            height=dp(50),
            padding_y=15
        )
        profile_card.add_widget(self.welcome_label)

        # Ajouter le scroll pour le feed
        scroll = ScrollView(size_hint=(1, None), height=dp(200))  # Hauteur maximale de défilement
        self.feed_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=350, padding=20, spacing=10)
        self.feed_layout.bind(minimum_height=self.feed_layout.setter('height'))
        scroll.add_widget(self.feed_layout)
        profile_card.add_widget(scroll)

        # Champs de saisie
        self.username_input = self.create_text_input(img[0], "account")
        self.feed_layout.add_widget(self.username_input)

        self.email_input = self.create_text_input("email", "email")
        self.feed_layout.add_widget(self.email_input)

        self.promotion_input = self.create_text_input(
            self.info.get('promotion') if self.info.get('promotion') else "Promotion", "school"
        )
        self.feed_layout.add_widget(self.promotion_input)

        self.first_name_input = self.create_text_input(
            self.info.get('first_name') if self.info.get('first_name') else 'first_name', "account"
        )
        self.feed_layout.add_widget(self.first_name_input)

        self.last_name_input = self.create_text_input(
            self.info.get('last_name') if self.info.get('last_name') else 'last_name', "account"
        )
        self.feed_layout.add_widget(self.last_name_input)

        self.numero_whatsapp_input = self.create_text_input(
            self.info.get('numero_whatsapp') if self.info.get('numero_whatsapp') else 'Numero', "phone"
        )
        self.feed_layout.add_widget(self.numero_whatsapp_input)

        # Bouton de retour
        layout.add_widget(MDIconButton(
            icon="arrow-left",
            pos_hint={"center_x": 0.1, "center_y": 0},
            height=dp(20),
            on_release=lambda x: self.switch_screen("feed_screen")
        ))

        layout.add_widget(profile_card)

        # Bouton de mise à jour
        layout.add_widget(MDRoundFlatButton(
            text="UPDATE",
            font_size=12,
            pos_hint={"center_x": 0.5},
            on_press=lambda x: self.update_profile(),
        ))

        self.add_widget(layout)

    def create_text_input(self, hint_text, icon_right):
        """Créer un champ de saisie avec des paramètres par défaut."""
        return MDTextFieldRound(
            hint_text=hint_text,
            icon_right=icon_right,
            size_hint_x=None,
            font_size=18,
            pos_hint={"center_x": 0.5},
            normal_color=(0.9, 0.9, 0.9, 1),
            _color_active=(0.2, 0.5, 0.8, 1)
        )

    def load_profile(self):
        """Charge les données du profil et les retourne sous forme de dictionnaire."""
        profile = self.user_auth.get_profile()
        if profile.get('author_name'):
            return {
                'username': profile['author_name'][0],
                'promotion': profile['promotion'],
                'first_name': profile['first_name'],
                'last_name': profile['last_name'],
                'numero_whatsapp': profile['numero_whatsapp']
            }
        return {}

    def update_profile(self):
        """Mettre à jour les informations du profil utilisateur."""
        from creat import UserProfile
        from userdata import UserDatabase
        from connection import ConnectionUserManager

        get_token = UserDatabase('local_storage.db')
        nom = ConnectionUserManager()
        user = nom.get_connection_user()
        token = get_token.get_user_token(user)

        # Mise à jour des données du profil
        profile_data = {
            'username': self.username_input.text or self.info.get('username'),
            'email': self.email_input.text or self.info.get('email'),
            'promotion': self.promotion_input.text or self.info.get('promotion'),
            'first_name': self.first_name_input.text or self.info.get('first_name'),
            'last_name': self.last_name_input.text or self.info.get('last_name'),
            'numero_whatsapp': self.numero_whatsapp_input.text or self.info.get('numero_whatsapp'),
        }

        result = UserProfile(token).update_profile(profile_data)
        if result:
            print("Profil mis à jour avec succès.")
            self.on_pre_enter()  # Réinitialiser l'écran
        else:
            print("Erreur lors de la mise à jour du profil.")

    def switch_screen(self, screen_name):
        self.manager.transition.direction = "right"
        self.manager.current = screen_name

    def show_add_post_dialog(self):
        """
        Affiche une boîte de dialogue pour ajouter un post avec un fichier et un champ de détail.
        """
        self.dialog = MDDialog(
            title="Ajouter un Post",
            type="custom",
            size_hint=(0.8, None),
            height="400dp",
            content_cls=Builder.load_string(
                """
BoxLayout:
    orientation: 'vertical'
    spacing: "12dp"
    size_hint_y: None
    height: self.minimum_height

    MDRoundFlatButton:
        id: file_button
        text: "Choisir un profile"
        pos_hint: {"center_x": 0.5}
        on_release: app.root.current_screen.select_file()

    MDLabel:
        id: file_label
        text: "Aucun fichier sélectionné"
        halign: "center"
        theme_text_color: "Hint"

    Image:
        id: preview_image
        source: ""
        size_hint: None, None
        size: "200dp", "200dp"
        allow_stretch: True
        keep_ratio: True

    MDRoundFlatButton:
        text: "Publier"
        icon: "publish"
        pos_hint: {"center_x": 0.5}
        on_release: app.root.current_screen.publish_post()
                """
            ),
            buttons=[
                MDFlatButton(
                    text="ANNULER",
                    on_release=self.close_dialog
                )
            ],
        )
        self.dialog.open()

    def close_dialog(self, *args):
        """
        Ferme la boîte de dialogue si elle est ouverte.
        """
        if self.dialog:
            self.dialog.dismiss()

    def select_file(self):
        """
        Simule une boîte de sélection de fichier pour choisir une image, un PDF ou un document.
        Si un fichier image est sélectionné, affiche un aperçu dans la boîte de dialogue.
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("Tous les fichiers", "*.*"),
                       ("Images", "*.png;*.jpg;*.jpeg"),
                       ]
        )

        if file_path:
            file_name = os.path.basename(file_path)
            self.dialog.content_cls.ids.file_label.text = f"Fichier sélectionné : {file_name}"
            self.selected_file_path = file_path

            # Si le fichier est une image, affichez un aperçu
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.dialog.content_cls.ids.preview_image.source = file_path
            else:
                # Supprime l'aperçu si ce n'est pas une image
                self.dialog.content_cls.ids.preview_image.source = ""
        else:
            self.dialog.content_cls.ids.file_label.text = "Aucun fichier sélectionné"
            self.dialog.content_cls.ids.preview_image.source = ""

    def publish_post(self):
        """Mettre à jour les informations du profil utilisateur."""
        from creat import UserProfile
        from userdata import UserDatabase
        from connection import ConnectionUserManager

        get_token = UserDatabase('local_storage.db')
        nom = ConnectionUserManager()
        user = nom.get_connection_user()
        token = get_token.get_user_token(user)
        """
        Publie le post avec les détails et le fichier sélectionné.
        """

        file_path = getattr(self, 'selected_file_path', None)

        if not file_path:
            self.show_error("Veuillez choisi une photo .")
            return

        #if not file_path:
            #self.show_error("Veuillez sélectionner un fichier.")
            #return

        # Logique de publication (ex. : enregistrement ou envoi au serveur)
        result = UserProfile(token).update_profile(photo_file=file_path)
        print(f"Post publié : Fichier={file_path}")

        # Fermer la boîte de dialogue après la publication
        self.close_dialog()

    def show_error(self, message):
        """
        Affiche une erreur sous forme de Snackbar.
        """
        Snackbar(text=message).open()