from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel


class MyApp(MDApp):
    def build(self):
        # Conteneur principal
        layout = MDBoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Création du label
        content_label2 = MDLabel(
            text="Ceci est un texte très long qui doit commencer en haut et continuer vers le bas sans dépasser les limites. "
                 "Nous ajustons dynamiquement la hauteur pour contenir tout le contenu.",
            size_hint=(None, None),  # Taille non proportionnelle
            width=dp(300),  # Largeur du label
            text_size=(dp(300), None),  # Contraint la largeur uniquement
            halign="left",  # Alignement horizontal à gauche
            valign="top",  # Alignement vertical en haut
            theme_text_color="Primary",  # Couleur principale du texte
            font_style='Subtitle2',  # Style du texte
            bold=True,  # Texte en gras
        )

        # Ajuster la hauteur dynamiquement
        content_label2.bind(
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )

        # Ajouter le label au layout principal
        layout.add_widget(content_label2)

        return layout


if __name__ == "__main__":
    MyApp().run()
