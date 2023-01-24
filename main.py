import DataBase
import Consts
import TGUser
import AddLink
import os
from dotenv import load_dotenv
from telegram.ext import Updater, ConversationHandler, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

load_dotenv()


def main():
    DataBase.init().init_database()

    updater = Updater(os.getenv('TOKEN', default=None), use_context=True)
    dispatcher = updater.dispatcher

    control_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', TGUser.start),
            CommandHandler('buttons', TGUser.buttons),
        ],
        states={
            Consts.STATES.NEW_USER: [
                MessageHandler(Filters.regex(r"^(?:[1-9]\d*(?:\.\d+)?|0\.0*[1-9]\d*)$"), TGUser.show_per_page)
            ],
            Consts.STATES.BUTTONS: [

            ],
            Consts.STATES.LIST: [
                CommandHandler('buttons', TGUser.buttons),
            ],
            Consts.STATES.ADD_LINK: [

            ],
            Consts.STATES.DOWNLOADER: [

            ]
        },
        fallbacks=[],
    )

    dispatcher.add_handler(control_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
