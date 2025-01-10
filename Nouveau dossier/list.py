import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
""""
 ['H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'Subtitle1', 'Subtitle2', 'Body1', 'Body2', 'Button', 'Caption', 'Overline', 'Icon']
"""
class FileItem(OneLineAvatarIconListItem):
    def __init__(self, file_path, **kwargs):
        super().__init__(**kwargs)
        self.file_path = file_path
        self.text = os.path.basename(file_path)
        self.font_style = 'Overline'
        self.halign= "center"
        self.font_size= 18

        # Ajouter l'icône et la checkbox
        icon = IconLeftWidget(icon="file-outline")
        self.add_widget(icon)

        self.checkbox = CheckBox(size_hint_x=None, width=50)
        self.add_widget(self.checkbox)

    def is_selected(self):
        return self.checkbox.active

class FileList(BoxLayout):
    def __init__(self, directory, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        # ScrollView pour la liste des fichiers
        scroll_view = ScrollView()
        file_list = MDList()

        # Ajouter les fichiers au MDList
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if os.path.isfile(file_path):
                item = FileItem(file_path)
                file_list.add_widget(item)

        scroll_view.add_widget(file_list)
        self.add_widget(scroll_view)

    def get_selected_files(self):
        return [child.file_path for child in self.children[0].children if child.is_selected()]

class FileListScreen(Screen):
    def __init__(self, directory, **kwargs):
        super().__init__(**kwargs)
        file_list = FileList(directory)
        self.add_widget(file_list)

class FileApp(MDApp):
    def build(self):
        directory = "."  # Remplace par le répertoire de ton choix
        sm = ScreenManager()
        sm.add_widget(FileListScreen(directory, name='file_list'))
        return sm

if __name__ == '__main__':
    FileApp().run()
