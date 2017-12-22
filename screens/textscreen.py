from kivy.app import App
from kivy.uix.screenmanager import Screen

from kivy.lang import Builder
from kivy.properties import ListProperty, BooleanProperty, StringProperty
from kivy.logger import Logger as log

from kivymd.list import ILeftBodyTouch, TwoLineIconListItem
from kivymd.button import MDIconButton
from kivymd.dialog import MDDialog
from kivymd.textfields import MDTextField

# Helper methods
from utils.urlref import add_refs

Builder.load_file("kv/screens/textscreen.kv")


class TextScreen(Screen):
    text_lines = ListProperty([])
    file_text = StringProperty("")

    def on_enter(self):
        log.info("Text Lines: {}".format(len(self.text_lines)))
        for line in self.text_lines:
            self.file_text += add_refs(line)+"\n"


