from kivy import Config
Config.set('graphics', 'multisamples', '0')
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from connection import ConnectionStatusManager
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from kivy.graphics import Ellipse, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget


from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRoundFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.behaviors import ButtonBehavior
from kivy.core.window import Window
from kivymd.app import MDApp

from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.boxlayout import MDBoxLayout 
from kivymd.uix.label import MDLabel
#from kivymd.uix.iconbutton import MDIconButton
from fonction import CustomSlideTransition,HeartButton
from liste_compte import CompteListScreen
from fonction import truncate_text
from kivymd.uix.dialog import MDDialog
# Définir la taille de la fenêtre pour une vue mobile
Window.size = (360, 640)
from kivymd.app import MDApp
#from load_file import LoadFileScreen
from kivymd.uix.button import MDFloatingActionButton
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from tkinter import filedialog
from kivymd.uix.button import MDFlatButton
import os
from loadFile import LoadFileScreen
from createcompte import CreatCompte
from kivymd.uix.label import MDLabel
from kivy.uix.behaviors.button import ButtonBehavior
from data import PostsAndSocialInteractions
from kivy.uix.image import AsyncImage
from kivymd.uix.textfield import MDTextField
from kivy.graphics import PushMatrix, PopMatrix, Rotate



# Créez une sous-classe de MDLabel avec ButtonBehavior
class ClickableMDLabel(ButtonBehavior, MDLabel):
    pass

from kivy.graphics import Rotate, PushMatrix, PopMatrix
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import AsyncImage
from kivy.graphics import Rotate, PushMatrix, PopMatrix


class ClickableImage(ButtonBehavior, AsyncImage):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Ajout de la rotation dans le Canvas
        with self.canvas.before:
            PushMatrix()
            self.rotation = Rotate(angle=90, origin=self.center)  # Angle initial
        with self.canvas.after:
            PopMatrix()

        # Met à jour l'origine de la rotation si la position ou la taille change
        self.bind(pos=self.update_origin, size=self.update_origin)

    def update_origin(self, *args):
        """Met à jour l'origine de la rotation."""
        self.rotation.origin = self.center

    def set_orientation(self, angle):
        """Change l'orientation de l'image en ajustant l'angle de rotation."""
        self.rotation.angle = angle  # Change l'angle de rotation




from kivymd.uix.button import MDRoundFlatButton, MDFlatButton

class FeedScreen(Screen):
    """
    Écran principal avec un feed scrollable, un header fixe, un menu latéral, et des publications simulées.
    """

    def __init__(self,auth_manager, **kwargs):
        super().__init__(**kwargs)

        # Layout principal
        layout = BoxLayout(orientation='vertical')
        self.auth_manager = auth_manager
        self.post_info = LoadFileScreen()
        self.auth_instance = UserAuth()
        posts_manager = PostsAndSocialInteractions(auth=self.auth_instance)
        self.response = posts_manager.get_all_posts()


        
       

        # En-tête fixe
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=56,
            padding=10,
            spacing=10,
            pos_hint={'top': 1}
        )
        header.add_widget(MDIconButton(icon="menu", size_hint_x=None, on_release=lambda x: self.switch_screen("menu_screen")))
        header.add_widget(Widget(size_hint_x=None, width=30))
        header.add_widget(MDLabel(text="source academique", halign="left", theme_text_color="Secondary",font_size=18,bold=True))
        header.add_widget(Widget(size_hint_x=None, width=20))
        header.add_widget(MDIconButton(
    icon="account",
    size_hint_x=None,
    on_release=lambda x: self.auth_manager.check_authentication()
))

        layout.add_widget(header)

        # Contenu scrollable
        scroll = ScrollView()
        self.feed_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.feed_layout.bind(minimum_height=self.feed_layout.setter('height'))
        scroll.add_widget(self.feed_layout)

        layout.add_widget(scroll)
        self.add_widget(layout)
        if self.response:
            if self.response != 'en_attente':
                self.on_enter()
            else:
                self.add_widget(MDLabel(
                text="en attente",
                halign="center",
                font_style="H3"
            ))
        else:
            self.add_widget(MDLabel(
                text="Veillez vous connecter svp",
                halign="center",
                font_style="H5"
            ))

    def switch_screen(self, screen_name):
        """
        Change l'écran en fonction de l'option sélectionnée.
        """
        if screen_name == 'menu_screen':
            self.manager.transition = CustomSlideTransition(direction="right", displacement=0.5, duration=0.5)
        else:
            self.manager.transition = CustomSlideTransition(direction="left", displacement=0.5, duration=0.5)
        self.manager.current = screen_name

    def show_comment_dialog(self, existing_comments=None, post_id=None):
        """
        Affiche une boîte de dialogue contenant les commentaires d'un post.
        Les commentaires sont réinitialisés après envoi ou fermeture de la boîte de dialogue.
        """
        if existing_comments is None:
            existing_comments = []

        # Fonction pour rafraîchir les commentaires dans le conteneur
        def refresh_comments():
            # Vider le conteneur
            comments_container.clear_widgets()
            # Recharger les commentaires depuis la liste `existing_comments`
            for comment in existing_comments:
                author_details = comment['author_details']['username']
                commentaire = comment['content']

                # Créez un MDCard pour chaque commentaire
                card = MDCard(
                    orientation="vertical",
                    size_hint=(1, None),
                    height=dp(100),
                    padding=dp(10),
                    spacing=dp(10),
                )

                # Ajouter une disposition verticale dans le MDCard
                content_box = MDBoxLayout(
                    orientation='vertical',
                    spacing=dp(5),
                    size_hint=(1, None),
                    height=dp(80)
                )

                # Ajoutez le nom de l'utilisateur et le commentaire
                user_label = MDLabel(
                    text=f"{author_details}: {commentaire}",
                    font_style='Subtitle2',
                    size_hint=(1, None),
                    halign="left",
                    bold=True,
                    text_size=(None, None),
                )

                # Ajouter le label dans la boîte de contenu
                content_box.add_widget(user_label)

                # Ajouter la boîte de contenu au MDCard
                card.add_widget(content_box)

                # Ajouter le MDCard au conteneur principal
                comments_container.add_widget(card)

        # Créer une disposition verticale pour contenir les commentaires
        comments_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=None,
            padding=dp(10)
        )
        comments_container.bind(minimum_height=comments_container.setter('height'))

        # Charger les commentaires initiaux
        refresh_comments()

        # Créer un ScrollView pour permettre le défilement
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(comments_container)

        # Champ de texte pour écrire un commentaire
        comment_field = MDTextField(
            hint_text="Écrire un commentaire"
        )

        # Bouton pour envoyer un commentaire
        send_button = MDRoundFlatButton(
            text="Envoyer",
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.add_comment_and_refresh(comment_field.text, post_id, existing_comments, refresh_comments)
        )

        # Disposition principale
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(250)
        )

        # Ajouter les widgets à la disposition principale
        content.add_widget(scroll)
        content.add_widget(comment_field)
        content.add_widget(send_button)

        # Créer une boîte de dialogue modale
        self.dialog = MDDialog(
            title="Commentaires",
            type="custom",
            content_cls=content,
            buttons=[
                MDRoundFlatButton(
                    text="Fermer",
                    on_release=lambda x: (self.dialog.dismiss(force=True), refresh_comments())
                )
            ]
        )

        # Afficher la boîte de dialogue
        self.dialog.open()

    def add_comment_and_refresh(self, comment_text, post_id, existing_comments, refresh_comments):
        profile = self.auth_instance.get_profile()
        """
        Ajoute un nouveau commentaire et rafraîchit la liste des commentaires.
        """
        if comment_text.strip():
            # Ajouter le commentaire dans la liste des commentaires existants
            new_comment = {
                'author_details': {'username': profile['author_name'][0]},  # Remplacez par l'utilisateur connecté
                'content': comment_text.strip()
            }
            existing_comments.append(new_comment)

            # Actualiser l'affichage
            refresh_comments()
            self.add_comment(comment_text=comment_text,post_id=post_id)



    def close_dialog(self, *args):
        self.dialog.dismiss()

    def add_comment(self,comment_text,post_id):
        #print(f"Commentaire: {comment_text}")
        add = PostsAndSocialInteractions(UserAuth())
        add.comment_on_post(post_id=post_id,comment=comment_text)
        #self.dialog.dismiss()

    def contenent(self, text):
        # Créer un label pour afficher tout le texte avec des sauts de ligne automatiques
        text_label = MDLabel(
            text=text,
            font_size=16,
            halign='left',
            valign='top',
            size_hint_y=None,
            text_size=(dp(300), None)  # Fixer une largeur pour gérer le retour à la ligne
        )
        
        # Redimensionner automatiquement la hauteur du label selon le contenu
        text_label.bind(
            texture_size=lambda instance, value: setattr(instance, 'height', value[1])
        )
        
        # Ajouter le label dans un ScrollView pour gérer le défilement
        scroll = ScrollView(size_hint=(1, None), height=dp(400))  # Ajuster la hauteur max
        scroll.add_widget(text_label)

        # Ajouter le ScrollView à la boîte principale
        content = MDBoxLayout(
            orientation="vertical",
            spacing=dp(12),
            size_hint_y=None,
            height=dp(400)  # Ajuster selon le contenu
        )
        content.add_widget(scroll)

        # Créer un dialogue avec un bouton de fermeture
        dialog = MDDialog(
            title="Texte complet",
            type="custom",
            content_cls=content,
            buttons=[
                MDRoundFlatButton(
                    text="Fermer",
                    on_release=lambda x: dialog.dismiss(force=True)  # Fermer le dialogue
                )
            ]
        )
        dialog.open()  # Ouvrir le dialogue


    def show_image(self,file_path):
        from kivymd.uix.boxlayout import MDBoxLayout  # Import nécessaire pour le conteneur personnalisé
        try:
            # Créer un conteneur pour l'image
            content = MDBoxLayout(
                orientation="vertical",
                size_hint=(1, None),
                height=dp(400)
            )
            content.bind(minimum_height=content.setter("height"))  # Ajuster la taille du conteneur si nécessaire

            # Ajouter l'image au conteneur
            image = AsyncImage(
                source=file_path,
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(1, 1),
                height=dp(600)
            )
            content.add_widget(image)

            # Créer le MDDialog
            dialog = MDDialog(
                title="Image",
                type="custom",
                content_cls=content,
                size_hint=(0.8, 0.8),
                buttons=[
                    MDFlatButton(text="FERMER", on_release=lambda x: dialog.dismiss())
                ]
            )
            dialog.open()
        except Exception as e:
            print(f"Erreur lors de l'affichage de l'image: {e}")  
    
    def create_post(self, post):

        # Vérifiez si le post est déjà un dictionnaire, sinon accédez au premier élément
        
        original_reponse = post
        #print(f'post original {original_reponse}')
        #if isinstance(post, list):
            #post = post[0]

        #print(f'post récupéré {post}')

        # Créer l'interface de la publication
        post_layout = BoxLayout(orientation='vertical', size_hint_y=None,
                                height=350, padding=10, spacing=10)
        post_layout.id = post[0]['post']['id']  # Attribuer l'ID du post au layout principal

        # Auteur & Photo
        header_layout = BoxLayout(orientation='horizontal',
                                size_hint_y=None,
                                height=85, padding=10,
                                spacing=10)
        profile_img = post[0]['post']['author_name'][1]
        header_layout.add_widget(ClickableImage(source=f'http://127.0.0.1:8000{profile_img}',
                                    allow_stretch=True,
                                    size_hint=(None, None),
                                    size=(50, 50)))


        # Conteneur principal
        info = BoxLayout(orientation='vertical', size_hint=(1, None), padding=(10, 5), spacing=7, width=200)

        # Premier label : Auteur
        author_label = MDLabel(
            text=str(post[0]['post']['author_name'][0]),
            font_size=18,
            bold=True,
            halign='left',
            size_hint_y=None,  # Taille fixe
            height=dp(30)  # Fixer une hauteur pour que le label ne soit pas affecté
        )

        # Deuxième label : Contenu avec gestion de retour à la ligne
        content_label = ClickableMDLabel(
            text=truncate_text(str(post[0]['post']['content']), 45),
            font_size=16,
            halign='left',
            valign='top',
            text_size=(info.width, None),  # Ajuste la largeur
            size_hint_y=None,  # Permet à la hauteur de varier
            height=dp(60),  # Fixe une hauteur maximale pour éviter d'affecter le premier label
            shorten=True  # Tronque le texte si nécessaire
        )


        # Fonction appelée lors du clic
        def on_label_click(instance):
            # Récupérer le texte du label cliqué
            label_text = str(post[0]['post']['content'])
            # Appeler une autre fonction avec ce texte
            self.contenent(label_text)

        content_label.bind(on_release=on_label_click)
        #print(f"l'ecran info {info.width}")
        # Mise à jour de la hauteur du label selon le contenu
        content_label.bind(
            width=lambda instance, value: setattr(content_label, 'text_size', (value, None)),
            texture_size=lambda instance, value: setattr(content_label, 'height', value[1])
        )

        # Ajouter les widgets au layout
        info.add_widget(author_label)
        info.add_widget(content_label)

        # Mise à jour de la hauteur totale de `info` en fonction du contenu
        info.bind(
            minimum_height=lambda instance, value: setattr(info, 'height', value)
        )

        header_layout.add_widget(info)
        header_layout.add_widget(MDIconButton(icon="dots-horizontal",
                                            size_hint_x=None,
                                            pos_hint={'top': 1},
                                            width=50))
        
        post_layout.add_widget(header_layout)

            # Contenu de la publication
        card = MDCard(
                orientation="horizontal",padding=dp(15), spacing=dp(10),
                #padding=1,
                size_hint_y=None,
                height=200,
                radius=[15],
                elevation=5,
                md_bg_color=(0.9, 0.9, 0.9, 1)  # Empêche le fond par défaut
            )

        image_layout = BoxLayout(size_hint=(1, 1), orientation="horizontal", padding=dp(10), spacing=dp(10))


        if post[0]['post']['file']:
            # Image dans le wrapper
            image_widget = ClickableImage(
                source=post[0]['post']['file'],
                allow_stretch=True,  # Permet de s'étirer pour occuper l'espace disponible
                keep_ratio=True,  # Maintient le ratio de l'image
                size=(400, 400)
            )
            def on_image_click(instance):
                image=post[0]['post']['file']
                self.show_image(file_path=image)                               

            image_widget.bind(on_release=on_image_click)
        # Ajout de l'image centrée dans le layout
            image_layout.add_widget(image_widget)

        # Ajout du layout contenant l'image au `MDCard`
            card.add_widget(image_layout)
            post_layout.add_widget(card)
        else:
            content_label2 = ClickableMDLabel(
            text=str(truncate_text(str(post[0]['post']['content']), 300)),
            size_hint=(None, None),  # Taille non proportionnelle
            width=dp(300),  # Fixe la largeur du label
            height=dp(500),
            text_size=(dp(300), None),  # Contraint uniquement la largeur, laisse la hauteur s'ajuster
            halign="center",  # Alignement horizontal à gauche
            valign="top",  # Alignement vertical en haut
            theme_text_color="Primary",  # Couleur principale du texte
            font_style='Subtitle2',  # Style de texte
            bold=True,  # Texte en gras
            size_hint_y=None,
            pos_hint={'center_y': 0.5, 'center_x': 0.5},  # Position
            #shorten=True,  # Tronque le texte si nécessaire
            ellipsis_options={'text': '...'},  # Ajoute des points de suspension si le texte est trop long)
            # Ajuster la hauteur dynamiquement en fonction du contenu
            )
            content_label2.bind(
    texture_size=lambda instance, value: setattr(instance, 'height', value[1])
)
        
            # Fonction appelée lors du clic
            def on_label_click(instance):
                # Récupérer le texte du label cliqué

                label_text = str(post[0]['post']['content'])
                # Appeler une autre fonction avec ce texte
                self.contenent(label_text)

            content_label2.bind(on_release=on_label_click)


            
            image_layout.add_widget(content_label2)
            card.add_widget(image_layout)
            post_layout.add_widget(card)



        # Actions sur la publication avec des icônes
        action_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10, spacing=20)
        action_layout.add_widget(HeartButton(size_hint_x=None, width=50, post_id=post[0]['post']['id'],verifi =post[0]['post'] ))
        action_layout.add_widget(Widget(size_hint_x=None, width=45))  # Espace vide de 85px
        existing_comments = (post[0]['post']['comments'])
        #print(f'le commentaire {existing_comments}')
        

        # Inclure l'ID dans l'appel du commentaire
        action_layout.add_widget(MDIconButton(icon="comment-outline", size_hint_x=None, width=50, 
            on_release=lambda x: self.show_comment_dialog(existing_comments=existing_comments, post_id=post[0]['post']['id'])))
        action_layout.add_widget(Widget(size_hint_x=None, width=50))  # Espace vide de 80px

        action_layout.add_widget(MDIconButton(icon="send-outline", size_hint_x=None, width=50))
        post_layout.add_widget(action_layout)

        self.add_widget(
            MDFloatingActionButton(
                icon="plus",
                md_bg_color=(0, 0.5, 1, 1),
                pos_hint={"center_x": 0.9, "center_y": 0.1},
                on_release=lambda x: self.Create_post()
            )
        )
        return post_layout

    def on_enter(self):

        self.feed_layout.clear_widgets()
        listeed = []
        if self.response:
            for i in self.response :
                if i not in listeed:
                    listeed.append(i)
                    # Vérifier si un post avec cet ID existe déjà
                    if not any(child.id == i.get('id', None) for child in self.feed_layout.children):
                        post = self.create_post([i])
                        post.id = i.get('id', None)  # Attribuer l'ID unique au post_layout
                        self.on_enter_actualise()
                        self.feed_layout.add_widget(post)


                
    def on_enter_actualise(self):
        # Nettoyer le layout avant d'ajouter de nouvelles publications

        self.feed_layout.clear_widgets()
        #print(f'réponse sur le post {response}')
        listeed = []

        for i in self.response if self.response else range(2):
            if i not in listeed:
                listeed.append(i)
                post = self.create_post([i])
                post.id = i.get('id', None)  # Attribuer l'ID unique au post_layout
                self.feed_layout.add_widget(post)

    def Create_post(self):
        self.post_info.show_add_post_dialog()
        self.post_info.dialog
        self.on_enter_actualise()

    def publish_post(self):
        """
        Publie le post avec les détails et le fichier sélectionné.
        """
        detail = self.post_info.dialog.content_cls.ids.detail_field.text
        file_path = getattr(self, 'selected_file_path', None)

        if not detail:
            self.post_info.show_error("Veuillez remplir le champ de détail.")
            return



        # Logique de publication (ex. : enregistrement ou envoi au serveur)
        print(f"Post publié : Détail={detail}, Fichier={file_path}")
        auth_instance = UserAuth()
        posts_manager = PostsAndSocialInteractions(auth=auth_instance)
        response = posts_manager.create_post(detail=detail,file_path=file_path)
        # Fermer la boîte de dialogue après la publication
        self.on_enter_actualise()
        self.post_info.close_dialog()

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
            self.post_info.dialog.content_cls.ids.file_label.text = f"Fichier sélectionné : {file_name}"
            self.selected_file_path = file_path

            # Si le fichier est une image, affichez un aperçu
            if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
               self.post_info.dialog.content_cls.ids.preview_image.source = file_path
            else:
                # Supprime l'aperçu si ce n'est pas une image
                self.post_info.dialog.content_cls.ids.preview_image.source = ""
        else:
            self.post_info.dialog.content_cls.ids.file_label.text = "Aucun fichier sélectionné"
            self.post_info.dialog.content_cls.ids.preview_image.source = ""

from data import UserAuth


class AuthManager(ScreenManager):
    def __init__(self,screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.user_auth = UserAuth()
        self.statut = ConnectionStatusManager()
        self.screen_manager = screen_manager
        
    def check_authentication(self):
        print(f'etat de connexion dans check :')
        
        """
        Vérifie si l'utilisateur est connecté et affiche l'écran approprié.
        """

        if self.statut.get_connection_status():
            self.transition = CustomSlideTransition(direction="left", duration=1)
            self.screen_manager.current = "profile_screen"
        else:
            self.transition = CustomSlideTransition(direction="up", duration=1)
            self.screen_manager.current  = "create_compte"

    def openApp(self):

        if self.statut.get_connection_status():
            self.transition = CustomSlideTransition(direction="left", duration=1)
            self.screen_manager.add_widget(FeedScreen(auth_manager=self, name="feed_screen"))
        else:
            self.transition = CustomSlideTransition(direction="up", duration=1)
            self.screen_manager.add_widget(CreatCompte(name='create_compte'))


from fonction import FileInterro,FileExam,FileTP
from profile_screen import ProfileScreen
from login import Login
from menu import MenuScreen

class MyApp(MDApp):
    """
    Application principale.
    """

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "LightBlue"
        self.theme_cls.theme_style = "Light"
        sm = ScreenManager()


        
        auth_manager = AuthManager(screen_manager=sm)
        auth_manager.openApp()
        sm.add_widget(FeedScreen(auth_manager=auth_manager, name="feed_screen"))
        

        sm.add_widget(MenuScreen(name="menu_screen"))

        sm.add_widget(Login(name="login"))
        sm.add_widget(CompteListScreen(name='compte_list'))
        sm.add_widget(LoadFileScreen(name='load_file'))
        sm.add_widget(CreatCompte(name='create_compte'))
        #sm.add_widget(FileListScreen(name='list_file',manager=auth_manager,files=))
        sm.add_widget(ProfileScreen(name="profile_screen"))
        sm.add_widget(FileInterro(name='interro_file'))
        sm.add_widget(FileExam(name='exam_file'))
        sm.add_widget(FileTP(name='tp_file'))


        


        return sm

if __name__ == "__main__":
    MyApp().run()





