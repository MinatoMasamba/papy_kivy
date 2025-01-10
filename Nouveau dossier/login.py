from kivy import Config
Config.set('graphics', 'multisamples', '0')
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.textfield import MDTextFieldRound

from creat import CREAT  # Import de la classe CREAT

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Brown"

        # Interface utilisateur
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.welcome_label = MDLabel(text="WELCOME", font_size=40, halign='center', size_hint_y=None, height=50)
        layout.add_widget(self.welcome_label)

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
        layout.add_widget(self.user_input)

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
        layout.add_widget(self.email_input)

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
        layout.add_widget(self.password_input)

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
        layout.add_widget(self.confirm_password_input)

        self.message_label = MDLabel(text="", halign='center', theme_text_color="Error")
        layout.add_widget(self.message_label)

        login_button = MDRoundFlatButton(text="LOGIN", font_size=12, size_hint_x=None, width=200, pos_hint={"center_x": 0.5})
        login_button.bind(on_press=self.logger)
        layout.add_widget(login_button)

        clear_button = MDRoundFlatButton(text="CLEAR", font_size=12, size_hint_x=None, width=200, pos_hint={"center_x": 0.5})
        clear_button.bind(on_press=self.clear)
        layout.add_widget(clear_button)

        return layout

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
        creat_instance = CREAT(username, password)

        # Appeler la méthode register_user de CREAT
        result = creat_instance.register_user()

        if result.get('success'):
            self.welcome_label.text = f"Welcome {username}!"
            self.message_label.text = result.get('message')
        else:
            self.message_label.text = result.get('message')

    def clear(self, instance):
        self.welcome_label.text = "WELCOME"
        self.user_input.text = ""
        self.email_input.text = ""
        self.password_input.text = ""
        self.confirm_password_input.text = ""
        self.message_label.text = ""

if __name__ == "__main__":
    MainApp().run()
