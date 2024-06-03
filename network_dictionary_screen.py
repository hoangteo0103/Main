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
                    
<CustomNetworkDictTextField>
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
                    
<NetworkDictionaryScreen>:
    md_bg_color: "#EEEEEE"
    MDFloatLayout:
        MDLabel:
            pos_hint: {"center_x": 0.55, "center_y": 0.95}
            text: "Network Dictionary Attack"
            halign: "left"
            theme_text_color: "Custom"
            text_color: "#FF5F00"
            font_style: "H5"
        
        CustomNetworkDictTextField:
            id: text_field_worker
            hint_text: "Number of threads"
            max_text_length: 2
            text: "2"
            pos_hint: {"center_x": 0.5, "center_y": 0.85}
        
        CustomNetworkDictTextField:
            id: text_field_url
            hint_text: "URL of Remote Dictionary file"
            max_text_length: 250
            text: "http://example.com/dict.txt"
            pos_hint: {"center_x": 0.5, "center_y": 0.75}
                
        CustomFileButton:
            icon: "file"
            id: rar_file_button
            size_hint_x: .6
            text: "Choose RAR file to crack"
            pos_hint: {"center_x": 0.5, "center_y": 0.65}
            on_release: root.prompt_file_rar()

        
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
                    
        MDList:
            pos_hint: {"center_x": 0.5, "center_y": 0.3}
            size_hint_x: .8
            size_hint_y: 0
            id: container
            padding: "10dp"
            spacing: "10dp"

''')

class NetworkDictionaryScreen(BaseScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_name = "test.rar"
        self.log = ""
        self.thread = None
        self.found_password = False
        self.dictionary_file_name = "https://hanerx.top/rarCracker/dict.json"
        self.running = False
        self.loc_y = 0.45
    
    def prompt_file_rar(self):
        top = tkinter.Tk()
        top.withdraw()
        file_name = tkinter.filedialog.askopenfilename(parent=top, title="Select a file", filetypes=[("RAR files", "*.rar")])
        if file_name:
            self.file_name = file_name
            self.ids.rar_file_button.text = os.path.basename(file_name)
            self.ids.container.clear_widgets()
            self.log = ""
            self.found_password = False
        top.destroy()
    
    def start(self):
        num_worker = self.ids.text_field_worker.text
        self.ids.container.size_hint_y = .3

        if not self.file_name:
            toast("Please select a file")
            return
        
        if not self.dictionary_file_name:
            toast("Please input a remote dictionary file URL")
            return

        self.thread = thread_with_trace(target=self.run_cracker, args=(num_worker))
        self.thread.daemon = True
        self.thread.start()

    def update_list(self, dt):
        if len(self.ids.container.children) >= 3:
            self.ids.container.clear_widgets()
        if 'password found' in self.log:
            self.hide_button(0)
            self.ids.container.clear_widgets()
            self.ids.container.add_widget(OneLineListItem(text=self.log, theme_text_color="Custom", text_color="white", bg_color="#74E291"))
            toast(self.log)
        else:
            self.ids.container.add_widget(OneLineListItem(text=self.log, theme_text_color="Custom", text_color="white", bg_color="#EE4E4E"))


    def callback(self, log):
        if self.found_password:
            return
        
        self.log = log
        if 'password found' in log:
            with open("breakpoint/dictionary_breakpoint.txt", "w") as f:
                f.write("0")
            self.found_password = True
        Clock.schedule_once(self.update_list, 0)
    
    def run_cracker(self, num_worker):
        self.running = True
        Clock.schedule_once(self.show_button, 0)
        cracker = RarCracker(self.file_name, workers=int(num_worker), provider=NetworkProvider(self.dictionary_file_name,
                                                                method=NetworkProvider.GET), break_point=LocalBreakPoint(breakpoint_path="breakpoint/network_dictionary_breakpoint.txt", breakpoint_count=1))
        cracker.crack(self.callback)
 
    def on_close(self):
        self.reset_breakpoint()                                                                                                                                                                                                   
        if self.thread:
            self.thread.join()
    
    def reset_breakpoint(self):
        with open("breakpoint/network_dictionary_breakpoint.txt", "w") as f:
            f.write("0")
            

class DictionaryApp(MDApp):


    def build(self):
        return NetworkDictionaryScreen()

if __name__ == "__main__":
    DictionaryApp().run()
