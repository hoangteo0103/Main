from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRoundFlatIconButton
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.toast import toast
import os
import tkinter
import tkinter.filedialog
import threading
from rarCracker.main import RarCracker
from kivymd.uix.list import OneLineListItem

Builder.load_string('''
<HomeScreen>:
    MDFloatLayout:
        MDLabel:
            pos_hint: {"center_x": 0.5, "center_y": 0.95}
            text: "Rar Cracker"
            halign: "center"
            theme_text_color: "Custom"
            text_color: 0, 0, 1, 1
            font_style: "H3"
''')

class HomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_name = ""
        self.log = ""
        self.thread = None
        self.found_password = False

    def on_close(self):
        if self.thread:
            self.thread.join()

class HomeApp(MDApp):
    def build(self):
        return HomeScreen()

if __name__ == "__main__":
    HomeApp().run()
