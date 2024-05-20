from api.item import Item
from kivymd.toast import toast
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty, ListProperty
from arabickivy import to_ar

Builder.load_file("itemgridscreen/ui.kv")


class ItemGridScreen(MDScreen):
    title = StringProperty("")
    data = ListProperty([])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next = None
        self.min_item_width = dp(150)

    # def on_enter(self, *args):
    #     if self.ids:
    #         self.ids.spinner.active = True

    def more_items(self):
        if self.next:
            Item.get_items_from_url(self.next, self.load_items, on_failure=self.failure)
            self.next = None

    def on_title(self, *_):
        self.data = []

    def load_items(self, items, response):
        self.data = self.data + [{"item": item, "size_hint": (1, None), "height": self.min_item_width} for item in items]
        self.next = response["next"]
        self.ids.spinner.active = False
        if not self.data:
            toast(to_ar(self.title) + " " + MDApp.get_running_app().lang["Does Not Exist"])

    def failure(self, *args):
        print(args)
        self.ids.spinner.active = False
        if not self.data:
            toast(MDApp.get_running_app().lang["Net Work Failure"])
