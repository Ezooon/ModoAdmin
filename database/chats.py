from sqlite3 import connect


class ChatsTable:
    # keep the handled chats
    def __init__(self):
        self.connection = connect("database/local.db")
        self.cur = self.connection.cursor()

    def get_all(self, **kwargs):
        filters = ""
        if kwargs:
            filters = " WHERE " + " ".join([f'{op} = {kwargs[op]}' for op in kwargs])
        line = "SELECT * FROM chats" + filters + ";"

        self.cur.execute(line)

        chats = []
        for chat in self.cur.fetchall():
            chats.append({
                "id": chat[0],
                "chat_name": chat[1],
                "image": chat[2],
                "owner": chat[3],
                "handler": chat[4],
                "cart": chat[5],
            })

        return chats

    def add_chats(self, chats):
        self.cur.execute("SELECT id FROM chats;")
        in_db = [m[0] for m in self.cur.fetchall()]
        for chat in chats:
            if chat.id in in_db:
                args = [
                    chat.chat_name,
                    chat.image,
                    chat.owner,
                    chat.handler,
                    chat.cart,
                    str(chat.id),
                ]
                print(args)
                self.cur.execute("""UPDATE chats SET 
                                chat_name = ?, image = ?, owner = ?, handler = ?, cart = ?
                                WHERE id = ?;""", args)
            else:
                args = [
                    chat.id,
                    chat.chat_name,
                    chat.image,
                    chat.owner,
                    chat.handler,
                    str(chat.cart),
                ]
                self.cur.execute("""INSERT INTO chats(id, chat_name, image, owner, handler, cart)
                                VALUES (?, ?, ?, ?, ?, ?);""", args)
        self.connection.commit()

    def delete_chat(self, chat_id):
        self.cur.execute('DELETE FROM chats WHERE "id" = ?', (chat_id,))
        self.cur.execute('DELETE FROM messages WHERE "chat" = ?', (chat_id,))
        self.connection.commit()

    def replace(self, old_id, chat):
        args = [chat["id"], chat["chat"], chat["sent_by"], chat["sent_to"],
                chat["content"], chat["sent"], chat["delivered"], chat["read"], old_id]
        self.cur.execute("""UPDATE chats SET 
                        id= ?, chat_name = ?, image = ?, owner = ?, handler = ?, cart = ?
                        WHERE id = ?;""", args)


db_chats = ChatsTable()
