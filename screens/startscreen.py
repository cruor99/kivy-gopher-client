from kivy.app import App
from kivy.uix.screenmanager import Screen

from kivy.lang import Builder
from kivy.properties import ListProperty, BooleanProperty, StringProperty
from kivy.logger import Logger as log
from kivy.metrics import dp
from kivy.uix.recycleview import RecycleView
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock

from kivymd.list import ILeftBodyTouch, TwoLineIconListItem
from kivymd.button import MDIconButton
from kivymd.dialog import MDDialog
from kivymd.textfields import MDTextField
from kivymd.card import MDCard
from kivymd.label import MDLabel

# Helper methods
from utils.urlref import add_refs

# Base python methods
from functools import partial

Builder.load_file("kv/screens/startscreen.kv")


class IconLeftWidget(ILeftBodyTouch, MDIconButton):
    pass


class UrlPopup(MDDialog):
    url = StringProperty("")

    def __init__(self, **kwargs):
        super(UrlPopup, self).__init__(**kwargs)
        self.add_action_button("Cancel", action=lambda *x: self.dismiss())
        self.add_action_button("Go", action=lambda *x: self.dismiss())


class StartScreen(Screen):
    current_menu = ListProperty([])
    first_startup = BooleanProperty(True)
    menu_jobs = ListProperty([])

    def on_enter(self):
        if self.first_startup:
            self.url_popup()
            self.first_startup = False

    def url_popup(self, *args):
        url_popup = UrlPopup()
        url_popup.bind(on_dismiss=self.generate_menu_from_url)
        url_popup.open()

    def generate_menu_from_url(self, instance):
        self.grab_items(url=instance.url)

    def on_current_menu(self, instance, value):
        log.info(len(value))
        self.generate_menu()

    def generate_menu(self, *args):
        self.ids.menu_list.clear_widgets()
        info_list_lines = []
        adding_interval = 0
        for job in self.menu_jobs:
            job.cancel()
        for item in self.current_menu:
            adding_interval += .1
            item_type = item[0]
            item_description = item[1]
            item_ending = item[2]
            item_origin = item[3]
            item_port = item[4]
            base_menu_item = TwoLineIconListItem()
            icon_widget = IconLeftWidget()
            if item_type == "1":
                icon_widget.icon = "folder"
            elif item_type == "0":
                icon_widget.icon = "file"
            elif item_type == "I":
                icon_widget.icon = "image"
            else:
                log.info("Item Type: {}".format(item_type))
                icon_widget.icon = "firefox"
            if not item_type == "i":
                base_menu_item.text = item_description
                base_menu_item.selector = item_ending
                base_menu_item.url = item_origin
                base_menu_item.port = item_port
                base_menu_item.item_type = item_type
                base_menu_item.add_widget(icon_widget)
                base_menu_item.bind(on_release=self.pressed_item)
                if info_list_lines > 0:
                    info_card = MDCard(
                        size_hint_x=.8,
                        size_hint_y=None,
                        height=dp(35) * len(info_list_lines))
                    info_text = ""
                    for line in info_list_lines:
                        info_text += add_refs(line) + "\n"
                    info_list_lines = []
                    info_label = MDLabel(
                        pos_hint={"center_x": .5,
                                  "center_y": .5},
                        text=info_text,
                        halign="center",
                        size_hint_y=None,
                        markup=True)
                    info_label.height = info_label.texture_size[1]
                    info_label.font_style = "Body1"
                    #info_recycleview.add_widget(info_label)
                    info_layout = FloatLayout()
                    info_layout.add_widget(info_label)
                    #info_card.height = info_l
                    info_card.add_widget(info_layout)
                    self.add_menu_widget(info_card)
                self.add_menu_widget(base_menu_item)
            if item_type == "i":
                info_list_lines.append(item_description)

    def add_menu_widget(self, widget, *args):
        self.ids.menu_list.add_widget(widget)

    def pressed_item(self, instance):
        log.info("Item URL: {}".format(instance.url))
        log.info("Item Port: {}".format(instance.port))
        log.info("Item Type: {}".format(instance.item_type))

        if instance.item_type == "0":
            text_item = App.get_running_app().root.call_get_textfile(
                instance.selector, instance.url, instance.port)
            text_screen = App.get_running_app(
            ).root.ids.gopher_screen_manager.get_screen("text_screen")
            text_screen.text_lines = text_item
            print(text_screen)
            log.info("Text Screen Text List: {}".format(
                len(text_screen.text_lines)))
            App.get_running_app().root.next_screen("text_screen")
        elif instance.item_type == "1":
            self.grab_items(
                url=instance.url,
                selector=instance.selector,
                port=instance.port)

    def grab_items(self, url="", selector="", port=70):
        menu_list = App.get_running_app().root.call_get_menu(
            url=url, selector=selector, port=port)
        if menu_list:
            self.current_menu = menu_list
        else:
            Clock.schedule_once(self.url_popup, 2)
