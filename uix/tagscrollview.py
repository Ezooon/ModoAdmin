from kivymd.uix.recycleview import RecycleView
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivy.properties import StringProperty
Builder.load_string("""
<TagCard>:
    padding: dp(10)
    spacing: dp(5)
    adaptive_width: True
    Label:
        size_hint: None, 1
        width: self.texture_size[0] + dp(20)
        text: root.text
        color: root.theme_cls.opposite_bg_normal
        halign: "center"
    Image:
        size_hint: None, 0.6
        width: self.height
        source: root.source
        pos_hint: {"center_y": 0.5}

<TagScrollView>:
    viewclass: "TagCard"
    size_hint: 1, None
    bar_inactive_color: 1,1,1,0
    bar_color: 1,1,1,0
    scroll_timeout: 500
    MDRecycleGridLayout:
        orientation: "rl-tb"
        size_hint: None, 1
        rows: 1
        adaptive_width: True
        padding: dp(10)
        spacing: dp(5)

""")


class TagCard(MDCard):
    text = StringProperty("")
    source = StringProperty("")


class TagScrollView(RecycleView):

    def add_widget(self, widget, *args, **kwargs):
        super(TagScrollView, self).add_widget(widget, *args, **kwargs)
        self.scroll_x = 1
