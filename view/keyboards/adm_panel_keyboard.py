from aiogram import types
import emoji

def dev_keyboard():
    markup_dev = types.ReplyKeyboardMarkup(resize_keyboard=True)

    but_view_all_user = types.KeyboardButton("Список пользователей")
    but_back = types.KeyboardButton(text=emoji.emojize(":BACK_arrow: Вернуться в главное меню"))

    markup_dev.row(but_view_all_user)
    markup_dev.row(but_back)

    return markup_dev