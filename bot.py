# coding=gbk
import asyncio
import emoji
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import urllib3
import locale
import configparser

import parser_pages

from functions.crud.create import create_new_prod, create_new_user
from functions.crud.delete import delete_prod
from functions.crud.read import read_info

from view.keyboards import start_keyboard, adm_panel_keyboard

locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian")

urllib3.disable_warnings()
logging.basicConfig(level=logging.INFO)
config = configparser.ConfigParser()
config.read("./settings.ini")

bot = Bot(token=config["bot"]["token"])

dp = Dispatcher(bot, storage=MemoryStorage())


class SaveInfo(StatesGroup):
    article_number = State()
    size = State()


class DelInfo(StatesGroup):
    article_number = State()


# Обработка действий команды "/start"
@dp.message_handler(commands=["start"])
async def start(message):
    check_user = read_info(column='*',
                           table='users',
                           where_text=f'mess_id="{message.from_user.id}"')
    user_group = check_user[0][3]
    main_photo = open('image/start_logo.jpg', 'rb')

    if not check_user:
        create = create_new_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name)
        if create['result']:
            if user_group == 'user':
                await bot.send_photo(message.from_user.id, main_photo)
                await bot.send_message(message.chat.id, text=emoji.emojize(':handshake: Привет! Я создан, чтобы помочь тебе'
                                                                           ' с отслеживанием скидок на Wildberries.ru\n '
                                                                           ':backhand_index_pointing_right: Если вы здесь '
                                                                           'впервые, :red_exclamation_mark: рекомендуем '
                                                                           'ознакомиться с правилами использования\n '
                                                                           ':backhand_index_pointing_right: Приятных Вам '
                                                                           'покупок и море $кидок! :face_blowing_a_kiss:'),
                                       reply_markup=start_keyboard.user_keyboard())
            elif user_group == 'dev':
                await bot.send_photo(message.from_user.id, main_photo)
                await bot.send_message(message.chat.id,
                                       text=emoji.emojize(':handshake: Привет разработчик!'),
                                       reply_markup=start_keyboard.dev_keyboard())
        else:
            await bot.send_message(message.chat.id,
                                   text='Произошла неопределенная ошибка, попробуйте позже или свяжитесь с тех. поддержкой')
    elif user_group == 'dev':
        await bot.send_photo(message.from_user.id, main_photo)
        await bot.send_message(message.chat.id,
                               text=emoji.emojize(':handshake: "Вы успешно инициализированы ботом!\nДоступ с повышенными правами!'),
                               reply_markup=start_keyboard.dev_keyboard())
    elif user_group == 'user':
        await bot.send_photo(message.from_user.id, main_photo)
        await bot.send_message(message.from_user.id,
                               text="Вы успешно инициализированы ботом!\nПриятных Вам покупок и море $кидок! ",
                               reply_markup=start_keyboard.user_keyboard())
    else:
        await bot.send_message(message.from_user.id,
                               text="Доступ в бота запрещен. Подробности уточняйте в тех. поддержке")


@dp.message_handler(content_types=['text'])
async def get_text_messages(message):
    check_user = read_info(column='*',
                           table='users',
                           where_text=f'mess_id="{message.from_user.id}"')
    user_group = check_user[0][3]
    if message.text == emoji.emojize(':plus:') + " Добавить":
        await bot.send_message(message.from_user.id,
                               "Отправьте мне артикул позиции, цену которой вы хотите отслеживать:")
        await SaveInfo.article_number.set()

    elif message.text == emoji.emojize(':heavy_dollar_sign:') + " Список моих хотелок " + emoji.emojize(
            ':heavy_dollar_sign:'):
        info = read_info(column='*',
                         table='users_info',
                         where_text=f'mess_id="{message.from_user.id}"')
        if info:
            message_text = 'Это список позиций, за изменением цен которых, мы следим для Вас:\n\n'
            for item in info:
                message_text += emoji.emojize(
                    f':backhand_index_pointing_right: Артикул: {str(item[1])} Цена: {str(item[4])} \n '
                    f'{str(item[2])} \n')
            await bot.send_message(message.from_user.id, message_text)
        else:
            await bot.send_message(message.from_user.id,
                                   "У Вас пока нет не одной позиции, добавьте первую по клику на кнопку 'Добавить'")
    elif message.text == emoji.emojize(':minus:') + " Удалить":
        await bot.send_message(message.from_user.id, "Отправьте мне артикул позиции, который вы хотите удалить:")
        await DelInfo.article_number.set()
    elif message.text == "Правила работы бота":
        rules_photo = open('image/rules_logo.jpg', 'rb')
        rules_text = emoji.emojize(
            "Основное правило нашего клуба: всем и везде сообщайте о нашем клубе! :winking_face:\n"
            "В боте представлено несколько функциональных кнопок:\n"
            ":plus: <b>Добавить</b> - <i>дает возможность добавить в систему артикул интересующей вас позиции из "
            "Wildberries за ценой которой, вам хотелось бы следить.</i>\n"
            ":minus: <b>Удалить</b> - <i>дает возможность удалить позицию, цена которой вас более не интересует.</i>\n"
            ":heavy_dollar_sign: <b>Список хотелок</b> - <i>показывает все позиции, цену которых, вы сейчас "
            "отслеживаете.</i>\n Приятного и продуктивного пользования!\nC ув. команда разработки :man_technologist:!")
        await bot.send_photo(message.from_user.id, rules_photo, caption=rules_text, parse_mode='html')
    elif message.text == emoji.emojize(':man_technologist: Панель управления'):
        if user_group == 'dev':
            await bot.send_message(message.chat.id,
                                   text=emoji.emojize(':play_button: Переход в раздел: Панель управления'),
                                   reply_markup=adm_panel_keyboard.dev_keyboard())
        else:
            await bot.send_message(message.chat.id,
                                   text=emoji.emojize('Доступ запрещен!'))
    elif message.text == emoji.emojize(":BACK_arrow: Вернуться в главное меню"):
        if user_group == 'dev':
            await bot.send_message(message.chat.id,
                                   text=emoji.emojize(':play_button: Переход в раздел: Главное меню\nДоступ с повышенными правами!'),
                                   reply_markup=start_keyboard.dev_keyboard())
        elif user_group == 'user':
            await bot.send_message(message.from_user.id,
                                   text=emoji.emojize(':play_button: Переход в раздел: Главное меню'),
                                   reply_markup=start_keyboard.user_keyboard())
        else:
            await bot.send_message(message.from_user.id,
                                   text="Доступ в бота запрещен. Подробности уточняйте в тех. поддержке")



# Обработка действий кнопки "Добавить"
@dp.message_handler(state=SaveInfo.article_number)
async def func_add_article(message: types.Message, state: FSMContext):
    async with state.proxy():
        article_number = message.text
        prod_info = parser_pages.search_prod(article_number)
        msg_text = ''
        if prod_info:
            create = create_new_prod(telegram_id=message.from_user.id,
                                     prod_info=prod_info)
            if create['result']:
                msg_text += emoji.emojize(f"Арт.: {prod_info[0]}\t\t\t\t:money_bag: {prod_info[2]} руб.\n"
                                          f"<b>{prod_info[1]}</b>\n\n"
                                          f"Мы начали отслеживать цену этого товара!\n")
                if prod_info[3] != '':
                    await bot.send_photo(message.from_user.id, photo=prod_info[3], caption=msg_text,
                                         parse_mode='html')
                else:
                    await bot.send_message(message.from_user.id, msg_text, parse_mode='html')
            else:
                await bot.send_message(message.from_user.id,
                                       'Упс, похоже этот артикул мы уже отслеживаем! Проверьте список хотелок :)')
        else:
            msg_text += emoji.emojize(f":speaking_head: Мы не смогли найти товар с этим артикулом")
            await bot.send_message(message.from_user.id, msg_text, parse_mode='html')
    await state.finish()


# Обработка действий кнопки "Удалить"
@dp.message_handler(state=DelInfo.article_number)
async def func_add_article(message: types.Message, state: FSMContext):
    async with state.proxy():
        article_number = message.text
        try:
            value_article = int(article_number)
            delete = delete_prod(table='users_info',
                                 where_text=f'article_number="{value_article}"')
            if delete['result']:
                await bot.send_message(message.from_user.id, f"Артикул {value_article} - успешно удален!")
            else:
                await bot.send_message(message.from_user.id,
                                       f"Введенный Вами артикул {value_article} - не найден. Проверьте данные и "
                                       f"попробуйте снова.")
        except ValueError:
            await bot.send_message(message.from_user.id,
                                   f"Заданный Вами артикул {article_number} - не корректен! Проверьте данные и"
                                   f" попробуйте снова.")
    await state.finish()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
