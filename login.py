from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRoundFlatButton
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from data import UserAuth
from kivymd.uix.button import MDIconButton
from kivy.metrics import dp
from connection import ConnectionStatusManager
from fonction import CustomSlideTransition

class Login(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.user_auth = UserAuth()  # Instance de UserAuth pour gérer les utilisateurs
        
        self.add_widget(MDIconButton(
            icon="arrow-left",
            pos_hint={"center_x": 0.1, "center_y": 0.955},
            height=dp(20),
            on_release=lambda x: self.switch_screen("feed_screen")
        ))

        # Création de la carte de connexion
        self.card = MDCard(size_hint=(None, None), size=(250, 500),
                           pos_hint={"center_x": 0.5, "center_y": 0.5},
                           elevation=10, padding=25, spacing=25,
                           radius=[20],
                           orientation='vertical')

        # Label de bienvenue
        self.welcome_label = MDLabel(text="WELCOME LOGIN ", font_size=40,
                                     halign='center', size_hint_y=None,
                                     height=40, padding_y=15)
        self.card.add_widget(self.welcome_label)
        
        # Champ utilisateur
        self.user = MDTextField(hint_text="username", icon_right="account",
                                size_hint_x=None, width=200, font_size=18,
                                pos_hint={"center_x": 0.5})
        self.card.add_widget(self.user)
        
        # Champ mot de passe
        self.password = MDTextField(hint_text="password", icon_right="eye-off",
                                    size_hint_x=None, width=200, font_size=18,
                                    pos_hint={"center_x": 0.5}, password=True)
        self.card.add_widget(self.password)
        
        # Bouton de connexion
        self.login_button = MDRoundFlatButton(text="LOG IN", font_size=12,
                                              pos_hint={"center_x": 0.5},
                                              on_release=self.logger)
        self.card.add_widget(self.login_button)
        
        # Bouton de réinitialisation
        self.clear_button = MDRoundFlatButton(text="CLEAR", font_size=12,
                                              pos_hint={"center_x": 0.5},
                                              on_release=self.clear)
        self.card.add_widget(self.clear_button)
        
        # Widget de remplissage
        self.card.add_widget(Widget(size_hint_y=None, height=10))
        
        # Ajouter la carte à l'écran
        self.add_widget(self.card)

    def logger(self, instance):

        username = self.user.text
        password = self.password.text

        # Appel de la méthode login de UserAuth
        if self.user_auth.login(username, password):
            connecter = ConnectionStatusManager()
            connecter.set_connection_status(True)
            user_data = self.user_auth.get_stored_credentials()
            self.welcome_label.text = f"Welcome, {user_data['first_name']} {user_data['last_name']}!"
            self.manager.transition = CustomSlideTransition(direction="left", duration=1)
            self.manager.current = "profile_screen"
        else:
            self.welcome_label.text = "Invalid credentials!"

    def clear(self, instance):
        self.welcome_label.text = "WELCOME"
        self.user.text = ""
        self.password.text = ""

    def switch_screen(self, screen_name):
        self.manager.transition = CustomSlideTransition(direction="right", duration=1)
        self.manager.current = screen_name