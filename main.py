from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

# KivyMD stuff
from kivymd.theming import ThemeManager
from kivymd.snackbar import Snackbar

# gopher client stuff
from gopher import get_menu, get_textfile, get_binary

#print(get_menu("", "mushmouth.tech", "70"))


class GopherRoot(BoxLayout):

    def __init__(self, **kwargs):
        super(GopherRoot, self).__init__(**kwargs)
        Clock.schedule_once(self.add_initial_screens)

    def add_initial_screens(self, *args):
        from screens.startscreen import StartScreen
        self.ids.gopher_screen_manager.add_widget(
            StartScreen(name="start_screen", id="start_screen"))
        from screens.textscreen import TextScreen
        self.ids.gopher_screen_manager.add_widget(
            TextScreen(name="text_screen", id="text_screen"))

    def call_get_menu(self, url):
        selector = ""
        host = ""
        port = 70
        if "gopher://" in url:
            selector, host = url.split("://")
        else:
            host = url
        menu_list = get_menu("", host, port)
        return menu_list

    def call_get_textfile(self, selector, url, port):
        text_item = get_textfile(selector, url, port)
        return text_item

    def next_screen(self, neoscreen):
        self.ids.gopher_screen_manager.current = neoscreen



class GopherApp(App):
    theme_cls = ThemeManager()

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.primary_hue = "900"
        return GopherRoot()


if __name__ == "__main__":
    GopherApp().run()
