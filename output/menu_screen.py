from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


Builder.load_string('''
<MenuScreen>:
    MDLabel:
        pos_hint: {"center_x": 0.5, "center_y": 0.9}
        text: "Rar Cracker"
        halign: "center"
        text_color: 0, 0, 1, 1
        font_style: "H2"
            
    MDRectangleFlatButton:
        text: "Brite Force Attack"
        font_size: "20sp"
        size_hint: 0.1, 0.1
        pos_hint: {"center_x": 0.5, "center_y": 0.75}
        on_press: root.manager.current = 'bruteforce'
                    
    
    MDRectangleFlatButton:
        text: "Dictionary Attack"
        font_size: "20sp"
        size_hint: 0.1, 0.1
        pos_hint: {"center_x": 0.5, "center_y": 0.5}

    MDRectangleFlatButton:
        text: "Quit"
        font_size: "20sp"
        size_hint: 0.1, 0.1
        pos_hint: {"center_x": 0.5, "center_y": 0.25}
''')


class MenuScreen(MDScreen):
    pass