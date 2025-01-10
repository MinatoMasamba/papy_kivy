from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from tkinter import filedialog


class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.selected_file_path = None
        self.show_options_dialog()

    def show_options_dialog(self):
        """
        Affiche une boîte de dialogue avec des options principales.
        """
        self.dialog = MDDialog(
            type="custom",
            size_hint=(None, None),
            height="600dp",
            width='350dp',
            content_cls=Builder.load_string(
                """
BoxLayout:
    orientation: 'vertical'
    spacing: "12dp"
    size_hint_y: None
    height: self.minimum_height
    size_hint: None, None  # Désactive le redimensionnement automatique
    size: "300dp", "300dp"  # Définir largeur et hauteur fixes (ici 300x300)

    MDLabel:
        text: "Options Disponibles"
        font_style: "H6"
        halign: "center"
        size_hint_y: None
        height: self.texture_size[1]

    MDRoundFlatButton:
        text: "Ajouter un Post"
        pos_hint: {"center_x": 0.5}
        on_release: root.add_post()

    MDRoundFlatButton:
        text: "Ajouter aux Favoris"
        pos_hint: {"center_x": 0.5}
        on_release: root.add_to_favorites()

    MDRoundFlatButton:
        text: "Ne Plus Voir"
        pos_hint: {"center_x": 0.5}
        on_release: root.hide_post()
                """
            ),
            buttons=[
                MDFlatButton(
                    text="FERMER",
                    on_release=self.close_dialog
                )
            ],
        )
        self.dialog.open()

    def add_post(self):
        """
        Action pour ajouter un post.
        """
        self.close_dialog()
        self.show_file_selection_dialog()

    def add_to_favorites(self):
        """
        Action pour ajouter aux favoris.
        """
        self.show_snackbar("Le post a été ajouté aux favoris.")

    def hide_post(self):
        """
        Action pour ne plus voir le post.
        """
        self.show_snackbar("Le post est masqué.")

    def show_file_selection_dialog(self):
        """
        Affiche une boîte de dialogue pour choisir un fichier à associer à un post.
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("Tous les fichiers", "*.*"),
                       ("Images", "*.png;*.jpg;*.jpeg"),
                       ("Documents", "*.pdf;*.docx;*.txt")]
        )

        if file_path:
            self.selected_file_path = file_path
            self.show_snackbar(f"Fichier sélectionné : {file_path.split('/')[-1]}")
        else:
            self.show_snackbar("Aucun fichier sélectionné.")

    def show_snackbar(self, message):
        """
        Affiche un message temporaire sous forme de Snackbar.
        """
        Snackbar(text=message).show()

    def close_dialog(self, *args):
        """
        Ferme la boîte de dialogue si elle est ouverte.
        """
        if self.dialog:
            self.dialog.dismiss()


class Main(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='Load'))
        return sm


if __name__ == "__main__":
    Main().run()
