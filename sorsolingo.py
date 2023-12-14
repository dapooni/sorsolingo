from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.app import App
from kivymd.uix.list import OneLineListItem

import sqlite3 as sql
from transformers import pipeline
Window.size = (360, 740)


class Start(Screen):
    pass


class Login(Screen):
    user = ObjectProperty()
    email = ObjectProperty()
    password = ObjectProperty()

    def identify(self):
        conn = sql.connect('profiles.db')
        c = conn.cursor()
        c.execute("SELECT * FROM profiles WHERE email=? AND password=?",
                  (self.email.text,self.password.text))
        result = c.fetchone()

        if result:
            app = App.get_running_app()
            app.set_current_user(result[1])
            print("Login successful!")
            self.manager.transition.direction = "left"
            self.manager.current = "main"
        else:
            print("Invalid email or password")
            self.email.text = ""
            self.password.text = ""
            error_label = MDLabel(
                text="Invalid email or password",
                halign="center",
                pos_hint={"center_x": .35, "center_y": .445},
                font_name="fonts/RobotoCondensed-Regular.ttf",
                theme_text_color="Custom",
                text_color=(1, 0, 0, 1)
            )
            self.add_widget(error_label)
            Clock.schedule_once(self.remove_error_label, 1.5)
        conn.close()

    def remove_error_label(self, dt):
        self.remove_widget(self.children[0])


class Forgot(Screen):
    email = ObjectProperty()

    def reset_pass(self):
        conn = sql.connect('profiles.db')
        c = conn.cursor()
        c.execute("SELECT password FROM profiles WHERE email=?", (self.email.text,))
        result = c.fetchone()

        if result:
            print(f"Password for {self.email.text}: {result[0]}")
            self.manager.transition.direction = "left"
            self.manager.current = "login"
        else:
            print(f"No password found for the email: {self.email.text}")
            message_email = MDLabel(
                text="No email found",
                halign="center",
                pos_hint={"center_x": .25, "center_y": .375},
                font_name="fonts/RobotoCondensed-Regular.ttf",
                theme_text_color="Custom",
                text_color=(1, 0, 0, 1)
            )
            self.add_widget(message_email)
            Clock.schedule_once(self.remove_error_label, 1.5)
        conn.close()

    def remove_error_label(self, dt):
        self.remove_widget(self.children[0])


class SignUp(Screen):
    email = ObjectProperty()
    password = ObjectProperty()

    def email_exists(self, email):
        conn = sql.connect('profiles.db')
        c = conn.cursor()
        c.execute("SELECT email FROM profiles WHERE email=?", (email,))
        result = c.fetchone()
        conn.close()
        return bool(result)

    def submit(self):
        if not self.email.text or not self.user.text or not self.password.text:
            print("Please fill in all fields.")
            message_email = MDLabel(
                text="Please fill in all fields",
                halign="center",
                pos_hint={"center_x": .3, "center_y": .455},
                font_name="fonts/RobotoCondensed-Regular.ttf",
                theme_text_color="Custom",
                text_color=(1, 0, 0, 1)
            )
            self.add_widget(message_email)
            Clock.schedule_once(self.remove_error_label, 1.5)
            return

        if self.email_exists(self.email.text):
            self.email.text = ""
            print("Email already exists.")
            message_email = MDLabel(
                text="Email already exists!",
                halign="center",
                pos_hint={"center_x": .3, "center_y": .455},
                font_name="fonts/RobotoCondensed-Regular.ttf",
                theme_text_color="Custom",
                text_color=(1, 0, 0, 1)
            )
            self.add_widget(message_email)
            Clock.schedule_once(self.remove_error_label, 1.5)
        else:
            conn = sql.connect('profiles.db')
            c = conn.cursor()
            c.execute("""INSERT INTO profiles(
                        user,
                        email,
                        password) VALUES(?,?,?) 
                    """, (self.user.text, self.email.text, self.password.text))
            conn.commit()
            conn.close()
            self.manager.transition.direction = "left"
            self.manager.current = "login"

    def remove_error_label(self, dt):
        self.remove_widget(self.children[0])


class MainWindow(Screen):
    pass

class DictionaryScreen(Screen):
    translate_input = ObjectProperty()
    translate_output = ObjectProperty()

    def spinner_clicked(self, value):
        input = self.ids.spinner_id.text
        if input=="English":
            self.ids.spinner_id2.values = ["Bisakol"]
        if input=="Bisakol":
            self.ids.spinner_id2.values = ["English", "Tagalog"] 
        if input=="Tagalog":
            self.ids.spinner_id2.values = ["Bisakol"]                       

        if input=="English" and value=="Bisakol":
            pipe = pipeline("text2text-generation", model="dapooni/sorsolingo-mt-en-bsl")
            translation = pipe(self.ids.translate_input.text)[0]["generated_text"]
            self.ids.translate_output.text = f'{translation}'
        elif input=="Bisakol" and value=="English":
            pipe = pipeline("text2text-generation", model="dapooni/sorsolingo-mt-bsl-en")
            translation = pipe(self.ids.translate_input.text)[0]["generated_text"]
            self.ids.translate_output.text = f'{translation}'
        elif input=="Tagalog" and value=="Bisakol":
            pipe = pipeline("text2text-generation", model="dapooni/sorsolingo-mt-tl-bsl")
            translation = pipe(self.ids.translate_input.text)[0]["generated_text"]
            self.ids.translate_output.text = f'{translation}'
        elif input=="Bisakol" and value=="Tagalog":
            pipe = pipeline("text2text-generation", model="dapooni/sorsolingo-mt-bsl-tl")
            translation = pipe(self.ids.translate_input.text)[0]["generated_text"]
            self.ids.translate_output.text = f'{translation}'

    def voice_input(self):
        self.ids.mic_on.icon = "assets/mic.png" if self.ids.mic_on.icon == "assets/stop.png" else "assets/stop.png"
        self.ids.mic_on.pos_hint = {"center_x": 0.98, "center_y": 0.8}

    def voice_output(self):
        # Insert Code
        print("Voice Output: No Function")

    def save_word(self):
        user = App.get_running_app().get_current_user()
        word_to_save = self.translate_input.text.strip()

        if user and word_to_save:
            user = App.get_running_app().get_current_user()
            word_to_save = self.translate_input.text.strip()

            if user and word_to_save:
                conn = sql.connect('profiles.db')
                c = conn.cursor()
                c.execute("INSERT INTO words (user, word) VALUES (?, ?)",
                          (user, word_to_save))
                conn.commit()
                print(f"\nWord '{word_to_save}' saved for user '{user}' in history.")
                conn.close()

class HistoryScreen(Screen):
    def on_enter(self, *args):
        super().on_enter(*args)
        self.load_history()
        self.update_username()

    def load_history(self):
        word_list = self.ids.save_word_lists
        word_list.clear_widgets()
        user = App.get_running_app().get_current_user()

        if user:
            history_items = self.fetch_history_from_database(user)

            for word in history_items:
                item = OneLineListItem(text=word)
                word_list.add_widget(item)

    def fetch_history_from_database(self, user):
        conn = sql.connect('profiles.db')
        cursor = conn.cursor()
        cursor.execute("SELECT word FROM words WHERE user=?", (user,))
        result = cursor.fetchall()
        history_words = [row[0] for row in result]
        conn.close()
        return history_words

    def clear_history(self):
        user = App.get_running_app().get_current_user()
        if user:
            conn = sql.connect('profiles.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM words WHERE user=?", (user,))
            conn.commit()
            conn.close()
            self.load_history()
            print("Cleared history")

    def update_username(self):
        current_user_email = App.get_running_app().get_current_user()
        user_label = self.ids.user_name
        if current_user_email:
            current_user_username = self.fetch_username_from_database(current_user_email)
            user_label.text = current_user_username

    def fetch_username_from_database(self, email):
        conn = sql.connect('profiles.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user FROM profiles WHERE email=?", (email,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]


class Profile(Screen):
    def on_enter(self, *args):
        super().on_enter(*args)
        self.update_username()

    def update_username(self):
        current_user_email = App.get_running_app().get_current_user()
        user_label = self.ids.user_name
        if current_user_email:
            current_user_username = self.fetch_username_from_database(current_user_email)
            user_label.text = current_user_username

    def fetch_username_from_database(self, email):
        conn = sql.connect('profiles.db')
        cursor = conn.cursor()
        cursor.execute("SELECT user FROM profiles WHERE email=?", (email,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]


class EditProfile(Screen):
    # Not Done yet
    def change_profile(self):
        user = self.ids.change_name.text.strip()
        password = self.ids.change_pass.text.strip()
        user1 = App.get_running_app().get_current_user()

        if user1 and user and password:
            conn = sql.connect('profiles.db')
            c = conn.cursor()
            c.execute("UPDATE profiles SET user=?, password=? WHERE user=?",
                      (user, password, user1))
            conn.commit()
            conn.close()

            self.user.text = user
            self.password.text = password

            print(f"\nProfile updated for user '{user}': Name='{user}', Password='{password}'")


class About(Screen):
    pass


class Help(Screen):
    pass


class Logout(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class SorsolingoApp(MDApp):
    current_user_email = None

    def build(self):
        self.icon = "Sorsolingo.png"
        Window.clearcolor = (1, 1, 1, 1)

        # Create the profiles table
        conn = sql.connect('profiles.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists profiles(
            user text,
            email text,
            password text)
        """)

        # Create the history table
        c.execute("""CREATE TABLE if not exists words(
            user TEXT,
            word TEXT,
            FOREIGN KEY(user) REFERENCES profiles(user),
            PRIMARY KEY(user, word))
        """)
        conn.commit()
        conn.close()
        return Builder.load_file('sorsofile.kv')

    def set_current_user(self, email):
        self.current_user = email

    def get_current_user(self):
        return self.current_user

if __name__ == "__main__":
    SorsolingoApp().run()