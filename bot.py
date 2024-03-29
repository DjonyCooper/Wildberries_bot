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
from functions.generation_table_all_users import gen_table

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
    send_message_step_one = State()
    send_message_step_two = State()


class DelInfo(StatesGroup):
    article_number = State()


# ���ҧ�ѧҧ��ܧ� �է֧ۧ��ӧڧ� �ܧ�ާѧߧէ� "/start"
@dp.message_handler(commands=["start"])
async def start(message):
    check_user = read_info(column='*',
                           table='users',
                           where_text=f'mess_id="{message.from_user.id}"')
    main_photo = open('image/start_logo.jpg', 'rb')
    if not check_user:
        create = create_new_user(telegram_id=message.from_user.id,
                                 full_name=message.from_user.full_name)
        if create['result']:
            await bot.send_photo(message.from_user.id, main_photo)
            await bot.send_message(message.chat.id,
                                   text=emoji.emojize(':handshake: ����ڧӧ֧�! �� ���٧էѧ�, ����ҧ� ���ާ��� ��֧ҧ�'
                                                      ' �� ����ݧ֧اڧӧѧߧڧ֧� ��ܧڧէ�� �ߧ� Wildberries.ru\n '
                                                      ':backhand_index_pointing_right: ����ݧ� �ӧ� �٧է֧�� '
                                                      '�ӧ�֧�ӧ���, :red_exclamation_mark: ��֧ܧ�ާ֧ߧէ�֧� '
                                                      '��٧ߧѧܧ�ާڧ���� �� ���ѧӧڧݧѧާ� �ڧ���ݧ�٧�ӧѧߧڧ�\n '
                                                      ':backhand_index_pointing_right: ����ڧ��ߧ��� ���ѧ� '
                                                      '���ܧ���� �� �ާ��� $�ܧڧէ��! :face_blowing_a_kiss:'),
                                   reply_markup=start_keyboard.user_keyboard())
        else:
            await bot.send_message(message.chat.id,
                                   text='�����ڧ٧��ݧ� �ߧ֧���֧է֧ݧ֧ߧߧѧ� ���ڧҧܧ�, ������ҧ�ۧ�� ���٧ا� �ڧݧ� ��ӧ�اڧ�֧�� �� ��֧�. ���էէ֧�اܧ��')
    else:
        user_group = check_user[0][3]
        if user_group == 'dev':
            await bot.send_photo(message.from_user.id, main_photo)
            await bot.send_message(message.chat.id,
                                   text=emoji.emojize(
                                       ':handshake: "���� ����֧�ߧ� �ڧߧڧ�ڧѧݧڧ٧ڧ��ӧѧߧ� �ҧ����!\n�������� �� ���ӧ���֧ߧߧ��ާ� ���ѧӧѧާ�!'),
                                   reply_markup=start_keyboard.dev_keyboard())
        elif user_group == 'user':
            await bot.send_photo(message.from_user.id, main_photo)
            await bot.send_message(message.from_user.id,
                                   text="���� ����֧�ߧ� �ڧߧڧ�ڧѧݧڧ٧ڧ��ӧѧߧ� �ҧ����!\n����ڧ��ߧ��� ���ѧ� ���ܧ���� �� �ާ��� $�ܧڧէ��! ",
                                   reply_markup=start_keyboard.user_keyboard())
        else:
            await bot.send_message(message.from_user.id,
                                   text="�������� �� �ҧ��� �٧ѧ��֧�֧�. ����է��ҧߧ���� �����ߧ�ۧ�� �� ��֧�. ���էէ֧�اܧ�")


@dp.message_handler(content_types=['text'])
async def get_text_messages(message):
    check_user = read_info(column='*',
                           table='users',
                           where_text=f'mess_id="{message.from_user.id}"')
    user_group = check_user[0][3]
    if message.text == emoji.emojize(':plus: ����ҧѧӧڧ��'):
        await bot.send_message(message.from_user.id,
                               "������ѧӧ��� �ާߧ� �ѧ��ڧܧ�� ���٧ڧ�ڧ�, ��֧ߧ� �ܧ������ �ӧ� ����ڧ�� ����ݧ֧اڧӧѧ��:")
        await SaveInfo.article_number.set()

    elif message.text == emoji.emojize(':heavy_dollar_sign: ����ڧ��� �ާ�ڧ� ����֧ݧ�� :heavy_dollar_sign:'):
        info = read_info(column='*',
                         table='users_info',
                         where_text=f'mess_id="{message.from_user.id}"')
        if info:
            message_text = '����� ���ڧ��� ���٧ڧ�ڧ�, �٧� �ڧ٧ާ֧ߧ֧ߧڧ֧� ��֧� �ܧ�������, �ާ� ��ݧ֧էڧ� �էݧ� ���ѧ�:\n\n'
            for item in info:
                message_text += emoji.emojize(
                    f':backhand_index_pointing_right: �����ڧܧ��: {str(item[1])} ���֧ߧ�: {str(item[4])} \n '
                    f'{str(item[2])} \n')
            await bot.send_message(message.from_user.id, message_text)
        else:
            await bot.send_message(message.from_user.id,
                                   "�� ���ѧ� ���ܧ� �ߧ֧� �ߧ� ��էߧ�� ���٧ڧ�ڧ�, �է�ҧѧӧ��� ��֧�ӧ�� ��� �ܧݧڧܧ� �ߧ� �ܧߧ��ܧ� '����ҧѧӧڧ��'")

    elif message.text == emoji.emojize(':minus: ���էѧݧڧ��'):
        await bot.send_message(message.from_user.id, "������ѧӧ��� �ާߧ� �ѧ��ڧܧ�� ���٧ڧ�ڧ�, �ܧ������� �ӧ� ����ڧ�� ��էѧݧڧ��:")
        await DelInfo.article_number.set()

    elif message.text == "����ѧӧڧݧ� ��ѧҧ��� �ҧ���":
        rules_photo = open('image/rules_logo.jpg', 'rb')
        rules_text = emoji.emojize(
            "����ߧ�ӧߧ�� ���ѧӧڧݧ� �ߧѧ�֧ԧ� �ܧݧ�ҧ�: �ӧ�֧� �� �ӧ֧٧է� ����ҧ�ѧۧ�� �� �ߧѧ�֧� �ܧݧ�ҧ�! :winking_face:\n"
            "�� �ҧ��� ���֧է��ѧӧݧ֧ߧ� �ߧ֧�ܧ�ݧ�ܧ� ���ߧܧ�ڧ�ߧѧݧ�ߧ��� �ܧߧ����:\n"
            ":plus: <b>����ҧѧӧڧ��</b> - <i>�էѧ֧� �ӧ�٧ާ�اߧ���� �է�ҧѧӧڧ�� �� ��ڧ��֧ާ� �ѧ��ڧܧ�� �ڧߧ�֧�֧����֧� �ӧѧ� ���٧ڧ�ڧ� �ڧ� "
            "Wildberries �٧� ��֧ߧ�� �ܧ������, �ӧѧ� ����֧ݧ��� �ҧ� ��ݧ֧էڧ��.</i>\n"
            ":minus: <b>���էѧݧڧ��</b> - <i>�էѧ֧� �ӧ�٧ާ�اߧ���� ��էѧݧڧ�� ���٧ڧ�ڧ�, ��֧ߧ� �ܧ������ �ӧѧ� �ҧ�ݧ֧� �ߧ� �ڧߧ�֧�֧��֧�.</i>\n"
            ":heavy_dollar_sign: <b>����ڧ��� ����֧ݧ��</b> - <i>���ܧѧ٧��ӧѧ֧� �ӧ�� ���٧ڧ�ڧ�, ��֧ߧ� �ܧ�������, �ӧ� ��֧ۧ�ѧ� "
            "����ݧ֧اڧӧѧ֧��.</i>\n ����ڧ��ߧ�ԧ� �� ����է�ܧ�ڧӧߧ�ԧ� ���ݧ�٧�ӧѧߧڧ�!\nC ���. �ܧ�ާѧߧէ� ��ѧ٧�ѧҧ��ܧ� :man_technologist:!")
        await bot.send_photo(message.from_user.id, rules_photo, caption=rules_text, parse_mode='html')

    elif message.text == emoji.emojize(':man_technologist: ���ѧߧ֧ݧ� ����ѧӧݧ֧ߧڧ�'):
        if user_group == 'dev':
            await bot.send_message(message.chat.id,
                                   text=emoji.emojize(':play_button: ���֧�֧��� �� ��ѧ٧է֧�: ���ѧߧ֧ݧ� ����ѧӧݧ֧ߧڧ�'),
                                   reply_markup=adm_panel_keyboard.dev_keyboard())
        else:
            await bot.send_message(message.chat.id,
                                   text=emoji.emojize('�������� �٧ѧ��֧�֧�!'))

    elif message.text == "����ڧ��� ���ݧ�٧�ӧѧ�֧ݧ֧�":
        if user_group == 'dev':
            all_user_info = read_info(column='*',
                                      table='users')
            table_all_users = gen_table(all_user_list=all_user_info)
            await bot.send_message(message.chat.id,
                                   text=table_all_users)
        else:
            await bot.send_message(message.chat.id,
                                   text=emoji.emojize('�������� �٧ѧ��֧�֧�!'))

    elif message.text == "������ѧӧڧ�� ����ҧ�֧ߧڧ�":
        if user_group == 'dev':
            info_user = read_info(column='*',
                                  table='users',
                                  where_text='NOT user_group="dev"')
            markup = types.InlineKeyboardMarkup(row_width=1)
            for item in info_user:
                telegram_id = item[1]
                name = item[2]
                markup.insert(
                    types.InlineKeyboardButton(text=name, callback_data=telegram_id))
            markup.add(types.InlineKeyboardButton(f"����ާ֧ߧ�", callback_data='no'))
            await bot.send_message(message.chat.id,
                                   text='�����ҧ֧�ڧ��, �ܧ�ާ� ����ڧ�� �����ѧӧڧ�� ����ҧ�֧ߧڧ�?',
                                   reply_markup=markup)
            await SaveInfo.send_message_step_one.set()
        else:
            await bot.send_message(message.chat.id,
                                   text='�������� �٧ѧ��֧�֧�!')

    elif message.text == emoji.emojize(":BACK_arrow: ���֧�ߧ����� �� �ԧݧѧӧߧ�� �ާ֧ߧ�"):
        if user_group == 'dev':
            await bot.send_message(message.chat.id,
                                   text=emoji.emojize(
                                       ':play_button: ���֧�֧��� �� ��ѧ٧է֧�: ���ݧѧӧߧ�� �ާ֧ߧ�\n�������� �� ���ӧ���֧ߧߧ��ާ� ���ѧӧѧާ�!'),
                                   reply_markup=start_keyboard.dev_keyboard())
        elif user_group == 'user':
            await bot.send_message(message.from_user.id,
                                   text=emoji.emojize(':play_button: ���֧�֧��� �� ��ѧ٧է֧�: ���ݧѧӧߧ�� �ާ֧ߧ�'),
                                   reply_markup=start_keyboard.user_keyboard())
        else:
            await bot.send_message(message.from_user.id,
                                   text="�������� �� �ҧ��� �٧ѧ��֧�֧�. ����է��ҧߧ���� �����ߧ�ۧ�� �� ��֧�. ���էէ֧�اܧ�")


# ���ҧ�ѧҧ��ܧ� �է֧ۧ��ӧڧ� �ܧߧ��ܧ� "����ҧѧӧڧ��"
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
                msg_text += emoji.emojize(f"�����.: {prod_info[0]}\t\t\t\t:money_bag: {prod_info[2]} ����.\n"
                                          f"<b>{prod_info[1]}</b>\n\n"
                                          f"���� �ߧѧ�ѧݧ� ����ݧ֧اڧӧѧ�� ��֧ߧ� ����ԧ� ���ӧѧ��!\n")
                if prod_info[3] != '':
                    await bot.send_photo(message.from_user.id, photo=prod_info[3], caption=msg_text,
                                         parse_mode='html')
                else:
                    await bot.send_message(message.from_user.id, msg_text, parse_mode='html')
            else:
                await bot.send_message(message.from_user.id,
                                       '�����, �����ا� ����� �ѧ��ڧܧ�� �ާ� ��ا� ����ݧ֧اڧӧѧ֧�! �����ӧ֧���� ���ڧ��� ����֧ݧ�� :)')
        else:
            msg_text += emoji.emojize(f":speaking_head: ���� �ߧ� ��ާ�ԧݧ� �ߧѧۧ�� ���ӧѧ� �� ���ڧ� �ѧ��ڧܧ�ݧ��")
            await bot.send_message(message.from_user.id, msg_text, parse_mode='html')
    await state.finish()


# ���ҧ�ѧҧ��ܧ� �է֧ۧ��ӧڧ� �ܧߧ��ܧ� "���էѧݧڧ��"
@dp.message_handler(state=DelInfo.article_number)
async def func_add_article(message: types.Message, state: FSMContext):
    async with state.proxy():
        article_number = message.text
        try:
            value_article = int(article_number)
            delete = delete_prod(table='users_info',
                                 where_text=f'article_number="{value_article}"')
            if delete['result']:
                await bot.send_message(message.from_user.id, f"�����ڧܧ�� {value_article} - ����֧�ߧ� ��էѧݧ֧�!")
            else:
                await bot.send_message(message.from_user.id,
                                       f"���ӧ֧է֧ߧߧ��� ���ѧާ� �ѧ��ڧܧ�� {value_article} - �ߧ� �ߧѧۧէ֧�. �����ӧ֧���� �էѧߧߧ��� �� "
                                       f"������ҧ�ۧ�� ��ߧ�ӧ�.")
        except ValueError:
            await bot.send_message(message.from_user.id,
                                   f"���ѧէѧߧߧ��� ���ѧާ� �ѧ��ڧܧ�� {article_number} - �ߧ� �ܧ���֧ܧ�֧�! �����ӧ֧���� �էѧߧߧ��� ��"
                                   f" ������ҧ�ۧ�� ��ߧ�ӧ�.")
    await state.finish()


# ���ҧ�ѧҧ��ܧ� �է֧ۧ��ӧڧ� �ܧߧ��ܧ� "������ѧӧڧ�� ����ҧ�֧ߧڧ�" (�ݧ�ӧڧ� callback �� �ܧߧ��ܧ� �ӧ��ҧ��� ���ݧ�٧�ӧѧ�֧ݧ�)
@dp.callback_query_handler(state=SaveInfo.send_message_step_one)
async def send_message_step_one_callback(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as user_info:
        try:
            await callback_query.message.delete()
        except:
            pass
        finally:
            if callback_query.data == 'no':
                await bot.send_message(callback_query.from_user.id,
                                       emoji.emojize(':speaking_head: �����֧�� ���֧�ӧѧ� ���ݧ�٧�ӧѧ�֧ݧ֧�.'))
                await state.finish()
            else:
                user_info['id'] = callback_query.data
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton(text='����ާ֧ߧ�', callback_data="no"))
                await bot.send_message(callback_query.from_user.id,
                                       text=f"���ѧ�ڧ�ڧ�� ����ҧ�֧ߧڧ�, �ܧ������ ����ڧ�� �����ѧӧڧ�� ���ݧ�٧�ӧѧ�֧ݧ� �� ID: {user_info['id']} �ڧݧ� �ߧѧاާڧ�� ����ާ֧ߧ�",
                                       reply_markup=markup)
                await state.finish()
                await SaveInfo.send_message_step_two.set()


# ���ҧ�ѧҧ��ܧ� �է֧ۧ��ӧڧ� �ܧߧ��ܧ� "������ѧӧڧ�� ����ҧ�֧ߧڧ�" (�ݧ�ӧڧ� message - ���֧���ӧѧ֧� �����֧��)
@dp.message_handler(state=SaveInfo.send_message_step_one)
async def send_message_step_one_msg(message: types.Message, state: FSMContext):
    async with state.proxy():
        try:
            await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
        except:
            pass
        finally:
            await bot.send_message(message.chat.id,
                                   emoji.emojize(':speaking_head: �����֧�� ���֧�ӧѧ�, ��.��. ���ݧ��֧ߧ� �ߧ֧ܧ���֧ܧ�ߧ��� �էѧߧߧ���.'))
            await state.finish()


# ���ҧ�ѧҧ��ܧ� �է֧ۧ��ӧڧ� �ܧߧ��ܧ� "������ѧӧڧ�� ����ҧ�֧ߧڧ�" (�ݧ�ӧڧ� message �էݧ� ���ݧ�٧�ӧѧ�֧ݧ� - �����ѧӧݧ�֧� ����ҧ�֧ߧڧ� ���ݧ�٧�ӧѧ�֧ݧ�)
@dp.message_handler(state=SaveInfo.send_message_step_two)
async def send_message_step_two_msg(message: types.Message, state: FSMContext):
    async with state.proxy() as user_info :
        try:
            await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
        except:
            pass
        finally:
            telegram_id = user_info['id']
            msg = f'�����ҧ�֧ߧڧ� ��� ��֧�. ���էէ֧�اܧ� �ҧ���:\n{message.text}'
            if telegram_id != '' and msg != '':
                await bot.send_message(telegram_id, text=msg)
                await bot.send_message(message.chat.id,
                                       emoji.emojize(f':speaking_head: ���ѧ�� ����ҧ�֧ߧڧ� ����֧�ߧ� �����ѧӧݧ֧ߧ� ���ݧ�٧�ӧѧ�֧ݧ� c ID: {telegram_id}.'))
            else:
                await bot.send_message(message.chat.id,
                                       emoji.emojize(f':speaking_head: ������ѧӧܧ� ����ҧ�֧ߧڧ� ���ݧ�٧�ӧѧ�֧ݧ� c ID: {telegram_id} �ߧ� �ӧ����ݧߧ֧ߧ�, ��.��. �ߧ� �ҧ��ݧ� ���ݧ��֧ߧ� �ӧ�� �ߧ֧�ҧ��էڧާ��� �էݧ� ����ԧ� �էѧߧߧ���'))
            await state.finish()


# ���ҧ�ѧҧ��ܧ� �է֧ۧ��ӧڧ� �ܧߧ��ܧ� "������ѧӧڧ�� ����ҧ�֧ߧڧ�" (�ݧ�ӧڧ� callback �ܧߧ��ܧ� ����ާ֧ߧ�)
@dp.callback_query_handler(state=SaveInfo.send_message_step_two)
async def send_message_step_two_callback(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy():
        await callback_query.message.delete()
        if callback_query.data == 'no':
            await bot.send_message(callback_query.from_user.id,
                                   emoji.emojize(':speaking_head: �����֧�� ���֧�ӧѧ� ���ݧ�٧�ӧѧ�֧ݧ֧�.'))
            await state.finish()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
