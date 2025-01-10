from kivy import Config
Config.set('graphics', 'multisamples', '0')
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from kivy.lang import Builder
from kivy.core.image import Image as CoreImage
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from tkinter import filedialog
from kivymd.uix.button import MDFlatButton
import os


class LoadFileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog = None
        self.selected_file_path = None
        #self.show_add_post_dialog()

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

    MDTextField:
        id: detail_field
        hint_text: "Détail du post"
        multiline: True
        helper_text: "Ajoutez une description ici"
        helper_text_mode: "on_focus"

    MDRoundFlatButton:
        id: file_button
        text: "Choisir un fichier (Image, PDF, Document)"
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

    def select_file(self):
        """
        Simule une boîte de sélection de fichier pour choisir une image, un PDF ou un document.
        Si un fichier image est sélectionné, affiche un aperçu dans la boîte de dialogue.
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("Tous les fichiers", "*.*"),
                       ("Images", "*.png;*.jpg;*.jpeg"),
                       ("Documents", "*.pdf;*.docx;*.txt")]
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
        """
        Publie le post avec les détails et le fichier sélectionné.
        """
        detail = self.dialog.content_cls.ids.detail_field.text
        file_path = getattr(self, 'selected_file_path', None)

        if not detail:
            self.show_error("Veuillez remplir le champ de détail.")
            return

        #if not file_path:
            #self.show_error("Veuillez sélectionner un fichier.")
            #return

        # Logique de publication (ex. : enregistrement ou envoi au serveur)
        #print(f"Post publié : Détail={detail}, Fichier={file_path}")

        # Fermer la boîte de dialogue après la publication
        self.close_dialog()

    def show_error(self, message):
        """
        Affiche une erreur sous forme de Snackbar.
        """
        Snackbar(text=message).open()

    def close_dialog(self, *args):
        """
        Ferme la boîte de dialogue si elle est ouverte.
        """
        if self.dialog:
            self.dialog.dismiss()


