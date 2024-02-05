import sqlite3
from functions.crud.read import read_info


def delete_prod(table: str, where_text: str = None):
    """Функция возвращает dict где в ['result']: True - удалено успешно, False - не удалено / не чего удалять\n
       • table [str] - название таблицы
       • where [Optional | str] - условие(-я), для сортировки по таблице
    """
    info_in_table = read_info(column='*',
                              table='users_info',
                              where_text=where_text)
    if info_in_table:
        con = sqlite3.connect("data/config.db")
        cur = con.cursor()
        cur.execute(f'DELETE from {table} WHERE {where_text}')
        con.commit()
        cur.close()
        con.close()
        return {'result': True}
    else:
        return {'result': False}

