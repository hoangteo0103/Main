from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.toast import toast
from rarCracker import *
from kivymd.uix.list import OneLineListItem
import tkinter
import os
import tkinter.filedialog
from components import *
from thread import *
from base_screen import BaseScreen

Builder.load_string('''
                    
<CustomLocalDictTextField>
    color_mode: 'custom'
    line_color_focus: "white"
    line_color_normal: "white"
    mode: "fill"
    size_hint_x: .6
    fill_color_normal: "white"
                    
<CustomFileButton>
    text_color: "white"
    icon_color: "white"
    font_style: "H6"
    md_bg_color: "#39A7FF"
                    
<CustomActionButton>
    text_color: "white"
    icon_color: "white"
    pos_hint: {"center_x": 1.5, "center_y": 1.5}
                    
<LocalDictionaryScreen>:
    md_bg_color: "#EEEEEE"
    MDFloatLayout:
        MDLabel:
            pos_hint: {"center_x": 0.55, "center_y": 0.95}
            text: "Local Dictionary Attack"
            halign: "left"
            theme_text_color: "Custom"
            text_color: "#FF5F00"
            font_style: "H5"
        
        CustomLocalDictTextField:
            id: text_field_worker
            hint_text: "Number of threads"
            max_text_length: 2
            text: "2"
            pos_hint: {"center_x": 0.5, "center_y": 0.85}
                
        CustomFileButton:
            icon: "file"
            id: rar_file_button
            size_hint_x: .6
            text: "Choose RAR file to crack"
            pos_hint: {"center_x": 0.5, "center_y": 0.75}
            on_release: root.prompt_file_rar()
                    
        CustomFileButton:
            icon: "file"
            size_hint_x: .6
            id: dictionary_file_button
            text: "Choose Local Dictionary file to crack"
            pos_hint: {"center_x": 0.5, "center_y": 0.65}
            on_release: root.prompt_file_dictionary()
        
        CustomActionButton:
            id: start_button
            icon: "play"
            text: "Start"
            md_bg_color: "#FF204E"
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            on_release: root.start()                    
        
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
                    
        MDRectangleFlatButton:
            pos_hint: {"center_x": 0.5, "center_y": 0.3}
            size_hint_x: .5
            size_hint_y: 0
            id: log_label_1
            theme_text_color: "Custom"
            padding: "10dp"
            spacing: "10dp"
            line_color: "#E1F7F5"

''')

class LocalDictionaryScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_name = ""
        self.log = ""
        self.thread = None
        self.found_password = False
        self.dictionary_file_name = ""
        self.running = False
        self.loc_y = 0.45
    
    def prompt_file_rar(self):
        top = tkinter.Tk()
        top.withdraw()
        file_name = tkinter.filedialog.askopenfilename(parent=top, title="Select a file", filetypes=[("RAR files", "*.rar")])
        if file_name:
            self.file_name = file_name
            self.ids.rar_file_button.text = os.path.basename(file_name)
            self.ids.log_label_1.text = "Please wait"
            self.ids.log_label_1.pos_hint = {"center_x": 1.5, "center_y": 1.5}
            self.ids.log_label_1.md_bg_color = "#E1F7F5"
            self.log = ""
            self.found_password = False
        top.destroy()
    
    def prompt_file_dictionary(self):
        top = tkinter.Tk()
        top.withdraw()
        dictionary_file_name = tkinter.filedialog.askopenfilename(parent=top, title="Select a file", filetypes=[("TXT files", "*.txt")])
        if dictionary_file_name:
            self.dictionary_file_name = dictionary_file_name
            self.ids.dictionary_file_button.text = os.path.basename(dictionary_file_name)
            self.log = ""
            self.found_password = False
        top.destroy()
    
    def start(self, resume=False):
        if resume == False:
            self.reset_breakpoint()
        num_worker = self.ids.text_field_worker.text

        if not self.file_name:
            toast("Please select a file")
            return
        
        if not self.dictionary_file_name:
            toast("Please select a dictionary file")
            return

        self.thread = thread_with_trace(target=self.run_cracker, args=(num_worker))
        self.thread.daemon = True
        self.thread.start()

    def update_list(self, dt):
            if self.log == "File don't have password":
                self.hide_button(0)
                self.ids.log_label_1.text = self.log
                self.ids.log_label_1.text_color = "white"
                self.ids.log_label_1.md_bg_color = "#41B06E"
                toast(self.log)
                return 
            if 'password found' in self.log:
                self.hide_button(0)
                # self.reset_breakpoint()
                self.ids.log_label_1.text = self.log
                self.ids.log_label_1.text_color = "white"
                self.ids.log_label_1.md_bg_color = "#41B06E"
                toast(self.log)
            else:
                self.ids.log_label_1.text = self.log
                self.ids.log_label_1.text_color = "white"
                self.ids.log_label_1.md_bg_color = "#EE4E4E"



    def callback(self, log):
        if self.found_password:
            return
        
        self.log = log
        if 'password found' in log:
            self.found_password = True
        Clock.schedule_once(self.update_list, 0)
    
    def run_cracker(self, num_worker):
        self.running = True
        Clock.schedule_once(self.show_button, 0)
        self.ids.log_label_1.pos_hint = {"center_x": 0.5, "center_y": 0.3}
        cracker = RarCracker(self.file_name, workers=int(num_worker), provider=LocalProvider(self.dictionary_file_name), break_point=LocalBreakPoint(breakpoint_path="breakpoint/dictionary_breakpoint.txt", breakpoint_count=1))
        cracker.crack(self.callback)
 
    def on_close(self):
        self.reset_breakpoint()                                                                                                                                                                                                   
        if self.thread:
            self.thread.join()
    
    def reset_breakpoint(self):
        with open("breakpoint/dictionary_breakpoint.txt", "w") as f:
            f.write("0")
            

class DictionaryApp(MDApp):


    def build(self):
        return LocalDictionaryScreen()

if __name__ == "__main__":
    DictionaryApp().run()