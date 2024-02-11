import sqlite3


def read_info(column: str, table: str, where_text: str = None):
    """Функция возвращает [(),()...] с данными из базы данных, если их нет - []\n
       • column [str] - название столбца
       • table [str] - название таблицы
       • where [Optional | str] - условие(-я), для сортировки по таблице
    """
    con = sqlite3.connect("./data/config.db") # при ошибке - заменить с абсолютный путь
    cur = con.cursor()
    if where_text is None:
        cur.execute(f'SELECT {column} FROM {table}')
    else:
        cur.execute(f'SELECT {column} FROM {table} WHERE {where_text}')
    info = cur.fetchall()
    return info


