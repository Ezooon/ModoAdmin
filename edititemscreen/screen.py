from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ColorProperty
from kivymd.uix.menu import MDDropdownMenu

from api.item import Item
from utils.image_colors import get_accent_color
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from plyer import filechooser

Builder.load_file("edititemscreen/ui.kv")


class EditItemScreen(MDScreen):
    item = ObjectProperty(Item())
    description = StringProperty("")
    price = NumericProperty(1)
    image = StringProperty("assets/images/loading.jpg")
    stock = NumericProperty(1)
    background_color = ColorProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        menu_items = [{
            "text": cat,
            "viewclass": "OneLineListItem",
            "on_release": lambda x=cat: self.fill_category_field(cat),
            "halign": "right"
        } for cat in Item.Categories]
        self.menu = MDDropdownMenu(caller=None, items=menu_items, width_mult=4, position="bottom")

    def on_enter(self, *args):
        if self.ids:
            self.menu.caller = self.ids.category_field

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

    def fill_category_field(self, cat):
        self.ids.category_field.text = cat

    def filter_categories(self, text):
        self.menu.dismiss()
        _cats = list(Item.Categories.keys())
        cats = filter(lambda cat: text in cat, _cats)
        menu_items = [{
            "text": cat,
            "viewclass": "OneLineListItem",
            "on_release": lambda x=cat: self.fill_category_field(cat),
            "halign": "right"
        } for cat in cats]
        self.menu.items = menu_items
        if menu_items:
            Clock.schedule_once(lambda x: self.menu.open(), 1)

    def choose_image(self):
        def set_image(files):
            self.image = files[0]
        filechooser.open_file(title="Pic an Image", preview=True, on_selection=set_image,
                              filters=["*png", "*jpg", "*webp", '*jpeg', '*jpe', '*gif',
                                       '*pbm', '*pgm', '*ppm', '*bmp', '*ico'])
