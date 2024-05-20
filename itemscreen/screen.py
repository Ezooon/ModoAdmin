from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ColorProperty
from api.item import Item
from utils.image_colors import get_accent_color
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

Builder.load_file("itemscreen/ui.kv")


class ItemScreen(MDScreen):
    item = ObjectProperty(Item())
    description = StringProperty("")
    price = NumericProperty(1)
    image = StringProperty("assets/images/item.jpg")
    stock = NumericProperty(1)
    background_color = ColorProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toolbar = None
        MDApp.get_running_app().bind(favorite=self.on_favorite_items)

    def add_to_favorite(self, _):
        from utils.image_colors import get_accent_color
        color = get_accent_color(self.ids.image._container.image)
        _.md_bg_color = color
        self.background_color = color

    def on_item(self, _, item):
        app = MDApp.get_running_app()

        self.ids.title.text = item.name
        self.description = item.description
        self.price = item.price
        self.image = item.image
        if self.image:
            color = get_accent_color(self.ids.image._container.image)
            self.background_color = color
        self.stock = item.stock

        # simular display line
        self.ids.simular.params = {"category": self.item.category_id}

        # in favorite?
        heart_button = self.ids.heart_button
        if self.item.id in app.favorite:
            heart_button.icon = "heart"
            heart_button.icon_color = 1, 0, 0, 1
        else:
            heart_button.icon = "heart-outline"
            heart_button.icon_color = 0, 0, 0, 1

    def on_favorite_items(self, _, items):
        if not self.item:
            return
        button = self.ids.heart_button
        if self.item.id in items:
            button.icon = "heart"
            button.icon_color = 1, 0, 0, 1
        else:
            button.icon = "heart-outline"
            button.icon_color = 0, 0, 0, 1

    def favorite(self):
        app = MDApp.get_running_app()
        if app.username:
            self.item.favorite(app.set_favorite)
        else:
            app.request_login()
