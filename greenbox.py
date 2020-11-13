from kivymd.app import MDApp

from kivy.lang import Builder
from kivymd.uix.screen import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout





Window.size = (300,500)

navigation_helper = '''

<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"
        
    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None

        Image:
            size: "18dp", "18dp"
            source: "ua_logo.jpg"

    ScrollView:

        MDList:
            OneLineListItem:
                text: "Sensor Data"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "sensorscreen"

            OneLineListItem:
                text: "Cameras"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "webcamscreen"

            OneLineListItem:
                text: "Lighting"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "lightingscreen"

            OneLineListItem:
                text: "Pumps"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "pumpscreen"
            
            OneLineListItem:
                text: "Board Control"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "boardscreen"

Screen:

    MDToolbar:
        id: toolbar
        pos_hint: {"top": 1}
        elevation: 10
        title: "V-Hive Green Box"
        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

    NavigationLayout:
        x: toolbar.height

        ScreenManager:
            id: screen_manager

            Screen:
                name: "sensorscreen"

                MDLabel:
                    text: "Sensor Data:"
                    halign: "center"
                    font_style: "H6"

                MDLabel:
                    text: "Temperature (F):"
                    pos_hint: {"top": .9}
                    font_style: "Caption"
                MDLabel:
                    text: "RH (%):"
                    pos_hint: {"top": .85}
                    font_style: "Caption"
                MDLabel:
                    text: "CO2 (ppm):"
                    pos_hint: {"top": .8}
                    font_style: "Caption"    
         
            Screen:
                name: "webcamscreen"

                MDCard:
                    orientation: "vertical"
                    size_hint: None,None
                    size: "160dp", "160dp"
                    pos_hint: {"center_x": .5, "center_y": .2}
                    elevation: 12
                    Image:
                        source: "seedlings.jpg"
                        size_hint_y: .8
                        allow_stretch: True
                        keep_ratio: True
                    MDLabel:
                        text: "seedling view"
                        halign: "center"
                        size_hint_y: .2

                MDCard:
                    orientation: "vertical"
                    size_hint: None,None
                    size: "160dp", "160dp"
                    pos_hint: {"center_x": .5, "center_y": .6}
                    elevation: 12
                    Image:
                        source: "bare bones.jpg"
                        size_hint_y: .8
                        allow_stretch: True
                        keep_ratio: True
                    MDLabel:
                        text: "v-hive view"
                        halign: "center"
                        size_hint_y: .2

            Screen:
                name: "lightingscreen"

                MDLabel:
                    text: "Lighting"
                    halign: "center"

            Screen:
                name: "pumpscreen"

                MDLabel:
                    text: "Pump Control"
                    halign: "center"

            Screen:
                name: "boardscreen"

                MDLabel:
                    text: "Board Control"
                    halign: "center"
            

        MDNavigationDrawer:
            id: nav_drawer

            ContentNavigationDrawer:
                screen_manager: screen_manager
                nav_drawer: nav_drawer  
   
             
'''

class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()

class DemoApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Lime"
        self.theme_cls.theme_style = "Light"
        screen = Builder.load_string(navigation_helper)
        return screen

    #def navigation_draw(self):
     #   print("Naviagation")

DemoApp().run()
