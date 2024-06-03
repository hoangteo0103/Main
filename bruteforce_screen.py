from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.toast import toast
import os
import tkinter
import tkinter.filedialog
from thread import *
from rarCracker.main import RarCracker
from kivymd.uix.list import OneLineListItem
from components import *
from base_screen import BaseScreen

Builder.load_string('''
                    
<CustomTextBruteField>
    color_mode: 'custom'
    line_color_focus: "white"
    line_color_normal: "white"
    mode: "fill"
    size_hint_x: .4
    size_hint_y: .1
    font_style: "H6"
    fill_color_normal: "white"

<CustomFileButton>
    text_color: "white"
    icon_color: "white"
    md_bg_color: "#39A7FF"
                    
<CustomActionButton>
    text_color: "white"
    icon_color: "white"
    pos_hint: {"center_x": 1.5, "center_y": 1.5}
                    
<BruteForceScreen>:
    md_bg_color: "#E1F7F5"
    MDFloatLayout:
        MDLabel:
            pos_hint: {"center_x": 0.55, "center_y": 0.95}
            text: "Brute Force Attack"
            halign: "left"
            theme_text_color: "Custom"
            text_color: "#FF5F00"
            font_style: "H5"
                
        CustomTextBruteField:
            id: text_field_worker
            hint_text: "Number of threads"
            max_text_length: 2
            text: "2"
            pos_hint: {"center_x": 0.25, "center_y": 0.85}
                    
        CustomTextBruteField:
            id: text_field_charset
            hint_text: "Charset"
            max_text_length: 250
            text: "abcdefghijklmnopqrstuvwxyz"
            pos_hint: {"center_x": 0.7, "center_y": 0.85}
            

        CustomTextBruteField:
            id: text_field_minimum_char
            hint_text: "Minimum characters"
            max_text_length: 2
            text: "1"
            pos_hint: {"center_x": 0.25, "center_y": 0.65}
        
        CustomTextBruteField:
            id: text_field_maximum_char
            hint_text: "Maximum characters"
            text: "2"
            max_text_length: 3
            pos_hint: {"center_x": 0.7, "center_y": 0.65}
                            
        CustomFileButton:
            icon: "file"
            id: file_button
            text: "Choose RAR file to crack"
            pos_hint: {"center_x": 0.5, "center_y": 0.55}
            on_release: root.prompt_file()       
        
        CustomActionButton:
            id: pause_resume_button
            text: "Pause"
            md_bg_color: "#FF204E"
            icon: "pause"
            on_release: root.pause_resume()
        
        CustomActionButton:
            id: stop_button
            text: "Stop"
            md_bg_color: "#FF204E"
            icon: "stop"
            on_release: root.stop()
        
        CustomActionButton:
            id: start_button
            icon: "play"
            text: "Start"
            md_bg_color: "#FF204E"
            pos_hint: {"center_x": 0.5, "center_y": 0.45}
            on_release: root.start()             

        
        MDList:
            pos_hint: {"center_x": 0.5, "center_y": 0.4}
            size_hint_x: .8
            size_hint_y: 0
            id: container
            padding: "10dp"
            spacing: "10dp"
''')


class BruteForceScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_name = ""
        self.loc_y = 0.25
        self.log = ""
        self.thread = None
        self.found_password = False
        self.loc_y = 0.4

    def prompt_file(self):
        top = tkinter.Tk()
        top.withdraw()
        file_name = tkinter.filedialog.askopenfilename(parent=top, title="Select a file", filetypes=[("RAR files", "*.rar")])
        if file_name:
            self.file_name = file_name
            self.ids.file_button.text = os.path.basename(file_name)
            self.ids.container.clear_widgets()
            self.log = ""
            self.found_password = False
            self.hide_button(0)
        top.destroy()

    def start(self):
        self.reset_breakpoint()
        num_worker = self.ids.text_field_worker.text
        charset = self.ids.text_field_charset.text
        min_char = self.ids.text_field_minimum_char.text
        max_char = self.ids.text_field_maximum_char.text
        

        if not self.file_name:
            toast("Please select a file")
            return

        self.thread = thread_with_trace(target=self.run_cracker, args=(num_worker, charset, min_char, max_char))
        self.thread.daemon = True
        self.thread.start()

    def update_list(self, dt):
        if len(self.ids.container.children) >= 2:
            self.ids.container.clear_widgets()
        if 'password found' in self.log:
            self.hide_button(0)
            self.ids.container.clear_widgets()
            self.reset_breakpoint()
            self.ids.container.add_widget(OneLineListItem(text=self.log, theme_text_color="Custom", text_color="white", bg_color="#74E291"))
            toast(self.log)
        else:
            self.ids.container.add_widget(OneLineListItem(text=self.log, theme_text_color="Custom", text_color="white", bg_color="#EE4E4E"))

    def callback(self, log):
        if self.found_password:
            return
        
        self.log = log
        if 'password found' in log:
            self.found_password = True
        Clock.schedule_once(self.update_list, 0)

    def run_cracker(self, num_worker, charset, min_char, max_char):
        self.running = True
        Clock.schedule_once(self.show_button, 0)
        cracker = RarCracker(self.file_name, start=int(min_char), workers=int(num_worker), stop=int(max_char), charset=charset, break_point=LocalBreakPoint("breakpoint/bruteforce_breakpoint.txt"))
        cracker.crack(self.callback)

    def on_close(self):
        if self.thread:
            self.thread.join()
    
    def reset_breakpoint(self):
        with open("breakpoint/bruteforce_breakpoint.txt", "w") as f:
            f.write("0")

class BruteForceApp(MDApp):
    def build(self):
        return BruteForceScreen()

if __name__ == "__main__":
    BruteForceApp().run()
