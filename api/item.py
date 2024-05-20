from .apirequest import api_request
from kivymd.app import MDApp
from database.items import db_items
from os.path import exists, split


class Item:
    ALLITEMS = {}
    Categories = {
        "Nothing": 1,
        "حقائب": 2,
        "خواتم": 3,
        "أسورة": 4,
        "عطور": 5,
        "أحذية": 6,
    }

    def __init__(self, **data):
        self.data = data
        # setting attributes
        self.id = data.get("id") or -1
        self.name = data.get("name") or ""
        self.price = float(data.get("price") or 1)
        self.description = data.get("description") or ""
        self.image = data.get("image") or "assets/images/loading.jpg"
        self.add_by = data.get("add_by") or 0
        self.category = data.get("category") or "Nothing"
        self.category_id = Item.Categories.get(self.category)
        self.stock = data.get("stock") or 0

        self.online = data.get("online") or True

        # add to ALLITEMS
        Item.ALLITEMS[self.id] = self

    @classmethod
    def get_all_categories(cls, on_success=lambda x, y: None, **kwargs):
        def success(response, categories):
            for cat in categories:
                cls.Categories[cat["name"]] = cat['id']
            on_success(response, categories)
        api_request("items/categories/", success, **kwargs)

    @classmethod
    def get_item(cls, item_id, on_success=None, **kwargs):
        if not MDApp.get_running_app().online and item_id not in cls.ALLITEMS:
            return Item(**db_items.get([item_id])[0])
        if not on_success or not cls.ALLITEMS[item_id].online:
            if item_id in cls.ALLITEMS:
                return cls.ALLITEMS[item_id]
            else:
                item = Item()
                return item

        def item_wrapper(thread, response):
            item = Item(**response)
            on_success(item)
            db_items.add_items((item,))

        api_request(f"items/{item_id}/", item_wrapper, **kwargs)

    @classmethod
    def get_items(cls, on_success=lambda x, y: None, **kwargs):
        def item_wrapper(thread, response):
            items_data = response.pop("results")
            items = []
            for data in items_data:
                items.append(Item(**data))
            on_success(items, response)

        api_request("items/all-items/", item_wrapper, **kwargs)

    @classmethod
    def get_category_items(cls, category, on_success=lambda x, y: None, **kwargs):
        def item_wrapper(thread, response):
            items_data = response.pop("results")
            items = []
            for data in items_data:
                items.append(Item(**data))
            on_success(items, response)

        api_request("items/all-items/", item_wrapper, params={"category": cls.Categories[category]}, **kwargs)

    @classmethod
    def get_items_from_url(cls, url, on_success=lambda x, y: None, **kwargs):
        def item_wrapper(thread, response):
            items_data = response.pop("results")
            items = []
            for data in items_data:
                items.append(Item(**data))
            on_success(items, response)

        api_request("", item_wrapper, full_url=url, **kwargs)

    @classmethod
    def check_items(cls, item_ids):
        ids = list(set(item_ids) - set(cls.ALLITEMS.keys()))
        items_data = db_items.get(ids)
        for item_data in items_data:
            Item(**item_data)

    def get_data(self):
        data = self.data

        data["id"] = self.id
        data["name"] = self.name
        data["price"] = self.price
        data["description"] = self.description
        data["image"] = self.image
        data["add_by"] = self.add_by
        data["category"] = Item.Categories.get(self.category)
        data["stock"] = self.stock

        self.data = data
        return self.data

    def favorite(self, on_success=lambda x: None, **kwargs):
        def success(_, data):
            on_success(data)

        api_request("account/favorite/" + str(self.id) + "/", on_success=success, method="POST")

    @classmethod
    def new_item(cls, body, on_success=lambda x: None, **kwargs):
        def success(_, data, img=None):
            if img:
                api_request("items/" + str(data["id"]) + "/image/" + data['name'] + ".jpg/", on_success=success,
                            headers={'Content-type': 'multipart/form-data'},
                            body=img, method="PATCH")
            on_success(data)

        img = None
        if "image" in body:
            img_path = body.pop("image")
            if exists(img_path):
                with open(img_path, "rb") as f:
                    img = f.read()

        api_request("items/", on_success=lambda x, y: success(x, y, img),
                    body=body, method="POST")

    def save(self, body, on_success=lambda x: None, **kwargs):
        def success(_, data):
            self.__init__(**data)
            on_success(self)

        img = None
        if "image" in body:
            img_path = body.pop("image")
            if exists(img_path):
                with open(img_path, "rb") as f:
                    img = f.read()

        api_request("items/" + str(self.id) + "/", on_success=success, body=body, method="PATCH")

        if img:
            api_request("items/" + str(self.id) + "/image/" + self.name + ".jpg/", on_success=success,
                        headers={'Content-type': 'multipart/form-data'},
                        body=img, method="PATCH")

    def __repr__(self):
        return f"<id: {self.id}, {self.name}>"
