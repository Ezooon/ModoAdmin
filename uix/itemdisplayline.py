from kivymd.toast import toast

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.imagelist import MDSmartTile
from kivymd.uix.spinner import MDSpinner
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, ListProperty, NumericProperty, ObjectProperty, DictProperty
from kivy.clock import Clock
from kivy.metrics import dp
from api.item import Item
from kivy.loader import Loader
from kivymd.app import MDApp

Loader.error_image = "assets/images/error.jpg"
Loader.loading_image = "assets/images/loading.jpg"
Builder.load_string("""
<ItemCard>:
    size_hint: None, 1
    width: self.height
    source: root.image
    box_radius: [0, 0, 24, 24]
    box_color: self.theme_cls.opposite_bg_normal[:3] + [0.5]
    radius: dp(24)
    BoxLayout:
        orientation: "vertical"
        padding: 0
        spacing: dp(10)
        MDLabel:
            text: root.name
            halign: "right"
            pos_hint: {"center_y": 0.5}
            shorten_from: "left"
            shorten: True
            font_size: sp(14)
            color: self.theme_cls.opposite_text_color
            outline_color: self.theme_cls.text_color
            outline_width: sp(1)
        MDLabel:
            text: str(root.price) + " SDG"
            font_style: "Caption"
            font_size: sp(12)
            color: self.theme_cls.opposite_text_color
            outline_color: self.theme_cls.text_color
            outline_width: sp(1)
            
    MDFloatLayout:
        size_hint: None, None
        size: 0, 0
        MDIconButton:
            id: heart_button
            icon: "heart-outline"
            pos: root.width - dp(48), root.height - dp(48)
            theme_text_color: "Custom"
            on_release:
                root.favorite(self)
                
        MDIconButton:
            id: cart_button
            icon: "pencil"
            theme_text_color: "Custom"
            pos: 0, root.height - dp(48)
            md_bg_color: 0, 0 , 0 ,0.001
            on_release:
                root.to_cart(self)

<ItemDisplayLine>:
    orientation: "vertical"
    size_hint: 1, None
    MDBoxLayout:
        size_hint: 1, None
        height: dp(40) 
        padding: dp(10)
        MDIconButton:
            id: button
            icon: "arrow-left"
            pos_hint: {"center_y": 0.5}
            on_release: root.button_release(self.icon)
        MDLabel:
            text: root.title
            halign: "right"
            font_style: "Subtitle1"
      
    BoxLayout:
        BoxLayout:
            size_hint: None, 1
            width: root.width - content.width if root.width > content.width else 0 
        MDRecycleView:
            id: recycle_view
            viewclass: "ItemCard"
            size_hint: 1, 1
            bar_inactive_color: 1,1,1,0
            bar_color: 1,1,1,0
            data: root.data
            do_scroll_y: False
            scroll_timeout: 500
            MDRecycleGridLayout:
                id: content
                orientation: "rl-tb"
                size_hint: None, 1
                rows: 1
                adaptive_width: True
                padding: dp(5)
                spacing: dp(10)

""")


class ItemCard(MDSmartTile):
    item = ObjectProperty(Item())
    name = StringProperty("")
    description = StringProperty("")
    price = NumericProperty(1)
    image = StringProperty("assets/images/item.jpg")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        MDApp.get_running_app().bind(favorite=self.on_favorite_items)

    def on_favorite_items(self, _, items):
        button = self.ids.heart_button
        if self.item.id in items:
            button.icon = "heart"
            button.icon_color = 1, 0, 0, 1
        else:
            button.icon = "heart-outline"
            button.icon_color = self.theme_cls.text_color

    def on_item(self, _, item):
        app = MDApp.get_running_app()

        self.name = item.name
        self.description = item.description
        self.price = item.price
        self.image = item.image

        # in favorite?
        heart_button = self.ids.heart_button
        if self.item.id in app.favorite:
            heart_button.icon = "heart"
            heart_button.icon_color = 1, 0, 0, 1
        else:
            heart_button.icon = "heart-outline"
            heart_button.icon_color = self.theme_cls.text_color

    def on_release(self):
        sm = MDApp.get_running_app().root
        sm.get_screen("item_screen").item = self.item
        sm.current = "item_screen"

    def favorite(self, button):
        app = MDApp.get_running_app()
        if app.username:
            self.item.favorite(app.set_favorite)
        else:
            app.request_login()

    def to_cart(self, button):
        toast("Use the client app to order")


class ItemDisplayLine(MDBoxLayout):
    title = StringProperty("")
    data = ListProperty([])
    params = DictProperty({"ordering": "?"})

    def __init__(self, **kwargs):
        self.spinner = MDSpinner(size=(dp(40), dp(40)))
        super(ItemDisplayLine, self).__init__(**kwargs)
        Clock.schedule_once(lambda x: self.load(), 1)
        floating = FloatLayout(size=(0, 0))
        self.add_widget(floating)
        floating.size_hint = (None, None)
        floating.add_widget(self.spinner)

    def on_center(self, _, pos):
        self.spinner.size_hint = (None, None)
        self.spinner.y = self.center_y - dp(20)
        self.spinner.x = self.center_x

    def on_params(self, _, params):
        self.load()

    def load(self):
        Item.get_items(self._load_items, params=self.params, on_failure=self.fail_to_load)
        self.spinner.active = True

    def _load_items(self, items, *_):
        """populating the display line with item widgets"""
        data = [{"item": item, "size_hint": (None, 1), "size": (self.height - dp(50), self.height - dp(50))}
                for item in items]
        self.ids.recycle_view.data = data
        self.ids.recycle_view.scroll_x = 1
        self.spinner.active = False
        self.ids.button.icon = "arrow-left"

    def fail_to_load(self, *args):
        """called on a network error or a request failure"""
        self.ids.button.icon = "reload"
        self.spinner.active = False

    def button_release(self, icon):
        """called when the more or reload button press"""
        if icon == "reload":
            self.load()
            return
        root = MDApp.get_running_app().root
        ig_screen = root.get_screen("item_grid_screen")
        ig_screen.title = self.title

        Item.get_items(ig_screen.load_items, params=self.params, on_failure=ig_screen.failure)

        root.current = "item_grid_screen"
