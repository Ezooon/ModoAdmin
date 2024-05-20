import webbrowser

from api.message import Message
from kivymd.app import MDApp
from kivymd.uix.screenmanager import ScreenManager
from kivymd.toast import toast
from kivy.properties import StringProperty, ObjectProperty, ListProperty, BooleanProperty, NumericProperty
from kivy.clock import Clock
import json


with open('about.txt', 'r') as f:
    about = f.read()
with open('privacy policy.txt', 'r') as f:
    privacy_policy = f.read()


class SM(ScreenManager):
    pass


class ModoAdminApp(MDApp):
    online = BooleanProperty()

    user = ObjectProperty()
    user_id = NumericProperty(0)
    username = StringProperty("")
    email = StringProperty("")
    user_api_token = StringProperty("")

    cart = ObjectProperty()

    favorite = ListProperty([])
    send_list = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lang = None
        self.chat_screen = None
        self.about = about
        self.privacy_policy = privacy_policy
        self.send_list = []

    def build_config(self, config):
        config.setdefaults("App", {
            "first launch": True,
            "language": "Arabic"
        })

        config.setdefaults("Account", {
            "id": 0,
            "username": "",
            "email": "",
            "user_api_token": "",
        })

    def build(self):
        # language
        with open('assets/lang/' + self.config.get("App", "language") + ".json", "r", encoding="UTF-8") as jf:
            self.lang = json.load(jf)

        # account
        from api.account import Account

        self.user_id = self.config.getint("Account", "id")
        self.username = self.config.get("Account", "username")
        self.email = self.config.get("Account", "email")
        self.user_api_token = self.config.get("Account", "user_api_token")

        self.user = Account(id=self.user_id, username=self.username, email=self.email).full_data()

        # favorites
        self.user.get_favorite(self.set_favorite, results="simple")

        # loading the to send Q
        self.send_list = Message.get_not_sent()

        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        sm = SM()

        # start chat check loop
        self.chat_screen = sm.get_screen("chat_screen")
        Clock.schedule_interval(self.check_new_messages, 5)

        # if the first launch start with the login screen
        first_launch = self.config.getboolean("App", "first launch")  # ToDo uncomment this
        if first_launch:
            sm.current = "login"
        else:
            sm.current = "home"
        self.config.set("App", "first launch", False)
        self.config.write()
        return sm

    def check_new_messages(self, dt):
        from api.message import Message

        def set_offline(request, data):
            if self.online and not isinstance(data, dict):
                self.online = False
                toast("You Are Offline", (1, 0, 0, 1))

        def set_online(*args):
            if not self.online:
                self.online = True
                toast("You Are Back Online", (0, 1, 0, 1))
                self.connected()
            self.chat_screen.add_messages(*args)

        def re_msg(msg, *_):
            self.send_list.append(msg)

        Message.get_undelivered_messages(self.chat_screen.chat, set_online, on_failure=set_offline)
        Message.refresh_unread()

        self.send_list.sort(key=lambda x: x.id)
        self.send_list.reverse()
        for msg in self.send_list:
            msg.send(chat=self.chat_screen.chat, on_failure=re_msg)
        self.send_list = []

    def connected(self):
        from api.item import Item
        Item.get_all_categories()
        self.root.get_screen("home").ids.handling.load_chats()

    def request_login(self, *args):
        self.root.current = "login"

    def on_username(self, _, value):
        self.config.set("Account", "username", value)
        self.config.write()

    def on_user_id(self, _, value):
        self.config.set("Account", "id", value)
        self.config.write()

    def on_email(self, _, value):
        self.config.set("Account", "email", value)
        self.config.write()

    def on_user_api_token(self, _, value):
        self.config.set("Account", "user_api_token", value)
        self.config.write()

    def set_favorite(self, results):
        self.favorite = [fitem['item'] for fitem in results]

    def open_url(self, url):
        webbrowser.open(url)

    def logout(self):
        from api.account import Account
        self.user = Account()
        self.user_id = self.user.id
        self.username = self.user.username
        self.email = self.user.email
        self.user_api_token = ""


ModoAdminApp().run()
