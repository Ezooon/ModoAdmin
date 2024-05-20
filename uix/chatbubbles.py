from kivy.metrics import dp

from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ListProperty
from kivy.lang import Builder
from kivy.clock import Clock

from datetime import datetime

from api.cart import Cart, CartItem
from api.item import Item
from api.message import Message

Builder.load_file("uix/chatbubbles.kv")


def am_pm(t):
    hh = t.hour if t.hour <= 12 else t.hour - 12
    c = "am" if t.hour <= 12 else "pm"
    mm = t.minute if t.minute > 9 else "0" + str(t.minute)
    return f"{hh}:{mm} {c}"


class BubbleBase(MDFloatLayout):
    BUBBLES = {}
    message = ObjectProperty(force_dispatch=True)

    text = StringProperty("...")
    sent = StringProperty("12:00 pm")
    status = NumericProperty(0)
    #  0: not sent
    #  1: sent
    #  2: delivered
    #  3: read

    def update_message(self, _):
        if self.message:
            self.message = Message.MESSAGES[self.message.id]
            return not self.message.delivered  # ToDo make it not self.message.read when you implement the read function

    def on_message(self, _, msg):
        BubbleBase.BUBBLES[msg.id] = self
        self.text = msg.content
        self.status = bool(msg.sent) + msg.delivered + msg.read
        sent = msg.sent or datetime.now()
        self.sent = am_pm(sent.time())

        if not msg.delivered:
            Clock.schedule_interval(self.update_message, 5)

    def on_height(self, _, h):
        self.height = sum([w.height for w in self.children]) - dp(10)


class ChatBubble(BubbleBase):
    pass


class CartBubble(BubbleBase):
    c_items = ListProperty()

    def on_message(self, _, msg):
        super(CartBubble, self).on_message(_, msg)

        c_items = Cart.itemsfromstr(msg.content)
        Item.check_items([ci.item.id for ci in c_items])
        self.c_items = c_items


class ReceivedBubble(BubbleBase):
    pass

