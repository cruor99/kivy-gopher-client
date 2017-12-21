from kivy.app import App
from kivy.uix.screenmanager import Screen

from kivy.lang import Builder
from kivy.properties import ListProperty, BooleanProperty, StringProperty
from kivy.logger import Logger as log

from kivymd.list import ILeftBodyTouch, TwoLineIconListItem
from kivymd.button import MDIconButton
from kivymd.dialog import MDDialog
from kivymd.textfields import MDTextField

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

    def on_enter(self):
        if self.first_startup:
            url_popup = UrlPopup()
            url_popup.bind(on_dismiss=self.generate_menu_from_url)
            url_popup.open()

    def generate_menu_from_url(self, instance):
        self.grab_items(instance.url)

    def on_current_menu(self, instance, value):
        log.info(value)
        self.generate_menu()

    def generate_menu(self, *args):
        for item in self.current_menu:
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
                icon_widget.icon = "firefox"
            base_menu_item.text = item_description
            base_menu_item.selector = item_ending
            base_menu_item.url = item_origin
            base_menu_item.port = item_port
            base_menu_item.add_widget(icon_widget)
            base_menu_item.bind(on_release=self.pressed_item)
            self.ids.menu_list.add_widget(base_menu_item)

    def pressed_item(self, instance):
        log.info(instance.url)
        log.info(instance.port)
        text_item = App.get_running_app().root.call_get_textfile(
            instance.selector, instance.url, instance.port)
        text_screen = App.get_running_app().root.ids.gopher_screen_manager.get_screen("text_screen")
        text_screen.text_lines = text_item
        print(text_screen)
        log.info("Text Screen Text List: {}".format(len(text_screen.text_lines)))
        App.get_running_app().root.next_screen("text_screen")


    def grab_items(self, url):
        self.current_menu = App.get_running_app().root.call_get_menu(url)
