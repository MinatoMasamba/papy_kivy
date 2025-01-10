from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget

kv = """

MDList:
    id: comments_list
    OneLineIconListItem:
        text: "Commentaire exemple"
        IconLeftWidget:
            icon: "account"
"""

class MainApp(MDApp):
    def build(self):
        # Créer le layout de publication
        post_layout = BoxLayout(orientation='vertical', size_hint_y=None,
                                height=350, padding=10, spacing=10)
        
        # Charger et ajouter le layout KV
        comment_layout = Builder.load_string(kv)
        post_layout.add_widget(comment_layout)

        return post_layout

if __name__ == '__main__':
    MainApp().run()
