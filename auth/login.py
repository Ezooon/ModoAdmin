from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from api.account import Account
from kivymd.toast import toast
from kivymd.app import MDApp

Builder.load_file("auth/login.kv")


class Login(MDScreen):
    def login(self, username, password):
        Account.login(username, password, self.logged_in, on_failure=self.login_failed)

    def logged_in(self, data):
        app = MDApp.get_running_app()
        app.user = Account(**data).full_data()
        app.user_id = data["id"]
        app.user_api_token = data["token"]
        app.username = data["username"]
        app.email = data["email"]
        app.user.get_favorite(app.set_favorite, results="simple")

        from uix.chatbubbles import BubbleBase, Message
        BubbleBase.BUBBLES = {}
        app.chat_screen.data = []

        toast("Wellcome back " + data["username"])

        self.parent.current = "home"

    def login_failed(self, *args):
        toast("Username or Password are Wrong")
