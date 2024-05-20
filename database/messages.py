from sqlite3 import connect


class MessagesTable:
    def __init__(self):
        self.connection = connect("database/local.db")
        self.cur = self.connection.cursor()

    def get_all(self, **kwargs):
        filters = ""
        if kwargs:
            filters = " WHERE " + " ".join([f'{op} {"=" if kwargs[op] is not None else "is"}'
                                            f' {kwargs[op] if kwargs[op] is not None else "NULL"}' for op in kwargs])
        line = "SELECT * FROM messages" + filters + ";"

        self.cur.execute(line)

        messages = []
        for msg in self.cur.fetchall():
            messages.append({
                "id": msg[0],
                "chat": msg[1],
                "sent_by": msg[2],
                "sent_to": msg[3],
                "content": msg[4],
                "sent": msg[5],
                "delivered": msg[6],
                "read": msg[7],
            })
        return messages

    def add_messages(self, messages):
        self.cur.execute("SELECT id FROM messages;")
        in_db = [m[0] for m in self.cur.fetchall()]
        for msg in messages:
            if msg.id in in_db:
                args = [msg.chat, msg.sent_by, str(msg.sent_to),
                        msg.content, msg.sent, msg.delivered, msg.read, msg.id]
                self.cur.execute("""UPDATE messages SET 
                                chat = ?, sent_by = ?, sent_to = ?, content = ?, sent = ?, delivered = ?, read = ?
                                WHERE id = ?;""", args)
            else:
                args = [str(msg.id), msg.chat, str(msg.sent_by), str(msg.sent_to),
                        msg.content, msg.sent, msg.delivered, msg.read]
                self.cur.execute("""INSERT INTO messages(id, chat, sent_by, sent_to, content, sent, delivered, read)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?);""", args)
        self.connection.commit()

    def replace(self, old_id, msg):
        args = [msg["id"], msg["chat"], msg["sent_by"], msg["sent_to"],
                msg["content"], msg["sent"], msg["delivered"], msg["read"], old_id]
        self.cur.execute("""UPDATE messages SET 
                        id= ?, chat = ?, sent_by = ?, sent_to = ?, content = ?, sent = ?, delivered = ?, read = ?
                        WHERE id = ?;""", args)

    def __eq__(self, other):
        return self.id == other.id


db_messages = MessagesTable()
