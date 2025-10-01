from kivymd.app import MDApp
from kivymd.uix.boxlayout import BoxLayout



class SelfieCameraApp(MDApp):
    pass

class SelfieCamera(BoxLayout):
    def take_photo(self):
        self.ids.camera.export_to_png('./selfie.png')

if __name__ == '__main__':
    SelfieCameraApp().run()