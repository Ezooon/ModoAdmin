from api.chat import Chat
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import MDBottomNavigationItem

Builder.load_file("home/handling/ui.kv")


class HandlingTap(MDBottomNavigationItem):
    data = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.load_chats, 5)

    def load_chats(self, *_):
        chats = [Chat(**data) for data in Chat.db_chats.get_all()]
        Chat.get_handled_chats(self._load_chats)
        self._load_chats(chats)

    def _load_chats(self, chats, response={"next": None}):
        self.data = [{"chat": chat, "size_hint": (1, None), "height": 60, 'pressed': self.open_chat} for chat in chats]
        self.next = response["next"]

    def open_chat(self, chat_card):
        app = MDApp.get_running_app()
        app.chat_screen.chat = chat_card.chat
        app.root.current = "chat_screen"

    def remove(self, chat):
        chat_card = {"chat": chat, "size_hint": (1, None), "height": 60, 'pressed': self.open_chat}
        if chat_card in self.data:
            self.data.remove(chat_card)
            Chat.db_chats.delete_chat(chat.id)

