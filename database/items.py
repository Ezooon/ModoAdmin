from sqlite3 import connect


class ItemsTable:
    def __init__(self):
        self.connection = connect("database/local.db")
        self.cur = self.connection.cursor()

    def get(self, ids):
        ids = f"({ids[0]})" if len(ids) == 1 else tuple(ids)
        self.cur.execute(f"SELECT * FROM items WHERE id IN {tuple(ids)};")

        items = []
        for item in self.cur.fetchall():
            items.append({
                "id": item[0],
                "name": item[1],
                "description": item[2],
                "price": item[3],
                "image": item[4],
                "stock": item[5],
                "add_by": item[6],
                "online": False
            })

        return items

    def get_all(self, **kwargs):
        filters = ""
        if kwargs:
            filters = " WHERE " + " ".join([f'{op} = {kwargs[op]}' for op in kwargs])
        line = "SELECT * FROM items" + filters + ";"

        self.cur.execute(line)

        items = []
        for item in self.cur.fetchall():
            items.append({
                "id": item[0],
                "name": item[1],
                "description": item[2],
                "price": item[3],
                "image": item[4],
                "stock": item[5],
                "add_by": item[6],
            })

        return items

    def add_items(self, items):
        self.cur.execute("SELECT id FROM items;")
        in_db = [m[0] for m in self.cur.fetchall()]
        for item in items:
            if item.id not in in_db:
                args = [item.id, item.name, item.description,
                        item.price, item.image, item.stock, item.add_by]
                self.cur.execute("""INSERT INTO items(id, name, description, price, image, stock, add_by)
                                VALUES (?, ?, ?, ?, ?, ?, ?);""", args)
            else:
                args = [item.name, item.description,
                        item.price, item.image, item.stock, item.add_by, item.id]
                self.cur.execute("""UPDATE items SET 
                                name = ?, description = ?, price = ?, image = ?, stock = ?, add_by = ?
                                WHERE id = ?;""", args)
        self.connection.commit()


db_items = ItemsTable()
