from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout
from uix.incartitem import InCartItem


Builder.load_string(r"""
<CartCard>:
    orientation: "vertical"
    radius: dp(10)
    padding:  dp(5), dp(10), dp(5), 0
    spacing: dp(2)
    size_hint: 1, None
    adaptive_height: True
        
    MDBoxLayout:
        size_hint: 1, None
        height: dp(30)
        MDLabel:
            id: total
            text: str(root.total) + " SDG"
            halign: "center"
            font_style: "Caption"
            pos_hint: {"bottom": 0.9}
        MDLabel:
            id: num_of_items
            text: str(root.total_amount) + " Item" + ("" if root.total_amount == 1 else "s")
            halign: "center"
            font_style: "Caption"
            pos_hint: {"bottom": 0.9}
""")


class CartCard(MDBoxLayout):
    items = ListProperty()
    total = NumericProperty()
    total_amount = NumericProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.item_widgets = []

    def on_items(self, _, items: list):
        self.clear_widgets(self.item_widgets)
        total_amount = 0
        total = 0
        for c_item in reversed(items):
            total_amount += c_item.amount
            total += c_item.price * c_item.amount

            self.item_widgets.append(InCartItem(c_item=c_item))
            self.add_widget(self.item_widgets[-1], 1)

        self.total_amount = total_amount
        self.total = total
        self.do_layout()
