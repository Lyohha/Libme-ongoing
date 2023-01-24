import psycopg2
import os


def init():
    return DataBase()


class DataBase:

    def __init__(self):
        self.__create_table_bot_settings = "CREATE TABLE IF NOT EXISTS bot_settings( " \
                                           "key VARCHAR(100) NOT NULL," \
                                           "value VARCHAR(100) NOT NULL);"
        self.__create_table_links = "CREATE TABLE IF NOT EXISTS links(" \
                                    "id SERIAL, " \
                                    "link TEXT, " \
                                    "last VARCHAR(30), " \
                                    "title TEXT, "\
                                    "type VARCHAR(30));"
        self.__create_table_tg_user = "CREATE TABLE IF NOT EXISTS tg_users(" \
                                      "chat_id VARCHAR(100) NOT NULL, " \
                                      "show_per_page INT DEFAULT '5', " \
                                      "last_messages TEXT);"
        self.__create_table_tg_user_feed = "CREATE TABLE IF NOT EXISTS feed(" \
                                           "id SERIAL, " \
                                           "chat_id VARCHAR(100) NOT NULL, " \
                                           "link TEXT NOT NULL);"
        self.__create_table_downloads = "CREATE TABLE IF NOT EXISTS downloads(" \
                                        "id SERIAL, " \
                                        "file_id BIGINT NOT NULL, " \
                                        "item_id VARCHAR(100) NOT NULL, " \
                                        "link BIGINT NOT NULL);"

        self.__get_tg_user_by_chat_id = "SELECT * FROM tg_users WHERE chat_id = %s;"
        self.__insert_tg_user = "INSERT INTO tg_users (chat_id, show_per_page) " \
                                "VALUES (%s, %s);"
        self.__update_tg_user = "UPDATE tg_users SET show_per_page = %s WHERE chat_id = %s;"
        self.__update_tg_user_last_messages = "UPDATE tg_users SET last_messages = %s WHERE chat_id = %s;"
        self.__get_active_users = "select chat_id from tg_users"

        self.__get_all_links = "SELECT * FROM links;"
        self.__get_link = "SELECT * FROM links WHERE link = %s;"
        self.__insert_link = "INSERT INTO links (link, title, type) VALUES (%s, %s, %s);"
        self.__update_last_in_link = "UPDATE links SET last = %s WHERE id = %s;"

        self.__insert_link_in_feed = "INSERT INTO feed (chat_id, link) VALUES (%s, %s);"
        self.__get_record_from_feed_by_chat_id_link = "SELECT * FROM feed WHERE chat_id = %s AND link = %s;"
        self.__get_chat_id_feed_paged = "SELECT feed.*, links.title FROM feed " \
                                        "LEFT JOIN links ON (feed.link = links.link) " \
                                        "WHERE chat_id = %s ORDER BY id DESC LIMIT %s OFFSET %s;"
        self.__get_chat_id_feed_count = "SELECT count(id) FROM feed WHERE chat_id = %s;"
        self.__remove_link_from_feed = "DELETE FROM feed WHERE chat_id = %s and id = %s"

        self.__get_bot_settings = "SELECT * from bot_settings"
        self.__add_bot_settings = "INSERT INTO bot_settings (key, value) " \
                                  "VALUES (%s, %s)"
        self.__update_bot_settings = "UPDATE bot_settings SET value = %s " \
                                     "WHERE key = %s"

    def __connection(self):
        return psycopg2.connect(
            host=os.getenv('HOST', default=None),
            user=os.getenv('USER', default=None),
            password=os.getenv('PASSWORD', default=None),
            database=os.getenv('DATABASE', default=None),
        )

    def init_database(self):
        connection = self.__connection()

        with connection:
            cur = connection.cursor()
            cur.execute(self.__create_table_bot_settings)
            cur.close()

        with connection:
            cur = connection.cursor()
            cur.execute(self.__create_table_links)
            cur.close()

        with connection:
            cur = connection.cursor()
            cur.execute(self.__create_table_tg_user)
            cur.close()

        with connection:
            cur = connection.cursor()
            cur.execute(self.__create_table_tg_user_feed)
            cur.close()

        with connection:
            cur = connection.cursor()
            cur.execute(self.__create_table_downloads)
            cur.close()

    def get_tg_user_by_chat_id(self, chat_id):
        connection = self.__connection()

        with connection:
            cur = connection.cursor()
            cur.execute(self.__get_tg_user_by_chat_id, (str(chat_id),))
            users = cur.fetchall()
            cur.close()

        if len(users) > 0:
            return users[0]
        return None

    def insert_tg_user(self, chat_id, show_per_page):
        user = self.get_tg_user_by_chat_id(chat_id)

        if user is not None:
            self.update_tg_user(chat_id, show_per_page)
            return

        connection = self.__connection()

        with connection:
            cur = connection.cursor()
            cur.execute(self.__insert_tg_user, (str(chat_id), str(show_per_page),))
            cur.close()

    def update_tg_user(self, chat_id, show_per_page):
        user = self.get_tg_user_by_chat_id(chat_id)

        if user is None:
            self.insert_tg_user(chat_id, show_per_page)
            return

        connection = self.__connection()

        with connection:
            cur = connection.cursor()
            cur.execute(self.__update_tg_user, (str(show_per_page), str(chat_id), ))
            cur.close()

    def update_tg_user_last_messages(self, chat_id, messages):
        connection = self.__connection()

        with connection:
            cur = connection.cursor()
            cur.execute(self.__update_tg_user_last_messages, (str(messages), str(chat_id),))
            cur.close()

    def get_active_users(self):
        __my_db_connector = self.__connection()
        with __my_db_connector:
            __con = __my_db_connector.cursor()
            __con.execute(self.__get_active_users)
            __my_db_connector.commit()
            all = __con.fetchall()
            __con.close()
        return all

    def get_link(self, link):
        connection = self.__connection()

        with connection:
            cur = connection.cursor()
            cur.execute(self.__get_link, (str(link),))
            links = cur.fetchall()
            cur.close()

        if len(links) > 0:
            return links[0]
        return None

    def get_all_links(self, link):
        connection = self.__connection()

        with connection:
            cur = connection.cursor()
            cur.execute(self.__get_all_links, ())
            links = cur.fetchall()
            cur.close()
        return links

    def insert_link(self, link, title, ltype):
        connection = self.__connection()

        with connection:
            cur = connection.cursor()
            cur.execute(self.__insert_link, (str(link), str(title), str(ltype),))
            cur.close()

    def get_record_from_feed_by_chat_id_link(self, chat_id, link):
        connection = self.__connection()

        with connection:
            cur = connection.cursor()
            cur.execute(self.__get_record_from_feed_by_chat_id_link, (str(chat_id), str(link),))
            links = cur.fetchall()
            cur.close()

        if len(links) > 0:
            return links[0]
        return None

    def insert_link_in_feed(self, chat_id, link):

        db_link = self.get_record_from_feed_by_chat_id_link(chat_id, link)

        if db_link is not None:
            return

        connection = self.__connection()
        with connection:
            cur = connection.cursor()
            cur.execute(self.__insert_link_in_feed, (chat_id, link,))
            cur.close()

    def get_chat_id_feed_count(self, chat_id):
        user = self.get_tg_user_by_chat_id(chat_id)
        if user is None:
            return []

        connection = self.__connection()

        with connection:
            cur = connection.cursor()
            cur.execute(self.__get_chat_id_feed_count, (str(chat_id), ))
            count = cur.fetchall()
            cur.close()

        return count[0][0]

    def get_chat_id_feed_paged(self, chat_id, page):
        user = self.get_tg_user_by_chat_id(chat_id)
        if user is None:
            return []

        connection = self.__connection()

        with connection:
            cur = connection.cursor()
            cur.execute(self.__get_chat_id_feed_paged, (str(chat_id), user[1], page * user[1]))
            links = cur.fetchall()
            cur.close()

        return links

    def remove_link_from_feed(self, chat_id, id):
        connection = self.__connection()

        with connection:
            cur = connection.cursor()
            cur.execute(self.__remove_link_from_feed, (str(chat_id), str(id), ))
            cur.close()

    def load_bot_settings(self):
        __my_db_connector = self.__connection()
        with __my_db_connector:
            __con = __my_db_connector.cursor()
            __con.execute(self.__get_bot_settings)
            __my_db_connector.commit()
            all = __con.fetchall()
            __con.close()
        return all

    def update_bot_setting(self, key, value):
        __my_db_connector = self.__connection()
        with __my_db_connector:
            __con = __my_db_connector.cursor()
            __con.execute(self.__update_bot_settings, (value, key, ))
            __my_db_connector.commit()
            __con.close()

    def add_bot_setting(self, key, value):
        __my_db_connector = self.__connection()
        with __my_db_connector:
            __con = __my_db_connector.cursor()
            __con.execute(self.__add_bot_settings, (key, value, ))
            __my_db_connector.commit()
            __con.close()