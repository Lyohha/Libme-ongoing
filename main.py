import DataBase
import Consts
import List
import TGUser
import AddLink
import Feed
import BotUpdates
import os
from time import sleep
from dotenv import load_dotenv
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

load_dotenv()


def main():
    DataBase.init().init_database()
    BotUpdates.init()
    if os.getenv('ENABLE_FEED', default=False):
        Feed.init().start()

    updater = Updater(os.getenv('TOKEN', default=None), use_context=True)
    dispatcher = updater.dispatcher

    if os.getenv('ENABLE_MESSAGE_PARSER', default=False):
        control_handler = ConversationHandler(
            entry_points=[
                CommandHandler('start', TGUser.start),
                CommandHandler('buttons', TGUser.buttons),
                MessageHandler(Filters.regex(Consts.BUTTONS.ADD), AddLink.on_new),
                MessageHandler(Filters.regex(Consts.BUTTONS.CANCEL), AddLink.on_cancel),
                MessageHandler(Filters.regex(Consts.BUTTONS.LIST), List.all),
                CallbackQueryHandler(List.delete, pass_user_data=True, pattern="delete/"),
                CallbackQueryHandler(List.pagination, pass_user_data=True, pattern="page/"),
            ],
            states={
                Consts.STATES.NEW_USER: [
                    MessageHandler(Filters.regex(r"^(?:[1-9]\d*(?:\.\d+)?|0\.0*[1-9]\d*)$"), TGUser.show_per_page)
                ],
                Consts.STATES.LIST: [
                    CommandHandler('buttons', TGUser.buttons),
                    MessageHandler(Filters.regex(Consts.BUTTONS.ADD), AddLink.on_new),
                    MessageHandler(Filters.regex(Consts.BUTTONS.LIST), List.all),
                    CallbackQueryHandler(List.delete, pass_user_data=True, pattern="delete/"),
                    CallbackQueryHandler(List.pagination, pass_user_data=True, pattern="page/"),
                ],
                Consts.STATES.ADD_LINK: [
                    MessageHandler(Filters.regex(Consts.BUTTONS.CANCEL), AddLink.on_cancel),
                    MessageHandler(Filters.text, AddLink.on_link),
                ],
                Consts.STATES.DOWNLOADER: [

                ]
            },
            fallbacks=[],
        )

        dispatcher.add_handler(control_handler)
        updater.start_polling()
        updater.idle()

    else:
        while True:
            sleep(1000)


if __name__ == '__main__':
    main()
