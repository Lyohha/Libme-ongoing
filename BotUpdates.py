import BotSettings
import DataBase
import os
import telegram
from telegram.ext import Updater


def init():
    return BotUpdates()


class BotUpdates:
    version = '1.0.0'
    description = 'Обновление до версии 1.0.0:\n- Релиз первой публичной версии.'

    def __init__(self):
        updater = Updater(os.getenv('TOKEN', default=None), use_context=True)
        dispatcher = updater.dispatcher
        context = telegram.ext.callbackcontext.CallbackContext(dispatcher)
        settings = BotSettings.init()
        version = settings.get("version")

        db = DataBase.DataBase()

        if version != BotUpdates.version and BotUpdates.description != '':
            users = db.get_active_users()
            for user in users:
                try:
                    message = context.bot.send_message(
                        user[0],
                        text=BotUpdates.description,
                    )
                except Exception as exe:
                    print(exe)

            settings.update("version", BotUpdates.version)
