# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.uix.screenmanager import Screen

from kivy.lang import Builder
from kivy.properties import ListProperty, BooleanProperty, StringProperty
from kivy.uix.label import Label
from kivy.logger import Logger as log

from kivymd.list import ILeftBodyTouch, TwoLineIconListItem
from kivymd.button import MDIconButton
from kivymd.dialog import MDDialog
from kivymd.textfields import MDTextField

# Helper methods
from utils.urlref import add_refs

# Components
from components.buttons import MDScrollableTextButton

Builder.load_file("kv/screens/textscreen.kv")


class TextScreen(Screen):
    text_lines = ListProperty([])
    file_text = StringProperty("")

    def on_enter(self):
        self.file_text = ""
        self.ids.label_list.clear_widgets()
        log.info("Text Lines: {}".format(len(self.text_lines)))
        i = 0
        for line in self.text_lines:
            i+= 1
            try:
                encoded_line = line.decode("latin-1")
                prepared_text = add_refs(encoded_line)+"\n"
                self.file_text += prepared_text
                if i % 50 == 0:
                    text_label = MDScrollableTextButton(text=self.file_text)
                    self.ids.label_list.add_widget(text_label)
                    self.file_text = ""
            except UnicodeDecodeError as e:
                log.info(line)
                log.exception(e)
        text_label = MDScrollableTextButton(text=self.file_text)
        self.ids.label_list.add_widget(text_label)
        self.file_text = ""
