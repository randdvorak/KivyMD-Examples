import functools
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty


class AutoCompleteField(TextInput):

    collected_text = StringProperty()
    text_completions = ObjectProperty()
    current_completion = StringProperty()
    reduce_func = None

    def __init__(self, completions=None, search_func=None, **kwargs):
        sorted_completions = sorted(completions)
        sorted_completions.reverse()
        self.text_completions = sorted_completions + ['***END***']
        self.reduce_func = search_func
        super(AutoCompleteField, self).__init__(**kwargs)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == 'backspace':
            self.collected_text = self.collected_text[:-1]
        if text:
            self.collected_text += text
        completion = self.get_completion_for_substring(self.collected_text)
        if completion:
            self.text = completion
            self.current_completion = completion
        else:
            self.text = self.collected_text
            self.current_completion = ''
        return True

    def insert_text(self, substring, from_undo=False):
        pass            

    def get_completion_for_substring(self, search_string):
        completion = functools.reduce(self.reduce_func, self.text_completions)
        return completion if completion != '***END***' else None