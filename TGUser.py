import Consts
import DataBase
from telegram import ReplyKeyboardMarkup


def start(update, context):
    context.bot.send_message(
        update.effective_chat.id,
        text="Здравствуй!\n\n"
             "Так как это наше первое знакомство, давайте проведем некоторые настройки",
    )
    context.bot.send_message(
        update.effective_chat.id,
        text="Начнем с пагинации\n\n"
             "Введите число, которое будет является количеством ссылок на одной странице",
    )
    return Consts.STATES.NEW_USER


def show_per_page(update, context):
    DataBase.init().insert_tg_user(update.effective_chat.id, update.message.text)

    __reply_keyboard = [
        [Consts.BUTTONS.LIST, Consts.BUTTONS.ADD],
    ]

    context.bot.send_message(
        update.effective_chat.id,
        text=f"Отлично! \n\n"
             "Настройки завершены",
        reply_markup=ReplyKeyboardMarkup(__reply_keyboard, resize_keyboard=True, one_time_keyboard=False)
    )

    return Consts.STATES.LIST


def buttons(update, context):
    __reply_keyboard = [
        [Consts.BUTTONS.LIST, Consts.BUTTONS.ADD],
    ]

    context.bot.send_message(
        update.effective_chat.id,
        text=f"Оуу! Похоже вы потеряли кнопки управления. Исправляем это недоразумение",
        reply_markup=ReplyKeyboardMarkup(__reply_keyboard, resize_keyboard=True, one_time_keyboard=False)
    )

    return Consts.STATES.LIST
