import DataBase
import requests
import re
import json


def new(link):
    return Parser(link)


class Parser:

    def __init__(self, link):
        self.__link = link
        self.__title = ''
        self.__slug = ''
        self.__type = ''
        self.__list = []

        self.process()

    def process(self):
        response = requests.get(
            url=self.__link,
        )

        match = re.search(r'window.__DATA__ = \{.+?\};', response.text)

        data = match[0].replace('window.__DATA__ = ', '')

        data = json.loads(data[:-1])

        self.__list = data['chapters']['list']

        self.__title = data['manga']['rusName']
        self.__slug = data['manga']['slug']
        self.__type = self.__get_type_by_link()

    def __get_type_by_link(self):
        site = self.__link.split('/')[2]

        if site == 'mangalib.me' or site == 'yaoilib.me' or site == 'hentailib.me':
            return 'manga'
        if site == 'ranobe.me':
            return 'ranobe'
        if site == 'animelib.me':
            return 'anime'

        return ''

    def get_all(self):
        return self.__list

    def get_new(self):
        items = self.get_all()

    def get_last(self):
        items = self.get_all()

        return items[0]

    def get_info(self):

        info = {
            'title': self.__title,
            'slug': self.__slug,
            'type': self.__type,
        }

        return info
