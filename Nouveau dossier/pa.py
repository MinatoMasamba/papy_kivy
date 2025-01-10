from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDIconButton
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout, BoxLayout
from kivymd.uix.label import MDLabel

# Définir la taille de la fenêtre
Window.size = (360, 640)

class FeedScreen(Screen):
    """Écran principal avec un feed scrollable."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # En-tête
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=56,
            padding=10,
            spacing=10
        )
        header.add_widget(MDIconButton(icon="menu", on_release=lambda x: self.switch_screen("menu_screen")))
        header.add_widget(MDLabel(text="Chass_Tricks", halign="center", theme_text_color="Primary"))
        layout.add_widget(header)

        # Contenu scrollable
        scroll = ScrollView()
        self.feed_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.feed_layout.bind(minimum_height=self.feed_layout.setter('height'))
        scroll.add_widget(self.feed_layout)

        layout.add_widget(scroll)
        self.add_widget(layout)

    def switch_screen(self, screen_name):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = screen_name

    def create_post(self, index):
        """Crée une publication simulée."""
        post = BoxLayout(orientation='vertical', size_hint_y=None, height=300, padding=10, spacing=10)

        # En-tête de la publication
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        header.add_widget(Image(source="car4.png", size_hint=(None, None), size=(50, 50)))
        header.add_widget(MDLabel(text=f"Auteur {index}", halign="left"))
        post.add_widget(header)

        # Image
        card = MDCard(size_hint_y=None, height=200, radius=[15])
        card.add_widget(Image(source="car1.jpg", allow_stretch=True, keep_ratio=True))
        post.add_widget(card)

        # Actions
        actions = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        actions.add_widget(MDIconButton(icon="heart-outline"))
        actions.add_widget(MDIconButton(icon="comment-outline"))
        actions.add_widget(MDIconButton(icon="send-outline"))
        post.add_widget(actions)

        return post

    def on_enter(self):
        self.feed_layout.clear_widgets()  # Évite la duplication
        for i in range(10):  # Limite le nombre de publications
            self.feed_layout.add_widget(self.create_post(i))


class MenuScreen(Screen):
    """Écran du menu latéral."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Boutons du menu
        buttons = [
            ("home", "Accueil", lambda x: self.switch_screen("feed_screen")),
            ("settings", "Options", lambda x: print("Option sélectionnée")),
            ("account", "Profil", lambda x: print("Profil sélectionné")),
        ]
        for icon, text, action in buttons:
            btn = MDRaisedButton(
                text=text,
                icon=icon,
                size_hint=(0.8, None),
                height=50,
                pos_hint={"center_x": 0.5},
                on_release=action
            )
            layout.add_widget(btn)

        self.add_widget(layout)

    def switch_screen(self, screen_name):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = screen_name


class MyApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FeedScreen(name="feed_screen"))
        sm.add_widget(MenuScreen(name="menu_screen"))
        return sm


if __name__ == "__main__":
    MyApp().run()
