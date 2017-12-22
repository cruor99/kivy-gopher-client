from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.logger import Logger as log
from kivy.metrics import dp
from kivy.properties import BooleanProperty, StringProperty, ListProperty

# KivyMD stuff
from kivymd.theming import ThemeManager
from kivymd.snackbar import Snackbar

# gopher client stuff
from gopher import get_menu, get_textfile, get_binary

#print(get_menu("", "mushmouth.tech", "70"))


class GopherRoot(BoxLayout):
    title_url = StringProperty("")
    title_selector = StringProperty("")
    edgemove = BooleanProperty(False)
    previous_menu_details = ListProperty([])

    def __init__(self, **kwargs):
        super(GopherRoot, self).__init__(**kwargs)
        Clock.schedule_once(self.add_initial_screens)
        self.menu_list = []

    def add_initial_screens(self, *args):
        from screens.startscreen import StartScreen
        self.ids.gopher_screen_manager.add_widget(
            StartScreen(name="start_screen", id="start_screen"))
        from screens.textscreen import TextScreen
        self.ids.gopher_screen_manager.add_widget(
            TextScreen(name="text_screen", id="text_screen"))

    def call_get_menu(self, url="", selector="", port=70):
        if "gopher://" in url:
            protocol, uri = url.split("://")
            log.info("Protocol: {}".format(protocol))
            log.info("URI: {}".format(uri))
        else:
            uri = url
        uri_components = uri.split("/")
        final_url = uri_components[0]
        self.title_url = final_url
        if len(uri_components[-1]) > 0 and uri_components[-1] != final_url:
            selector = uri_components[-1]
        try:
            menu_list = get_menu(selector, final_url, port)
            previous_menu = [selector, final_url, port]
            if len(self.previous_menu_details) > 0:
                self.menu_list.append(self.previous_menu_details)
            self.previous_menu_details = previous_menu
            self.title_selector = selector
        except Exception as e:
            log.exception(e)
            Snackbar(text=str(e.args[-1])).show()
            if self.menu_list:
                return self.call_get_menu(
                    selector=self.menu_list[-1][0],
                    url=self.menu_list[-1][1],
                    port=self.menu_list[-1][2])
            else:
                return []
        return menu_list

    def on_touch_down(self, touch):
        if touch.x < dp(30):
            self.edgemove = True
        else:
            self.edgemove = False
        super(GopherRoot, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.x < dp(30):
            pass
        else:
            if self.edgemove:
                previous_menu = self.previous_menu()
                menu_screen = self.ids.gopher_screen_manager.get_screen("start_screen")
                menu_screen.current_menu = previous_menu
                self.ids.gopher_screen_manager.current = "start_screen"
                self.edgemove = False
            else:
                pass
        super(GopherRoot, self).on_touch_move(touch)

    def previous_menu(self, *args):
        previous_menu = self.menu_list.pop()
        menu_list = self.call_get_menu(selector=previous_menu[0], url=previous_menu[1], port=previous_menu[2])
        return menu_list

    def call_get_textfile(self, selector, url, port):
        self.menu_list.append(self.previous_menu_details)
        self.previous_menu_details = []
        self.title_url = url
        self.title_selector = selector
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
