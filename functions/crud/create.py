import sqlite3

def create_new_user(telegram_id: int, full_name: str):
    try:
        con = sqlite3.connect("data/config.db")
        cur = con.cursor()
        cur.execute(f'INSERT INTO users (mess_id, mess_user_name, user_group) '
                    f'VALUES("{telegram_id}", "{full_name}", "user")')
        con.commit()
        cur.close()
        con.close()
        return {'result': True}
    except:
        return {'result': False}


def create_new_prod(telegram_id: int, prod_info: dict):
    """Функция для добавления нового продукта в базу данных, возвращает dict где в ['result']: True - удалено успешно,
    False - не удалено / не чего удалять\n
           • telegram_id [int] - пользовательский идентификатор в телеграмм
           • prod_info [dict] - словарь с данными для записи в БД
    """
    con = sqlite3.connect('data/config.db')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM users_info WHERE article_number={prod_info[0]};')
    val_prod_info = cur.fetchall()
    if val_prod_info == []:
        if len(prod_info) != 4:
            return {'result': False}
        else:
            cur.execute(
                f'INSERT INTO users_info (mess_id, article_number, article_name, article_href, article_price)'
                f'VALUES("{telegram_id}", "{prod_info[0]}", "{prod_info[1]}", "{prod_info[3]}", "{prod_info[2]}");')
            con.commit()
            cur.close()
            con.close()
            return {'result': True}
    else:
        return {'result': False}