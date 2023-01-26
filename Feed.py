import DataBase
import Parser
from threading import Thread
from time import sleep
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
import telegram
import os


def init():
    return Feed()


def insert_link_to_tg_user(chat_id, link):
    db = DataBase.init()
    db.insert_in_queue(chat_id, link)


class Feed:
    links = []
    index = 0

    def __init__(self):
        self.load_links()

    def load_links(self):
        db = DataBase.init()
        links = db.get_all_links()

        for link in links:
            Feed.links.append(link[1])

    def start(self):
        thread = Thread(target=self.feed_thread, args=())
        thread.start()

    def __clear_queue(self):
        db = DataBase.init()
        items = db.get_queue()

        for item in items:
            db_link = db.get_link(item[2])

            if db_link is None:
                parser = Parser.new(item[2])

                db.insert_link(item[2],
                               parser.get_info()['title'],
                               parser.get_info()['type'],
                               parser.get_last()['chapter_id'])
                Feed.links.append(item[2])

            db.insert_link_in_feed(item[1], item[2])
            db.remove_queue_item(item[0])

    def feed_thread(self):
        updater = Updater(os.getenv('TOKEN', default=None), use_context=True)
        dispatcher = updater.dispatcher
        context = telegram.ext.callbackcontext.CallbackContext(dispatcher)

        while True:
            self.__clear_queue()

            link = Feed.links[Feed.index]

            db = DataBase.init()

            db_link = db.get_link(link)

            if db_link is not None:

                try:
                    parser = Parser.new(link)
                except:
                    sleep(10)
                    continue

                items = parser.get_all()

                users = []

                for item in items:
                    if str(item['chapter_id']) == db_link[2]:
                        break

                    if len(users) == 0:
                        users = db.get_users_by_link(link)

                    url = db_link[1] + '/v' + str(item['chapter_volume']) + '/c' + str(item['chapter_number'])

                    buttons = [[
                        InlineKeyboardButton('Перейти', url=url),
                    ]]

                    for user in users:
                        try:
                            context.bot.send_message(
                                user[0],
                                text=F"{parser.get_info()['title']}\nТом {item['chapter_volume']} Глава {item['chapter_number']}",
                                reply_markup=InlineKeyboardMarkup(buttons)
                            )
                        except Exception as exe:
                            continue

                db.update_last_in_link(db_link[0], parser.get_last()['chapter_id'])

            Feed.index = Feed.index + 1

            if Feed.index == len(Feed.links):
                Feed.index = 0

            sleep(120)
