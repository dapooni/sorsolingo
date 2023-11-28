from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu

KV = '''
MDBoxLayout:
    orientation: "vertical"
    size_hint: .82, .05
    pos_hint: {"center_x": .5, "center_y": .67}

    MDTextField:
        id: dialect
        hint_text: "Choose Dialect"
        on_focus: if self.focus: app.show_menu(self)

'''

class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def show_menu(self, textfield):
        menu_items = [
            {"text": "Bisakol", "viewclass": "OneLineListItem", "on_release": lambda x: self.menu_callback(x)},
            {"text": "Tagalog", "viewclass": "OneLineListItem", "on_release": lambda x: self.menu_callback(x)},
            {"text": "English", "viewclass": "OneLineListItem", "on_release": lambda x: self.menu_callback(x)},
        ]
        self.menu = MDDropdownMenu(items=menu_items, width_mult=4)
        self.menu.caller = textfield
        self.menu.open()

    def menu_callback(self, text):
        self.root.ids.dialect.text = text
        self.menu.dismiss()

Test().run()
