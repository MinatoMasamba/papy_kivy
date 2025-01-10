from kivy import Config
Config.set('graphics', 'multisamples', '0')
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivymd.uix.label import MDLabel
from kivy.core.image import Image as CoreImage

from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.textfield import MDTextFieldRound
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
#from kivymd.uix.iconbutton import MDIconButton
from fonction import CustomSlideTransition


from data import UserAuth

class CreatCompte(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.userauth = UserAuth()
        self.add_widget(MDIconButton(
            icon="arrow-left",
            pos_hint={"center_x": 0.1, "center_y": 0.955},
            height=dp(20),
            on_release=lambda x: self.switch_screen("feed_screen")
        ))
        
        # Création de la carte de connexion
        card = MDCard(size_hint=(None, None), size=(250, 500),
                           pos_hint={"center_x": 0.5, "center_y": 0.5},
                           elevation=10, padding=25, spacing=25,
                           radius=[20],
                           orientation='vertical')

        self.user_input = MDTextFieldRound(
            hint_text="username",
            icon_right="account",
            size_hint_x=None,
            width=200,
            font_size=18,
            pos_hint={"center_x": 0.5},
            normal_color=[0.9, 0.9, 0.9, 1],  # Initialisation correcte de normal_color
            _color_active=[0.2, 0.5, 0.8, 1]  # Initialisation correcte de _color_active
        )
        card.add_widget(MDLabel(text='Crée votre compte', halign='center'))
        
        card.add_widget(self.user_input)

        self.email_input = MDTextFieldRound(
            hint_text="email",
            icon_right="email",
            size_hint_x=None,
            width=200,
            font_size=18,
            pos_hint={"center_x": 0.5},
            normal_color=[0.9, 0.9, 0.9, 1],  # Initialisation correcte de normal_color
            _color_active=[0.2, 0.5, 0.8, 1]  # Initialisation correcte de _color_active
        )
        card.add_widget(self.email_input)

        self.password_input = MDTextFieldRound(
            hint_text="password",
            icon_right="eye-off",
            password=True,
            size_hint_x=None,
            width=200,
            font_size=18,
            pos_hint={"center_x": 0.5},
            normal_color=[0.9, 0.9, 0.9, 1],  # Initialisation correcte de normal_color
            _color_active=[0.2, 0.5, 0.8, 1]  # Initialisation correcte de _color_active
        )
        card.add_widget(self.password_input)

        self.confirm_password_input = MDTextFieldRound(
            hint_text="confirm password",
            icon_right="eye-off",
            password=True,
            size_hint_x=None,
            width=200,
            font_size=18,
            pos_hint={"center_x": 0.5},
            normal_color=[0.9, 0.9, 0.9, 1],  # Initialisation correcte de normal_color
            _color_active=[0.2, 0.5, 0.8, 1]  # Initialisation correcte de _color_active
        )
        
        card.add_widget(self.confirm_password_input)

        self.message_label = MDLabel(text="", halign='center', theme_text_color="Error")
        card.add_widget(self.message_label)

        login_button = MDRoundFlatButton(text="cree ", font_size=12, size_hint_x=None, width=200, pos_hint={"center_x": 0.5})
        login_button.bind(on_press=self.logger)
        card.add_widget(login_button)

        clear_button = MDRoundFlatButton(text="clear", font_size=12, size_hint_x=None, width=200, pos_hint={"center_x": 0.5})
        clear_button.bind(on_press=self.clear)
        card.add_widget(clear_button)

        self.add_widget(card)
        login_button = MDRoundFlatButton(text="se connecté", font_size=12, size_hint_x=None, width=200, pos_hint={"center_x": 0.5,'center_y':0.09})
        login_button.bind(on_press= lambda x: self.switch_screen('login'))
        self.add_widget(login_button)

    def logger(self, instance):
        username = self.user_input.text
        password = self.password_input.text
        email = self.email_input.text
        confirm_password = self.confirm_password_input.text

        # Vérifier si les mots de passe correspondent
        if password != confirm_password:
            self.message_label.text = "Les mots de passe ne correspondent pas!"
            return

        # Créer une instance de CREAT
        creat_instance = self.userauth.creat(username, password)
        from connection import ConnectionStatusManager
        # Appeler la méthode register_user de CREAT
        result = creat_instance
        print(f'le resultata {result}')
        connecter = ConnectionStatusManager()
        connecter.set_connection_status(True)
        self.manager.transition = CustomSlideTransition(direction="right", duration=1)
        self.manager.current = 'feed_screen' 

    def clear(self, instance):
        self.welcome_label.text = "WELCOME"
        self.user_input.text = ""
        self.email_input.text = ""
        self.password_input.text = ""
        self.confirm_password_input.text = ""
        self.message_label.text = ""

    def switch_screen(self, screen_name):
        self.manager.transition = CustomSlideTransition(direction="right", duration=1)
        self.manager.current = screen_name 