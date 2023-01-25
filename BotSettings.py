import DataBase


def init():
    return BotSettings()


class BotSettings:

    __settings = None

    def __init__(self):
        self.load_settings()

    def load_settings(self):

        if BotSettings.__settings is not None:
            return

        db = DataBase.DataBase()
        settings = db.load_bot_settings()
        BotSettings.__settings = {}

        for line in settings:
            BotSettings.__settings[line[0]] = line[1]

    def get(self, key):
        if key in BotSettings.__settings:
            return BotSettings.__settings[key]

        return ''

    def update(self, key, value):

        db = DataBase.DataBase()
        if key in BotSettings.__settings:
            db.update_bot_setting(key, value)
        else:
            db.add_bot_setting(key, value)

        BotSettings.__settings[key] = value
