from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivymd.app import MDApp
from kivymd.uix.floatlayout import FloatLayout
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDIcon
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from plyer import filechooser

import pyttsx3

Window.size = (480, 720)
engine = pyttsx3.init(debug=True)

def onStart(name):
   print('starting ' + name)

def onEnd(name, completed):
    print('ending ' + name)
    if completed:
       engine.endLoop()

def onWord(name, location, length):
   print('word ' + name + ' ' + str(location) + ' ' + str(length))

def onError(name, exc):
    print('error ' + exc)

def playOutput(input, voice):
    engine.setProperty('voice', voice)
    engine.say(input, 'output')
    engine.startLoop()

engine.connect('started-utterance', onStart)
engine.connect('started-word', onWord)
engine.connect('finished-utterance', onEnd)
engine.connect('error', onError)


class PlayButton(ButtonBehavior, MDIcon):
    pass

class Filechooser(BoxLayout):
    pass 

class Interface(FloatLayout):

    def changeState(self):
        if self.ids.play_button.icon == 'Play.png':
            self.ids.play_button.icon = 'Pause.png'
            voices = engine.getProperty('voices')
            if self.ids.male.active:
                voice = voices[0].id
            else:
                voice = voices[1].id
            # proc = threading.Thread(target=playOutput, args=(self.ids.input_text.text, voice))
            # proc.start()
            playOutput(self.ids.input_text.text, voice)

        else:
            self.ids.play_button.icon = 'Play.png'
        
    def export_to_file(self):
        self.dialog = MDDialog(
            size_hint=(.8, None),
            title='Filename',
            type='custom',
            content_cls=Filechooser(),
            buttons=[MDRaisedButton(text='Export', on_release=self.selectFile)]
        )
        self.dialog.open()
    
    def export(self, location):
        print(location[0])
        objs = self.dialog.content_cls.children
        print(objs[0].text)

    def selectFile(self, instances):
        filechooser.choose_dir()

class Text2SpeechApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Pink'
        self.theme_cls.theme_style = 'Light'
        return 0

if __name__ == '__main__':
    Text2SpeechApp().run()
