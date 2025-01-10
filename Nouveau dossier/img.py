from kivy.graphics import Color, Ellipse, Rectangle, StencilPush, StencilUse, StencilPop, StencilUnUse
from kivy.uix.widget import Widget
from kivy.core.image import Image as CoreImage
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivymd.app import MDApp

class CircularProfileImage(Widget):
    source = StringProperty("default.jpg")  # Chemin vers l'image par défaut

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
        """Chargement de l'image source et mise à jour de la texture."""
        try:
            self.image_texture = CoreImage(self.source).texture
            self.image_rect.texture = self.image_texture
        except Exception as e:
            print(f"Erreur lors du chargement de l'image : {e}")

class MainApp(MDApp):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(10))

        # Ajouter une carte pour contenir l'image circulaire
        profile_card = MDCard(
            orientation="vertical",
            size_hint=(None, None),
            size=(dp(200), dp(250)),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            md_bg_color=(0.95, 0.95, 0.95, 1),  # Gris clair
            radius=[dp(20)]  # Coins arrondis
        )

        # Ajouter l'image circulaire dans la carte
        profile_image = CircularProfileImage(
            source="car5.jpg",
            size_hint=(None, None),
            size=(dp(150), dp(150)),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )

        profile_card.add_widget(Widget(size_hint=(1, None), height=dp(20)))  # Espacement en haut
        profile_card.add_widget(profile_image)

        layout.add_widget(profile_card)

        return layout

if __name__ == "__main__":
    MainApp().run()
