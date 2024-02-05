from aiogram import types
import emoji

def user_keyboard():
    markup_user = types.ReplyKeyboardMarkup(resize_keyboard=True)

    but_manual = types.KeyboardButton("Правила работы бота")
    but_all_target = types.KeyboardButton(text=emoji.emojize(':heavy_dollar_sign: Список моих хотелок :heavy_dollar_sign:'))
    but_add_search = types.KeyboardButton(text=emoji.emojize(':plus: Добавить'))
    but_del_search = types.KeyboardButton(text=emoji.emojize(':minus: Удалить'))

    markup_user.row(but_all_target)
    markup_user.row(but_add_search, but_del_search)
    markup_user.row(but_manual)

    return markup_user

def dev_keyboard():
    markup_dev = types.ReplyKeyboardMarkup(resize_keyboard=True)

    but_manual = types.KeyboardButton("Правила работы бота")
    but_all_target = types.KeyboardButton(text=emoji.emojize(':heavy_dollar_sign: Список моих хотелок :heavy_dollar_sign:'))
    but_add_search = types.KeyboardButton(text=emoji.emojize(':plus: Добавить'))
    but_del_search = types.KeyboardButton(text=emoji.emojize(':minus: Удалить'))
    but_adm_panel = types.KeyboardButton(text=emoji.emojize(':man_technologist: Панель управления'))

    markup_dev.row(but_all_target)
    markup_dev.row(but_add_search, but_del_search)
    markup_dev.row(but_manual)
    markup_dev.row(but_adm_panel)

    return markup_dev