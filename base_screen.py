from kivy.uix.screenmanager import Screen as MDScreen
from thread import *

class BaseScreen(MDScreen):
    def show_button(self, dt):  
        self.ids.pause_resume_button.text = "Pause"
        self.ids.pause_resume_button.icon = "pause"
        self.ids.pause_resume_button.md_bg_color = "#FF204E"
        self.running = True
        self.ids.start_button.pos_hint = {"center_x": 1.5, "center_y": 1.5}
        self.ids.pause_resume_button.pos_hint = {"center_x": 0.4, "center_y": self.loc_y + 0.05}
        self.ids.stop_button.pos_hint = {"center_x": 0.6, "center_y": self.loc_y + 0.05}


    def hide_button(self, dt):
        self.ids.start_button.pos_hint = {"center_x": 0.5, "center_y": self.loc_y + 0.05}
        self.ids.pause_resume_button.pos_hint = {"center_x": 1.5, "center_y": 1.5}
        self.ids.stop_button.pos_hint = {"center_x": 1.5, "center_y": 1.5}

    def pause_resume(self):
        if self.running:
            self.pause()
        else:
            self.resume()

    def pause(self):
        self.ids.pause_resume_button.text = "Resume"
        self.ids.pause_resume_button.icon = "play"
        self.ids.pause_resume_button.md_bg_color = "#00C853"

        if self.thread:
            self.running = False
            self.thread.kill()
    
    def resume(self):
        self.ids.pause_resume_button.text = "Pause"
        self.ids.pause_resume_button.icon = "pause"
        self.ids.pause_resume_button.md_bg_color = "#FF204E"
        self.running = True
        self.start(resume=True)



    def stop(self):
        self.running = False
        self.thread.kill()
        self.ids.log_label.text = ""
        self.hide_button(0)
        self.reset_breakpoint()

    def on_close(self):
        self.reset_breakpoint()
        if self.thread:
            self.thread.join()