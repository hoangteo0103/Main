from kivymd.uix.textfield import MDTextField
from rarCracker import *
from kivymd.uix.button import MDRectangleFlatIconButton, MDRoundFlatIconButton


class CustomTextBruteField(MDTextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CustomLocalDictTextField(MDTextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CustomNetworkDictTextField(MDTextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CustomFileButton(MDRectangleFlatIconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
class CustomActionButton(MDRoundFlatIconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)