from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu

from kivymd.uix.button import MDFlatButton, MDRaisedButton

from kivymd.uix.dialog import MDDialog

from kivymd.app import MDApp

from api.message import Message, db_messages
from uix.chatbubbles import ChatBubble
from kivymd.uix.screen import MDScreen
from kivy.properties import ListProperty, ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_file("chatscreen/ui.kv")


class ChatScreen(MDScreen):
    data = ListProperty([])
    chat = ObjectProperty()

    def __init__(self, **kwargs):
        super(ChatScreen, self).__init__(**kwargs)
        messages_data = db_messages.get_all()
        messages = []
        for data in messages_data:
            messages.append(Message(**data))
        Clock.schedule_once(lambda x: self.add_messages(messages), 0)

        lang = MDApp.get_running_app().lang

        self.delivered_dialog = MDDialog(
            title=lang["Order Delivered"], type="custom",
            text=lang["The order will be marked as delivered."], buttons=[
                MDFlatButton(text=lang["Back"], on_press=lambda x: self.delivered_dialog.dismiss()),
                MDRaisedButton(text=lang["Confirm"], on_press=self.order_delivered)])

        self.drop_dialog = MDDialog(
            title=lang["Drop & Delete Chat"], type="custom",
            text=lang["You won't be able to send messages to this chat!"], buttons=[
                MDFlatButton(text=lang["Back"], on_press=lambda x: self.drop_dialog.dismiss()),
                MDRaisedButton(text=lang["Confirm"], on_press=self.drop_chat,
                               md_bg_color=self.theme_cls.error_color)])

        self.cancel_dialog = MDDialog(
            title=lang["Cancel Order"], type="custom",
            text=lang["The order will be canceled?"], buttons=[
                MDFlatButton(text=lang["Back"], on_press=lambda x: self.cancel_dialog.dismiss()),
                MDRaisedButton(text=lang["Confirm"], on_press=self.cancel_order,
                               md_bg_color=self.theme_cls.error_color)])

        menu_items = [{
                "text": lang["Order Delivered"],
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.delivered_dialog.open(),
            }, {
                "text": lang["Cancel Order"],
                "viewclass": "OneLineListItem",
                "on_release": lambda: self.cancel_dialog.open(),
            }, {
            "text": lang["Drop & Delete Chat"],
            "viewclass": "OneLineListItem",
            "on_release": lambda: self.drop_dialog.open(),
        }]
        self.menu = MDDropdownMenu(caller=None, items=menu_items, width_mult=4)

    def on_enter(self, *args):
        if self.ids:
            self.ids.sv.scroll_y = 0
            self.menu.caller = self.ids.menu_button
        self.ids.sv.refresh_from_data()

    def send(self, text_field):
        text = text_field.text
        msg = Message(content=text, chat=self.chat.id, sent_to=self.chat.owner, sent_by=self.chat.handler)
        db_messages.add_messages([msg])
        MDApp.get_running_app().send_list.append(msg)

        if text.startswith('C{"id": '):
            self.data.append({"viewclass": 'CartBubble', "message": msg,
                              "size_hint": (1, None)})
        else:
            self.data.append({"viewclass": 'ChatBubble', "message": msg,
                              "size_hint": (1, None)})
        text_field.text = ""
        self.ids.sv.refresh_from_data()

    def add_messages(self, messages, to_send=False):
        data = []
        msgs_to_send = []
        for msg in messages:
            if msg.id not in ChatBubble.BUBBLES:
                if msg.id < 1 and not to_send:
                    msgs_to_send.append(msg)
                    continue
                if msg.content.startswith('C{"id": '):
                    data.append({"viewclass": 'CartBubble', "message": msg,
                                 "size_hint": (1, None)})
                elif msg.sent_by_user:
                    data.append({"viewclass": 'ChatBubble', "message": msg,
                                 "size_hint": (1, None)})
                else:
                    data.append({"viewclass": 'ReceivedBubble', "message": msg,
                                 "size_hint": (1, None)})
            if not msg.sent:
                MDApp.get_running_app().send_list.append(msg)

        if data:
            self.data = self.data + data
            self.ids.sv.scroll_y = 0
            self.ids.sv.refresh_from_data()

        if msgs_to_send:
            msgs_to_send.sort(key=lambda x: x.id)
            msgs_to_send.reverse()
            self.add_messages(msgs_to_send, True)

    def on_chat(self, _, chat):
        ChatBubble.BUBBLES = {}
        self.data = []
        chat.get_messages(self.add_messages, on_failure=self.add_db_messages)

    def add_db_messages(self, *args):
        msgs_data = Message.db_messages.get_all(chat=self.chat.id)
        self.add_messages([Message(**data) for data in msgs_data])

    def order_delivered(self, *_):
        self.menu.dismiss()
        self.delivered_dialog.dismiss()
        self.chat.order_delivered()
        MDApp.get_running_app().root.current = "home"
        MDApp.get_running_app().root.get_screen("home").ids.handling.remove(self.chat)

    def cancel_order(self, *_):
        self.menu.dismiss()
        self.cancel_dialog.dismiss()
        self.chat.cancel_order()
        MDApp.get_running_app().root.current = "home"
        MDApp.get_running_app().root.get_screen("home").ids.handling.remove(self.chat)

    def drop_chat(self, *_):
        self.menu.dismiss()
        self.drop_dialog.dismiss()
        self.chat.drop_chat()
        MDApp.get_running_app().root.current = "home"
        MDApp.get_running_app().root.get_screen("home").ids.handling.remove(self.chat)
