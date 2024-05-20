from kivy.lang import Builder
from kivymd.uix.list import OneLineRightIconListItem
from kivy.properties import StringProperty
Builder.load_string("""
<OneLineIconItem>:
    halign: "right"
    IconRightWidgetWithoutTouch:
        icon: root.icon

""")


class OneLineIconItem(OneLineRightIconListItem):
    halign = StringProperty('left')
    icon = StringProperty('')

    def on_halign(self, _, h):
        self.ids._lbl_primary.halign = h
