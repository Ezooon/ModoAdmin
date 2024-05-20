from kivy.lang import Builder
from kivy.properties import ListProperty
from api.item import Item
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from uix.cartcard import CartCard
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.clock import Clock
from api.chat import Chat


Builder.load_file("home/orders/ui.kv")


class OrdersTap(MDBottomNavigationItem):
    data = ListProperty([])

    def __init__(self, **kwargs):
        super(OrdersTap, self).__init__(**kwargs)
        Clock.schedule_once(self.load_chats, 5)
        self._chat = None
        self.next = None
        lang = MDApp.get_running_app().lang
        dialog_cart = CartCard()
        self.dialog = MDDialog(title=lang["Accept Order"], content_cls=dialog_cart, type="custom", buttons=[
            MDFlatButton(text=lang["Back"], on_press=lambda: self.dialog.dismiss()),
            MDRaisedButton(text=lang["Cancel Order"], on_press=self.cancel_order, md_bg_color=self.theme_cls.error_color),
            MDRaisedButton(text=lang["Accept Order"], on_press=self.accept_order),
                ],
        )
        self.dialog.ids.title.halign = "right"

    def _accept_order(self, chat):
        chat.save_to_db()
        self.parent.get_screen("Handling").load_chats()
        self.load_chats()

    def accept_order(self, *args):
        self._chat.accept_order(self._accept_order)
        self.dialog.dismiss()

    def cancel_order(self, *args):
        self._chat.cancel()
        self.dialog.dismiss()

    def more_chats(self):
        if self.next:
            Chat.get_chats_from_url(self.next, self.load_items, on_failure=self.failure)
            self.next = None

    def _load_chats(self, chats, response):
        self.data = self.data + [{"chat": chat, "size_hint": (1, None), "height": 60, 'pressed': self.open_dialog} for chat in chats]
        self.next = response["next"]

    def load_chats(self, *_):
        Chat.get_unhandled_chats(self._load_chats)
        self.data = []

    def open_dialog(self, chat_card):
        self._chat = chat_card.chat
        c_items = self._chat.cart.c_items
        Item.check_items([ci.item.id for ci in c_items])
        self.dialog.content_cls.items = c_items
        self.dialog.update_height()
        self.dialog.open()
