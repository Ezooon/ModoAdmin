from .apirequest import api_request, HOST
from .item import Item


class Account:

    def __init__(self, **data):
        self.data = data

        # setting attributes
        self._fill_data(None, data)

        # auth
        self.token = ""

    def profile_picture_url(self):
        return HOST + "account/" + self.username + "/profile/"

    @classmethod
    def login(cls, username, password, on_success=lambda x: None, **kwargs):

        def logged_in(thread, data):
            on_success(data)

        body = {'username': username, 'password': password}
        api_request("account/login/", on_success=logged_in, body=body, method="POST", **kwargs)

    @classmethod
    def logout(cls):
        pass

    @classmethod
    def sign_up(cls, username, email, password, on_success=lambda x: None):

        def signed_up(thread, data):
            cls.login(username, password, on_success)

        body = {'username': username, 'email': email, 'password': password}
        api_request("account/sign-up/", on_success=signed_up, body=body, method="POST")

    def get_favorite(self, on_success=lambda x: None, results="full", **kwargs):
        def item_wrapper(_, data):
            if results == "simple":
                on_success(data)
                return
            items_data = data
            items = []
            for data in items_data:
                items.append(Item(**data))
            on_success(items)

        api_request("account/favorite/", on_success=item_wrapper, params={"results": results}, **kwargs)

    def _fill_data(self, _, data):
        self.id = data.get("id") or -1
        self.username = data.get("username") or ""
        self.email = data.get("email") or ""
        self.image = data.get('image') or ""
        self.account_type = data.get('account_type') or "CL"
        self.chat = data.get('chat') or 0

    def full_data(self):
        api_request("account/details/", self._fill_data)
        return self
