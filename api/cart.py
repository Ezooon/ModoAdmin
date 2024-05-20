from .apirequest import api_request
from kivymd.app import MDApp
from .item import Item
from .message import Message
import json


class Cart:
    CARTS = {}

    def __init__(self, **data):
        self.data = data

        # setting attributes
        self.id = data.get("id") or -1
        self.user = data.get("user") or MDApp.get_running_app().user.id
        self.total = float(data.get("total") or 0)
        self.count = data.get("count") or 1
        self.c_items = data.get("c_items") or CartItem.wrapper(data.get("cart_items") or [])
        self.add_date = data.get("add_date") or ""
        self.delivered = data.get("delivered") or False

        if data.get("message"):
            self.message = Message(**data["message"])
        else:
            self.message = None

        # add to CARTS
        Cart.CARTS[self.id] = self

    def order(self, on_success=lambda x: None, **kwargs):

        def ordered(_, data):
            print(data)
            on_success(Cart(**data))

        body = {
            "cart_items": [
                {
                    "item": c_item.item.id,
                    "price": c_item.price,
                    "amount": c_item.amount
                }
                for c_item in self.c_items
            ]
        }

        api_request("items/carts/order/", on_success=ordered, method="POST", body=body, **kwargs)

    def compare_items(self, items):
        """items is the items of the new cart"""
        report = {"oos": []}  # oos list the out-of-stock items
        for c_item in self.c_item:
            if c_item not in items:
                report["oos"].append(c_item.item.name)

        for c_item in items:
            o_c_item = self.get_item(c_item.item.id)  # old cart item
            if c_item.amount < o_c_item.amount:
                report[c_item.id] = c_item.amount - o_c_item.amount

        return report

    def __getitem__(self, item_id):
        for c_item in self.c_item:
            if item_id in c_item.item.id:
                return c_item

    def __str__(self):
        return "C" + json.dumps({
            "id": self.id,
            "items": [
                {
                    "item": c_item.item.id,
                    "price": c_item.price,
                    "amount": c_item.amount
                } for c_item in self.c_items]
        })

    @classmethod
    def fromstr(cls, s):
        return Cart(**json.loads(s[1:]))

    @classmethod
    def itemsfromstr(cls, s):
        try:
            return CartItem.wrapper(json.loads(s[1:])["items"])
        except Exception as e:
            return []


class CartItem:
    def __init__(self, **data):
        self.data = data

        self.id = data.get("id") or -1
        self.amount = data.get("amount") or 1

        item = data.get("item") or dict()
        if isinstance(item, dict):
            self.item = Item(**item)
        else:
            self.item = Item.get_item(item)
        self.price = float(data.get("price") or self.item.price)

    @classmethod
    def wrapper(cls, items_data):
        c_item = []
        for data in items_data:
            c_item.append(CartItem(**data))
        return c_item

    def __eq__(self, other):
        return self.item.id == other.item.id

    def __repr__(self):
        return self.item.name + str(self.amount)

