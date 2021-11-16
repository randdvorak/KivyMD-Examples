import functools

from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty, NumericProperty


class HomeScreen(MDScreen):
    gender = StringProperty(defaultvalue='MALE')
    heightval = NumericProperty()
    weightval = NumericProperty()
    bmival = NumericProperty()
    bmiclass = StringProperty()
    mclasses = {0:'Skinny boy', 18.6:'Healthy lad', 25:'Dad bod', 30:'Whoa! dude'}
    fclasses = {0:'Skinny chick', 18.6:'Healthy lass', 25:'Mom bod', 30:'Whoa! girl'}
    
    def setGender(self, morf):
        self.gender = morf
    
    def on_heightval(self, instance, value):
        self.calcBMI()

    def on_gender(self, instance, value):
        genderChanged = self.gender == value
        if genderChanged and self.bmival != 0:
            self.calcBMI()

    def on_weightval(self, instance, value):
        self.calcBMI()

    def calcBMI(self):
        if self.heightval != 0 and self.weightval !=0:
            self.bmival = (self.weightval / self.heightval**2) * 703
            self.classes = self.mclasses if self.gender == 'MALE' else self.fclasses
            self.bmiclass = self.classes[functools.reduce(lambda a, b: a if self.bmival >= a and self.bmival < b else b, self.classes.keys())]

class MainApp(MDApp):
    def __init__(self):
        super().__init__()
        Window.size = (320, 640)
        self.theme_cls.primary_palette = 'Red'
        self.theme_cls.primary_hue = 'A700'
        self.theme_cls.theme_style = 'Light'

if __name__ == '__main__':
    MainApp().run()