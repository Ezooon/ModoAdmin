from kivymd.uix.card import MDCard
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.lang import Builder


Builder.load_string("""
<ChatCard>:
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
                text: str(root.total) + " SDG"
                font_style: "Caption"
            MDLabel:
                text: " X " + str(root.count)
                font_style: "Caption"
                halign: "right"
    FitImage:
        size_hint: None, 1
        source: root.image
        width: self.height
        keep_ratio: False
        radius: root.radius
""")


class ChatCard(MDCard):
    chat = ObjectProperty(force_dispatch=True)
    name = StringProperty("Chat Name")
    image = StringProperty("https://notarealimage.com/image0")
    total = NumericProperty(0)
    count = NumericProperty(1)

    def on_chat(self, _, chat):
        self.image = chat.image
        self.total = chat.cart.total
        self.count = chat.cart.count
        self.name = chat.chat_name

    def pressed(self, instance):
        pass
