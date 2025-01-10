from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivy.lang import Builder
from tkinter import filedialog
from kivymd.uix.button import MDFlatButton


class MainApp(MDApp):
    def build(self):
        return Builder.load_string("""
BoxLayout:
    orientation: 'vertical'
    MDRaisedButton:
        text: "Ajouter un Post"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        on_release: app.show_add_post_dialog()
        """)

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
        on_release: app.select_file()

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
        on_release: app.publish_post()

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
        from tkinter import filedialog
        from kivy.clock import Clock
        from kivy.uix.image import CoreImage
        import os

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
                try:
                    img = CoreImage(file_path)
                    
                    def update_image_preview(*args):
                        self.dialog.content_cls.ids.preview_image.texture = img.texture
                    
                    Clock.schedule_once(update_image_preview, 0)
                except Exception as e:
                    self.dialog.content_cls.ids.preview_image.source = ""
                    print(f"Erreur lors du chargement de l'image : {e}")
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

        if not file_path:
            self.show_error("Veuillez sélectionner un fichier.")
            return

        # Logique de publication (enregistrement local ou envoi au serveur)
        print(f"Post publié : Détail={detail}, Fichier={file_path}")

        # Fermer la boîte de dialogue après la publication
        self.close_dialog()


    def show_error(self, message):
        """
        Affiche une erreur sous forme de Snackbar.
        """
        from kivymd.uix.snackbar import Snackbar

        Snackbar(text=message).show()


    def close_dialog(self, *args):
        """
        Ferme la boîte de dialogue si elle est ouverte.
        """
        if self.dialog:
            self.dialog.dismiss()


if __name__ == "__main__":
    MainApp().run()
