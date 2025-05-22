from kivy.lang import Builder
from kivymd.app import MDApp

KV = '''
BoxLayout:
    orientation: 'vertical'
    MDRaisedButton:
        text: "Hola Mundo"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
'''

class TestApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

TestApp().run()


  