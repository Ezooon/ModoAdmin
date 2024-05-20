from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen

Builder.load_file("favoritescreen/ui.kv")


class FavoriteScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_item_width = dp(150)

    def on_enter(self):
        MDApp.get_running_app().user.get_favorite(self.load_items)

    def load_items(self, data):
        self.data = [{"item": item, "size_hint": (1, None), "height": self.min_item_width} for item in data]
        self.ids.recycle_view.scroll_x = 1
