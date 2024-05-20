from kivymd.app import MDApp
from .cart import Cart
from .message import Message
from .apirequest import api_request
from database.chats import db_chats


class Chat:
    CHATS = {}
    db_chats = db_chats

    def __init__(self, **data):
        self.data = data
        # setting attributes
        self.id = data.get("id") or -1
        self.chat_name = data.get("chat_name") or "Chat Name"
        self.image = data.get("image") or "assets/images/account_default.jpg"
        self.owner = data.get("owner") or -1
        self.handler = data.get("handler") or -1

        if isinstance(data.get("cart"), str):
            self.cart = Cart.fromstr(data['cart'])
        else:
            self.cart = Cart(**data.get("cart") or {})

        messages_data = data.get("messages") or []
        self.messages = [Message(**msg_data) for msg_data in messages_data]

    def get_messages(self, on_success=lambda x: None, **kwargs):
        def success(msgs):
            self.messages = msgs
            on_success(msgs)

        Message.get_all_messages(success, params={'chat': self.id}, body={"after": self.cart.add_date}, **kwargs)

    @classmethod
    def get_unhandled_chats(cls, on_success, **kwargs):
        def success(_, response):
            chats_data = response.pop("results")
            chats = [Chat(**chat_data) for chat_data in chats_data]
            on_success(chats, response)

        api_request("chat/unhandled/", success, **kwargs)

    @classmethod
    def get_handled_chats(cls, on_success, **kwargs):
        def success(_, response):
            chats_data = response.pop("results")
            chats = [Chat(**chat_data) for chat_data in chats_data]
            on_success(chats, response)

        api_request("chat/all/", success, params={"handler": MDApp.get_running_app().user_id}, **kwargs)

    @classmethod
    def get_chats_from_url(cls, url, on_success=lambda x, y: None, **kwargs):
        def success(_, response):
            chats_data = response.pop("results")
            chats = [Chat(**chat_data) for chat_data in chats_data]
            on_success(chats, response)

        api_request("", success, full_url=url, **kwargs)

    def save_to_db(self):
        db_chats.add_chats([self])

    def accept_order(self, on_success):
        def success(_, response):
            self.handler = response["handler"]
            on_success(self)

        api_request("chat/" + str(self.id) + "/handle/", success, method="PUT")

    def order_delivered(self, on_success=lambda x: None):
        def success(_, response):
            on_success(self)

        api_request("chat/" + str(self.id) + "/delivered/", success, method="PUT")

    def cancel_order(self, on_success=lambda x: None):
        def success(_, response):
            on_success(self)

        api_request("chat/" + str(self.id) + "/cancel/", success, method="PUT")

    def drop_chat(self, on_success=lambda x: None):
        def success(_, response):
            on_success(self)

        api_request("chat/" + str(self.id) + "/drop/", success, method="PUT")

