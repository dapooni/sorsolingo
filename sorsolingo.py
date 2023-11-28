from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import Screen
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp

from kivy.animation import Animation


Window.size = (360, 740)

class Start(Screen):
    pass

class Login(Screen):
    pass

class Forgot(Screen):
    pass

class SignUp(Screen):
    pass

class MainWindow(Screen):
    pass

class HistoryScreen(Screen):
    def on_pre_enter(self, *args):
        self.load_search_history()

    def load_search_history(self):
        history_grid = self.ids.history_grid
        history_grid.clear_widgets()

        # Get the search history from wherever you store it
        search_history = ["Word1", "Word2", "Word3"]  # Replace with your data

        for word in search_history:
            item_layout = BoxLayout(size_hint_y=None, height=dp(36), spacing=dp(10))
            item_layout.add_widget(Label(text=word, font_size="16sp", halign="left"))

            delete_button = DeleteIconButton()
            delete_button.parent_layout = item_layout
            delete_button.word = word
            item_layout.add_widget(delete_button)

            history_grid.add_widget(item_layout)

    def delete_word(self, word):
        # Add your logic to delete the word from the search history
        # For example, if the search history is a list, you can do:
        search_history = ["Word1", "Word2", "Word3"]  # Replace with your data
        if word in search_history:
            search_history.remove(word)
            # Save the updated search history
            # For example, if your search history is stored in a file or database:
            # with open('search_history.txt', 'w') as file:
            # file.write('\n'.join(search_history))

        # Reload the search history
        self.load_search_history()

    def clear_search_history(self):
        # Add your logic to clear the entire search history
        # For example, if the search history is a list, you can do:
        search_history = []
        # Save the updated search history
        # For example, if your search history is stored in a file or database:
        # with open('search_history.txt', 'w') as file:
        #     file.write('')

        # Reload the search history
        self.load_search_history()


class DictionaryScreen(Screen):
    # def spinner_clicked(self, value): for translating


    def update_search_history(self, search_text):
        # Limit the search history to a certain number of entries (e.g., 10)
        max_history_entries = 10

        # Add the new search text to the beginning of the list
        self.search_history.insert(0, search_text)

        # Trim the list to the maximum number of entries
        self.search_history = self.search_history[:max_history_entries]

    def clear_search_history(self):
        # Clear the entire search history
        self.search_history = []

class SearchHistoryItem(OneLineAvatarIconListItem):
    def __init__(self, text="", delete_callback=None, **kwargs):
        super().__init__(text=text, **kwargs)

        # Create the delete icon and set its behavior
        delete_icon = IconLeftWidget(icon="delete")
        delete_icon.on_release = lambda: delete_callback(text)
        self.add_widget(delete_icon)

class MainWindow(Screen):
    def search_action(self, search_text):
        # Perform your search logic here
        # For example, let's update the description labels with the search results
        description_label = self.ids.description_label
        description_label.text = f"Search results for: {search_text}"

        # You can add more logic to update other UI elements or perform other actions

class Profile(Screen):
    pass

class EditProfile(Screen):
    pass

class About(Screen):
    pass

class Help(Screen):
    pass

class Logout(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class SorsolingoApp(MDApp):
    def build(self):
        self.icon = "Sorsolingo.png"
        Window.clearcolor = (1, 1, 1, 1)
        return Builder.load_file('sorsofile.kv')

if __name__ == "__main__":
    SorsolingoApp().run()