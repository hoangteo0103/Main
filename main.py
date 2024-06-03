from kivy.clock import Clock
from kivy.lang import Builder

from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.button import MDFillRoundFlatIconButton
from bruteforce_screen import BruteForceScreen
from local_dictionary_screen import LocalDictionaryScreen
from home_screen import HomeScreen
KV = '''
#:import FadeTransition kivy.uix.screenmanager.FadeTransition


<ExtendedButton>
    elevation: 3.5
    shadow_radius: 12
    shadow_softness: 4
    -height: "56dp"


<DrawerClickableItem@MDNavigationDrawerItem>
    focus_color: "#e7e4c0"
    unfocus_color: "#fffcf4"
MDScreen:

    MDNavigationLayout:

        ScreenManager:

            MDScreen:

                MDBoxLayout:
                    orientation: "vertical"
                    MDBoxLayout:
                        adaptive_height: True
                        md_bg_color: "white"
                        padding: "12dp"

                        MDLabel:
                            text: "Rar Cracker"
                            adaptive_height: True
                            pos_hint: {"center_y": .5}
                            theme_text_color: "Custom"
                            font_style: "H4"

                    MDBoxLayout:

                        MDNavigationRail:
                            id: navigation_rail
                            md_bg_color: "white"
                            selected_color_background: "#FFF7FC"
                            ripple_color_item: "#FFF7FC"
                            on_item_release: app.switch_screen(*args)

                            MDNavigationRailItem:
                                text: "Home"
                                icon: "home"
                            MDNavigationRailItem:
                                text: "Bruteforce"
                                icon: "lock"

                            MDNavigationRailItem:
                                text: "Dictionary"
                                icon: "book"

                            MDNavigationRailItem:
                                text: "Settings"
                                icon: "cog"

                        ScreenManager:
                            id: screen_manager
                            transition:
                                FadeTransition(duration=.2, clearcolor=app.theme_cls.bg_dark)

    
'''


class ExtendedButton(MDFillRoundFlatIconButton, CommonElevationBehavior):
    '''
    Implements a button of type
    `Extended FAB <https://m3.material.io/components/extended-fab/overview>`_.

    .. rubric::
        Extended FABs help people take primary actions.
        They're wider than FABs to accommodate a text label and larger target
        area.

    This type of buttons is not yet implemented in the standard widget set
    of the KivyMD library, so we will implement it ourselves in this class.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.padding = "16dp"
        Clock.schedule_once(self.set_spacing)

    def set_spacing(self, interval):
        self.ids.box.spacing = "12dp"

    def set_radius(self, *args):
        pass
        # if self.rounded_button:
        #     self._radius = self.radius = self.height / 4


class MainApp(MDApp):
    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def switch_screen(
        self, instance_navigation_rail, instance_navigation_rail_item
    ):
        '''
        Called when tapping on rail menu items. Switches application screens.
        '''

        self.root.ids.screen_manager.current = (
            instance_navigation_rail_item.text.lower()
        )

    def on_start(self):
        '''Creates application screens.'''

        navigation_rail_items = self.root.ids.navigation_rail.get_items()[:]
        navigation_rail_items.reverse()

        self.root.ids.screen_manager.add_widget(HomeScreen(name="home"))
        self.root.ids.screen_manager.add_widget(BruteForceScreen(name="bruteforce"))
        self.root.ids.screen_manager.add_widget(LocalDictionaryScreen(name="dictionary"))
 

MainApp().run()