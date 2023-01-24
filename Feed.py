import DataBase
import Parser


def init():
    return Feed()


def insert_link_to_tg_user(chat_id, link):
    db = DataBase.init()
    db_link = db.get_link(link)

    parser = Parser.new(link).get_info()

    if db_link is None:
        db.insert_link(link, parser['title'], parser['type'])
        db_link = db.get_link(link)
        Feed.links.append(link)

    db.insert_link_in_feed(chat_id, link)


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
        pass

    def feed_thread(self):
        link = Feed.links[Feed.index]

        Feed.index = Feed.index + 1

        if Feed.index == len(Feed.links):
            Feed.index = 0
