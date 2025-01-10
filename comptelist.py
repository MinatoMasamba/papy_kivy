from kivy import Config
Config.set('graphics', 'multisamples', '0')
import os
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from connection import ConnectionStatusManager
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.core.image import Image as CoreImage
from kivy.metrics import dp
from kivymd.uix.button import MDRoundFlatButton
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
#from kivymd.uix.iconbutton import MDIconButton
from fonction import CustomSlideTransition
import os
from kivy.uix.checkbox import CheckBox
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget
from data import UserAuth


class compteItem(OneLineAvatarIconListItem):
    def __init__(self, file_path, **kwargs):
        super().__init__(**kwargs)
        self.file_path = file_path
        self.text = str(file_path)
        self.font_style = 'Overline'
        self.halign= "center"
        self.font_size= 18

        # Ajouter l'icône et la checkbox
        if 'aucun compte trouver' != file_path:
            icon = IconLeftWidget(icon="account-outline")
            self.add_widget(icon)
        else:
            icon = IconLeftWidget(icon="")
            self.add_widget(icon)


        self.checkbox = CheckBox(size_hint_x=None, width=50)
        self.add_widget(self.checkbox)

    def is_selected(self):
        return self.checkbox.active

class CompteList(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.user = UserAuth()

        # ScrollView pour la liste des fichiers
        scroll_view = ScrollView()
        file_list = MDList(
             radius=[5],
            padding=20, spacing=10,
        )

        # Ajouter les fichiers au MDList
        if self.user.list_users():
            for file_name in self.user.list_users():
                item = compteItem(file_name)
                file_list.add_widget(item)
        else:
            item = compteItem('aucun compte trouver')
            file_list.add_widget(item)


        scroll_view.add_widget(file_list)
        self.add_widget(Widget(size_hint_y=None, height=50))
        self.add_widget(scroll_view)

    def get_selected_files(self):
        return [child.file_path for child in self.children[0].children if child.is_selected()]

class CompteListScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        file_list = CompteList()
        

        self.add_widget(MDIconButton(
            icon="arrow-left",
            pos_hint={"center_x": 0.1, "center_y": 0.955},
            height=dp(20),
            on_release=lambda x: self.switch_screen("menu_screen",None)
        ))
        deconnecter = ConnectionStatusManager()
        self.add_widget(file_list)
        self.add_widget(MDRoundFlatButton(text="Deconnecter", font_size=12,
                                              pos_hint={"center_x": 0.5,"center_y": 0.2},
                                              on_release=lambda x: (deconnecter.set_connection_status(False),
                                                                    self.switch_screen("menu_screen",file_list))))

    
    
    def switch_screen(self, screen_name,file_list=None):
        if file_list is not None :
            file_list.user.logout()
        self.manager.transition = CustomSlideTransition(direction="right", duration=1)
        self.manager.current = screen_name