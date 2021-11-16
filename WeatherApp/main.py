from ast import Str
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextFieldRect
from kivy.core.window import Window
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty

from bs4 import BeautifulSoup
import requests
import functools



class HomeScreen(MDScreen):

    city_name = StringProperty()
    temperature = StringProperty()
    condition = StringProperty()
    datetime = StringProperty()
    visibility = StringProperty()
    pressure = StringProperty()
    humidity = StringProperty()

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def get_city_data(self, city_link):
        link_data = city_link.split('/')
        city = link_data[-1].capitalize()
        country = link_data[-2].capitalize()
        self.city_name = city + ', ' + country
        data = requests.get(city_link)
        soup = BeautifulSoup(data.text, 'html.parser')
        qlook = soup.find(id='qlook')
        self.temperature = qlook.find(class_='h2').get_text()
        self.condition = qlook.find('p').get_text()
        table = soup.find(class_='bk-focus__info')
        tds = table.find_all('td')
        self.datetime = tds[1].get_text()
        self.visibility = tds[3].get_text()
        self.pressure = tds[4].get_text()
        self.humidity = tds[5].get_text()

class CitySearchField(MDTextFieldRect):
   
    collected_text = StringProperty()
    city_links = ObjectProperty()
    city_names = ObjectProperty()
    current_city_link = StringProperty()

    def __init__(self, **kwargs):
        data = requests.get('https://www.timeanddate.com/weather/')
        soup = BeautifulSoup(data.text, 'html.parser')
        table = soup.find(class_='tb-scroll')
        links = table.find_all('a')
        self.city_links = {}
        for a in links:
            self.city_links.update({a.get_text():'https://www.timeanddate.com' + a['href']})
        names = sorted(self.city_links.keys())
        names.reverse()
        self.city_names = names + ['***END***']
        super(CitySearchField, self).__init__(**kwargs)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == 'backspace':
            self.collected_text = self.collected_text[:-1]
        if text:
            self.collected_text += text
        city = self.get_city_for_string(self.collected_text)
        if city:
            self.text = city
            self.current_city_link = self.city_links[city]
        else:
            self.current_city_link = ''
            self.text = self.collected_text
        return True

    def insert_text(self, substring, from_undo=False):
        pass            
    
    def get_city_for_string(self, cstr):
        city = functools.reduce(lambda a, b: a if a.lower().startswith(cstr.lower()) and not b.lower().startswith(cstr.lower()) else b, self.city_names)
        return city if city != '***END***' else None


class MainApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__()
        Window.size = (320, 640)
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_hue = 'A700'

if __name__ == '__main__':
    MainApp().run()