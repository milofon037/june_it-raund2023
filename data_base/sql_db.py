import sqlite3 as sql


class Database:
    def __init__(self, db_file):
        self.connection = sql.connect(db_file)
        self.cur = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            res = self.cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id, )).fetchall()
            return bool(len(res))

    def add_user(self, user_id, lang):
        with self.connection:
            return self.cur.execute("INSERT INTO users (user_id, language) values (?, ?)", (user_id, lang))

    def set_lang(self, user_id, lang):
        with self.connection:
            return self.cur.execute("UPDATE users SET language = ? WHERE user_id = ?", (lang, user_id))

    def get_lang(self, user_id):
        with self.connection:
            return self.cur.execute("SELECT language FROM users WHERE user_id = ?", (user_id, )).fetchone()[0]
