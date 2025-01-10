from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFloatingActionButton
from kivy.uix.boxlayout import BoxLayout

class MyApp(MDApp):
    def build(self):
        # Définir une disposition verticale
        layout = BoxLayout(orientation="vertical", padding="12dp", spacing="12dp")

        # Ajouter un label
        label = MDLabel(
            text="Cliquez sur le bouton ci-dessous",
            halign="center",
            font_style="H5"
        )
        layout.add_widget(label)

        # Ajouter un bouton flottant avec une icône "+"
        add_button = MDFloatingActionButton(
            icon="plus",
            pos_hint={"center_x": 0.5},
            md_bg_color=self.theme_cls.primary_color,
            on_release=self.on_add_button_pressed
        )
        layout.add_widget(add_button)

        return layout

    def on_add_button_pressed(self, *args):
        print("Bouton Ajouter pressé !")

if __name__ == "__main__":
    MyApp().run()
