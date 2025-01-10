from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRoundFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextFieldRound
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """
        Ouvre un menu latéral avec des options.
        """
        # Crée la disposition principale du menu (fixée en haut à gauche)
        menu_layout = MDBoxLayout(
            orientation='vertical',
            spacing=10,  # Espacement entre les boutons
            size_hint=(None, 1),  # Largeur fixe, ajustée à la hauteur
            width=250 , # Largeur fixée du menu
            pos_hint={"center_x": 0.4, "center_y": 0.5}
        )

        # Fonction pour créer un bouton personnalisé avec icône et texte
        def create_button_with_icon_and_text(icon, text, on_press_action):
            class CustomButton(ButtonBehavior, BoxLayout):
                def __init__(self, **kwargs):
                    super().__init__(**kwargs)
                    self.orientation = 'horizontal'
                    self.size_hint = (None, None)
                    self.size = (250, 50)
                    self.spacing = 10

                    # Arrière-plan arrondi
                    with self.canvas.before:
                        Color(0.2, 0.6, 1, 1)  # Couleur bleue
                        self.bg_rect = RoundedRectangle(
                            size=self.size,
                            pos=self.pos,
                            radius=[20, 20, 20, 20]  # Coins arrondis
                        )

                    # Mettre à jour la taille et la position
                    self.bind(pos=self.update_canvas, size=self.update_canvas)

                def update_canvas(self, *args):
                    self.bg_rect.size = self.size
                    self.bg_rect.pos = self.pos

            # Crée un bouton interactif
            button_layout = CustomButton()

            # Icône à gauche
            icon_button = MDIconButton(
                icon=icon,
                user_font_size="24sp",  # Taille de l'icône
                size_hint=(None, None),
                size=(40, 40)
            )

            # Texte à droite
            label = MDLabel(
                text=text,
                halign="left",  # Alignement du texte
                valign="middle",
                size_hint=(1, 1),
            )

            # Ajouter l'icône et le texte au bouton
            button_layout.add_widget(icon_button)
            button_layout.add_widget(label)

            # Associer l'action au clic
            button_layout.bind(on_press=lambda instance: on_press_action(instance))

            # Ajouter le bouton personnalisé au layout du menu
            menu_layout.add_widget(button_layout)

        # Création de chaque bouton du menu
        create_button_with_icon_and_text("home", "Accueil", lambda x: self.switch_screen("feed_screen"))
        create_button_with_icon_and_text("heart", "Favorie ", lambda x: print("Option 1 sélectionnée"))
        create_button_with_icon_and_text("tools", "Tp", lambda x: self.switch_screen('tp_file'))
        create_button_with_icon_and_text("clipboard-text", "Interro", lambda x: self.switch_screen('interro_file'))
        create_button_with_icon_and_text("note", "Examen", lambda x: self.switch_screen('exam_file'))
        create_button_with_icon_and_text("account", "Compte", lambda x: self.switch_screen('compte_list'))
        create_button_with_icon_and_text("help", "Aide", lambda x: print("Option 3 sélectionnée"))
        create_button_with_icon_and_text("cog", "Parametre", lambda x: print("Option 4 sélectionnée")) 

        # Ajoute des espaces vides pour équilibrer le menu
        menu_layout.add_widget(Widget(size_hint_x=None, width=60))
        menu_layout.add_widget(Widget(size_hint_x=None, width=60))

        # Ajoute le menu_layout à l'écran principal
        self.add_widget(menu_layout)

    def switch_screen(self, screen_name, choisi=None):
        from connection import ConnectionStatusManager
        from fonction import CustomSlideTransition

        self.statut = ConnectionStatusManager()

        self.manager.transition = CustomSlideTransition(direction="left", duration=1)

        if screen_name == 'feed_screen':
            if self.statut.get_connection_status():          
                self.manager.current = screen_name
            else:
                self.manager.current = 'create_compte'
    
        else:
            self.manager.current = screen_name

        
