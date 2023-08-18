import psycopg2

class DataBase:
    def __init__(self, host, port, data, user, password):
        self.connect = psycopg2.connect(
            host=host,
            port=port,
            database=data,
            user=user,
            password=password
        )
        self.cursor = self.connect.cursor()

    def add_user(self, user_id, first_name, username, lang):
        with self.connect:
            self.cursor.execute("INSERT INTO users(user_id, first_name, username, lang) VALUES(%s, %s, %s, %s)", (user_id, first_name, username, lang,))
            self.connect.commit()

    def check_user(self, user_id):
        with self.connect:
            self.cursor.execute("SELECT user_id FROM users WHERE user_id=%s", (user_id,))
            return bool(len(self.cursor.fetchall()))

    def add_queue(self, chat_id):
        with self.connect:
            self.cursor.execute("INSERT INTO queue(chat_id) VALUES(%s)", (chat_id,))
            self.connect.commit()

    def delete_queue(self, chat_id):
        with self.connect:
            self.cursor.execute("DELETE FROM queue WHERE chat_id=%s", (chat_id,))
            self.connect.commit()

    def get_queue(self, user_id):
        with self.connect:
            self.cursor.execute("SELECT chat_id FROM queue WHERE chat_id=%s", (user_id,))
            que_info = self.cursor.fetchone()
            if que_info is None:
                return False
            else:
                return True

    def get_user_queue(self):
        with self.connect:
            self.cursor.execute("SELECT chat_id FROM queue")
            user = self.cursor.fetchone()
            if user is not None and bool(len(user)):
                return user[0]
            else:
                return False

    def create_chat(self, chat_one, chat_two):
        with self.connect:
            if chat_two != 0:
                self.cursor.execute("DELETE FROM queue WHERE chat_id=%s", (chat_two,))
                self.cursor.execute("INSERT INTO chats(chat_one, chat_two) VALUES(%s, %s)", (chat_one, chat_two,))
                self.connect.commit()
                return True
            else:
                return False

    def delete_chat(self, user_id):
        with self.connect:
            self.cursor.execute("DELETE FROM chats WHERE chat_one=%s OR chat_two=%s", (user_id, user_id,))
            self.connect.commit()


    def get_active_chat(self, user_id):
        with self.connect:
            self.cursor.execute("SELECT * FROM chats WHERE chat_one=%s OR chat_two=%s", (user_id, user_id,))
            users = self.cursor.fetchone()
            if users is not None:
                if users[1] == user_id:
                    return users[2]
                elif users[2] == user_id:
                    return users[1]
            else:
                return False

    def get_lang(self, user_id):
        with self.connect:
            self.cursor.execute("SELECT lang FROM users WHERE user_id=%s", (user_id,))
            return self.cursor.fetchone()[0]

    def add_dates(self, user_id, dates):
        with self.connect:
            self.cursor.execute("UPDATE users SET dates=%s WHERE user_id=%s", (dates, user_id,))

    def check_dates(self, user_id):
        with self.connect:
            self.cursor.execute("SELECT dates FROM users WHERE user_Id=%s", (user_id,))
            return self.cursor.fetchone()[0]

    def del_dates(self, user_id):
        with self.connect:
            self.cursor.execute("UPDATE users SET dates=NULL WHERE user_id=%s", (user_id,))
            self.connect.commit()

    def update_dates(self, user_id, dates):
        with self.connect:
            self.cursor.execute("UPDATE users SET dates=%s WHERE user_id=%s", (dates, user_id,))
            self.connect.commit()

    def get_channels(self):
        with self.connect:
            self.cursor.execute("SELECT channel FROM channels")
            a = self.cursor.fetchall()
            result = [item[0] for item in a]
            return result
        
    def check_channels(self):
        with self.connect:
            self.cursor.execute("SELECT channel FROM channels")
            return self.cursor.fetchone()
