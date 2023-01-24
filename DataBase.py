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
                                    "last VARCHAR(30));"

        self.__create_table_tg_user = "CREATE TABLE IF NOT EXISTS tg_users(" \
                                      "chat_id VARCHAR(100), " \
                                      "show_per_page INT DEFAULT '5', " \
                                      "last_messages TEXT);"

        self.__create_table_tg_user_feed = "CREATE TABLE IF NOT EXISTS tg_user_feed(" \
                                           "id SERIAL, " \
                                           "tg_user_id BIGINT NOT NULL, " \
                                           "link_id BIGINT NOT NULL);"
        self.__create_table_downloads = "CREATE TABLE IF NOT EXISTS tg_user_feed(" \
                                        "id SERIAL, " \
                                        "file_id BIGINT NOT NULL, " \
                                        "item_id VARCHAR(100) NOT NULL, " \
                                        "link_id BIGINT NOT NULL);"

        self.__get_tg_user_by_chat_id = "SELECT * FROM tg_users WHERE chat_id = %s;"

        self.__insert_tg_user = "INSERT INTO tg_users (chat_id, show_per_page) " \
                                "VALUES (%s, %s);"

        self.__update_tg_user = "UPDATE tg_users SET show_per_page = %s WHERE chat_id = %s;"

        self.__update_tg_user_last_messages = "UPDATE tg_users SET last_messages = %s WHERE chat_id = %s;"

        self.__get_all_links = "SELECT * FROM links;"

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
