from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen


Builder.load_string('''
<MenuScreen>:
    md_bg_color: 0, 0, 0, 1
    FitImage:
        source: "assets/background.jpg"
    MDLabel:
        pos_hint: {"center_x": 0.5, "center_y": 0.9}
        text: "Rar Cracker"
        halign: "center"
        text_color: 0, 0, 1, 1
        font_style: "H2"
            
    MDRectangleFlatIconButton:
        text: "Brute Force Attack"
        icon: "lock"
        theme_text_color: "Custom"
        text_color: "#3AA6B9"
        pos_hint: {"center_x": 0.5, "center_y": 0.75}
        on_press: root.manager.current = 'bruteforce'
        style: "raised"
        font_size: "20sp"
        md_bg_color: "#3AA6B9"
        size_hint: 0.1, 0.1
        line_width: 1    
    
    MDRectangleFlatIconButton:
        icon: "file"
        text: "Dictionary Attack"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        font_size: "20sp"
        md_bg_color: 0, 1, 0, 1
        size_hint: 0.1, 0.1
        line_width: 1 

    MDRectangleFlatIconButton:
        text: "Quit"
        icon: "exit-to-app"
        pos_hint: {"center_x": 0.5, "center_y": 0.25}
        
        font_size: "20sp"
        md_bg_color: 0, 1, 0, 1
        size_hint: 0.1, 0.1
        line_width: 1      
        shadow_radius: 0,1,0,1

''')


class MenuScreen(MDScreen):
    pass

class BruteForceApp(MDApp):
    def build(self):
        return MenuScreen()

if __name__ == "__main__":
    BruteForceApp().run()