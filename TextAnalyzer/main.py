from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.relativelayout import RelativeLayout
from textblob import TextBlob

Window.size = (480, 800)

class MainInterface(RelativeLayout):
    def clear(self):
        self.ids.input.text = ''
        self.ids.no_words.text = '0'
        self.ids.no_sentences.text = '0'
        self.ids.polarity.text = '0.0%'
        self.ids.sentiment.text = '0.0%'


    def submit(self):
        blob = TextBlob(self.ids.input.text)
        self.ids.no_words.text = str(len(blob.words))
        self.ids.no_sentences.text = str(len(blob.sentences))
        pol, sent = blob.sentiment
        self.ids.polarity.text = '{:.1f}%'.format(pol*100)
        self.ids.sentiment.text = '{:.1f}%'.format(sent*100)

class TextAnalyzerApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.theme_style = 'Dark'
        return 0

if __name__ == '__main__':
    TextAnalyzerApp().run()