import Feed
from telegram import ReplyKeyboardMarkup
import Consts


__control_keyboard = [
        [Consts.BUTTONS.LIST, Consts.BUTTONS.ADD],
    ]

__cancel_keyboard = [
        [Consts.BUTTONS.CANCEL],
    ]


def on_new(update, context):
    context.bot.send_message(
        update.effective_chat.id,
        text=f"Введите ссылку",
        reply_markup=ReplyKeyboardMarkup(__cancel_keyboard, resize_keyboard=True, one_time_keyboard=False)
    )
    return Consts.STATES.ADD_LINK


def on_link(update, context):
    link = update.message.text.split('?')[0]

    Feed.insert_link_to_tg_user(update.effective_chat.id, link)

    context.bot.send_message(
        update.effective_chat.id,
        text=f"Ссылка добавлена. Она появиться в вашем списке через минуту.",
        reply_markup=ReplyKeyboardMarkup(__control_keyboard, resize_keyboard=True, one_time_keyboard=False)
    )

    return Consts.STATES.LIST


def on_cancel(update, context):
    context.bot.send_message(
        update.effective_chat.id,
        text=f"Вы отменили добавление ссылки",
        reply_markup=ReplyKeyboardMarkup(__control_keyboard, resize_keyboard=True, one_time_keyboard=False)
    )

    return Consts.STATES.LIST
