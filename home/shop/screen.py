from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from uix.itemdisplayline import Item, ItemDisplayLine
Builder.load_file("home/shop/ui.kv")


class ShopTap(MDBottomNavigationItem):
    def search(self, text_field):
        root = MDApp.get_running_app().root
        ig_screen = root.get_screen("item_grid_screen")
        ig_screen.title = text_field.text

        Item.get_items(ig_screen.load_items, params={"search": text_field.text}, on_failure=ig_screen.failure)

        root.current = "item_grid_screen"

    def on_ids(self, _, ids):
        if "displays" in ids:
            for cat in Item.Categories:
                if cat != 'Nothing':
                    self.ids.displays.add_widget(ItemDisplayLine(
                        height=dp(190),
                        title=cat,
                        params={"category": Item.Categories[cat]}))
