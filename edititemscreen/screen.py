from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, ColorProperty
from kivymd.uix.menu import MDDropdownMenu

from api.item import Item
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen

from plyer import filechooser

Builder.load_file("edititemscreen/ui.kv")


class EditItemScreen(MDScreen):
    item = ObjectProperty(Item())
    image = StringProperty("assets/images/loading.jpg")
    background_color = ColorProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        menu_items = [{
            "text": cat,
            "viewclass": "OneLineListItem",
            "on_release": lambda x=cat: self.fill_category_field(cat),
            "halign": "right"
        } for cat in Item.Categories]
        self.menu = MDDropdownMenu(caller=self, items=menu_items, width_mult=4)

    def on_enter(self, *args):
        if self.ids:
            self.menu.caller = self.ids.category_field
            self.menu.position = "bottom"

    def on_item(self, _, item):
        self.image = item.image
        self.ids.name_field.text = item.name
        self.ids.category_field.text = item.category
        self.ids.price_field.text = str(item.price)
        self.ids.stock_field.text = str(item.stock)
        self.ids.description_field.text = item.description

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
        if menu_items and self.menu.caller != self:
            Clock.schedule_once(self.open_menu, 2)

    def open_menu(self, _):
        if not self.menu.parent and self.menu.items:
            self.menu.open()

    def choose_image(self):
        def set_image(files):
            if files:
                self.image = files[0]

        filechooser.open_file(title="Pic an Image", preview=True, on_selection=set_image,
                              filters=[["Images", "*png", "*jpg", "*webp", '*jpeg', '*jpe', '*gif',
                                       '*pbm', '*pgm', '*ppm', '*bmp', '*ico'], "*"])

    def new(self):
        self.item = Item()
        self.ids.name_field.text = ""
        self.ids.category_field.text = ""
        self.ids.price_field.text = ""
        self.ids.stock_field.text = ""
        self.ids.description_field.text = ""

    def save(self):
        item = self.item
        for n in ["name_field", "category_field", "price_field", "stock_field", "description_field"]:
            if self.ids[n].text == "":
                toast("all the fields are required")
                return

        data = {}
        if self.image != item.image: data["image"] = self.image
        if self.ids.category_field.text != item.category: data["category"] = self.ids.category_field.text
        if self.ids.name_field.text != item.name: data["name"] = self.ids.name_field.text
        if self.ids.price_field.text != str(item.price): data["price"] = self.ids.price_field.text
        if self.ids.stock_field.text != str(item.stock): data["stock"] = self.ids.stock_field.text
        if self.ids.description_field.text != item.description: data["description"] = self.ids.description_field.text
        if not data:
            toast("Saved!")
            return

        if self.item.id < 1:
            Item.new_item(data, self.created)
            return
        self.item.save(data, self.updated)

    def created(self, data):
        self.item = Item(**data)
        toast("Saved")

    def updated(self, item):
        self.item = item
        toast("Saved")
