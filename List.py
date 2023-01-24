import DataBase
import Consts
import math
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def all(update, context):
    __show_list(update, context)
    return Consts.STATES.LIST


def pagination(update, context):
    __show_list(update, context, int(update.callback_query.data.split('/')[1]))
    return Consts.STATES.LIST


def __show_list(update, context, page=0):
    __delete_messages(update, context)

    db = DataBase.init()

    links = db.get_chat_id_feed_paged(update.effective_chat.id, page)

    message_ids = []

    for link in links:
        keyboard = [[
            InlineKeyboardButton('Удалить', callback_data=f"delete/{link[0]}"),
            InlineKeyboardButton('Перейти', url=link[2]),
        ], ]
        message = context.bot.send_message(
            update.effective_chat.id,
            text=F"{link[3]}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        message_ids.append(str(message.message_id))

    count = db.get_chat_id_feed_count(update.effective_chat.id)
    user = db.get_tg_user_by_chat_id(update.effective_chat.id)

    # pagination
    pages = math.ceil(count / int(user[1]))

    if pages > 1:
        pagination_buttons = []
        for index in range(pages):
            pagination_buttons.append(InlineKeyboardButton(f"{index + 1}", callback_data=f"page/{index}"), )

        message = context.bot.send_message(
            update.effective_chat.id,
            text='Страницы',
            reply_markup=InlineKeyboardMarkup([pagination_buttons])
        )
        message_ids.append(str(message.message_id))

    message_ids = ';'.join(message_ids)

    db.update_tg_user_last_messages(update.effective_chat.id, message_ids)


def delete(update, context):
    db = DataBase.init()
    db.remove_link_from_feed(update.effective_chat.id, update.callback_query.data.split('/')[1])

    __show_list(update, context)
    return Consts.STATES.LIST


def __delete_messages(update, context):
    db = DataBase.init()
    user = db.get_tg_user_by_chat_id(update.effective_chat.id)
    if user is None:
        return

    if user[2] is None:
        return

    messages = user[2].split(';')

    if len(messages) == 0:
        return

    for index in range(len(messages)):
        try:
            context.bot.deleteMessage(
                update.effective_chat.id,
                messages.pop(0),
            )
        except Exception:
            pass
