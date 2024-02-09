import sqlite3


def update_info(table_name: str, column: str, new_data, where_name: str, where_text: str):
    """Функция обновляет данные в базе данных\n
       • table_name [str] - название таблицы
       • column [str] - название столбца
       • new_data [str / int] - новые данные для указанного столбца
       • where_name [str] - название стоблца, для формирования условия сортировки
       • where_text [str] - значения столбца, для формирования условия сортировки
    """
    try:
        con = sqlite3.connect("./data/config.db") # при ошибке - заменить с абсолютный путь
        cur = con.cursor()
        cur.execute(f"UPDATE {table_name} SET {column}='{new_data}' WHERE {where_name}='{where_text}'")
        con.commit()
        cur.close()
        con.close()
        return {'result': True}
    except:
        return {'result': False}