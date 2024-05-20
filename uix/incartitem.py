from kivymd.uix.card import MDCardSwipe, MDCardSwipeFrontBox
from kivymd.app import MDApp
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.lang import Builder


Builder.load_string("""
<InCartItem>:
    md_bg_color: 1,1,1,1
    size_hint: 1, None
    height: dp(60)
    radius: dp(10)
    on_release: root.pressed(root)
    MDBoxLayout:
        orientation: "vertical"
        padding:  dp(5), dp(10), dp(5), 0
        MDLabel:
            text: root.name
            halign: "right"
        BoxLayout:
            MDLabel:
                text: str(root.price * root.amount) + " SDG"
                font_style: "Caption"
            MDLabel:
                text: str(root.price) + " X " + str(root.amount)
                font_style: "Caption"
                halign: "right"
    FitImage:
        size_hint: None, 1
        source: root.image
        width: self.height
        keep_ratio: False
        radius: root.radius

<InCartSwipeItem>:
    height: dp(50)
    item_card: item_card
    md_bg_color: 1,1,1,0
    size_hint: 1, None
    height: dp(60)
    radius: dp(10)
    on_swipe_complete:
        app.cart.remove_item(self.c_item.item.id)
    MDCardSwipeLayerBox:
        md_bg_color: 1,0,0,0
    InCartItem:
        id: item_card
        c_item: root.c_item
        radius: root.radius
        size_hint: 1, 1
        pressed: root.pressed
""")


class InCartSwipeItem(MDCardSwipe):
    c_item = ObjectProperty()

    def pressed(self, instance):
        pass


class InCartItem(MDCardSwipeFrontBox):
    c_item = ObjectProperty(force_dispatch=True)
    name = StringProperty("Item")
    image = StringProperty("assets/images/item.jpg")
    price = NumericProperty(0)
    amount = NumericProperty(1)

    def on_item(self, item):
        self.name = item.name
        self.image = item.image

    def on_amount(self, _, amount):
        self.c_item.amount = amount

    def on_c_item(self, _, c_item):
        self.name = c_item.item.name
        self.image = c_item.item.image
        self.price = c_item.price
        self.amount = c_item.amount

        if not c_item.item.online:
            MDApp.get_running_app().bind(online=self.on_online)

    def on_online(self, _, online):
        if online:
            if not self.c_itme.item.online:
                from api.item import Item
                self.c_item = Item.get_item(self.c_itme.item.id, on_success=self.on_item)
            MDApp.get_running_app().unbind(online=self.on_online)

    def pressed(self, instance):
        sm = MDApp.get_running_app().root
        sm.get_screen("item_screen").item = self.c_item.item
        sm.current = "item_screen"

