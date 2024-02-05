import datetime
import sqlite3
from parser_pages import parse_page
import requests
import emoji
import schedule

def checker():
    print(f"checker - started в {datetime.datetime.now()}")
    con = sqlite3.connect('data/config.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM users_info")
    all_info_sql = cur.fetchall()
    msg_text = ''
    for item in all_info_sql:
        article = item[1]
        old_price = item[4]
        now_price = 0
        if item[5] != None:
            all_info = search_prod.search_prod_size(str(item[5]), str(article))
            now_price = all_info[3]
        else:
            all_info = search_prod.search_prod(str(article))
            now_price = all_info[2]

        if int(now_price) < int(old_price):
            URL_MSG = f"https://api.telegram.org/bot6152475270:AAHO70SZ2hlajDYsUuTdln8v-EO_-l5DlJc/sendMessage"
            URL_PHOTO = f"https://api.telegram.org/bot6152475270:AAHO70SZ2hlajDYsUuTdln8v-EO_-l5DlJc/sendPhoto"
            msg_text += emoji.emojize(f"Арт.: {all_info[0]}\t\t\t\t:money_bag: {old_price} руб.\n"
                                    f"<b>{all_info[1]}</b>\n\n"
                                    f"Цена снизилась до: {now_price} руб. пора брать!\n")
            if all_info[3] == '':
                data = {"chat_id": item[0], "text": msg_text, "parse_mode": 'html'}
                requests.post(URL_MSG, data=data)
            else:
                data = {"chat_id": item[0], "photo": all_info[3], "caption": msg_text, "parse_mode": 'html'}
                requests.post(URL_PHOTO, data=data)
            cur.execute(f'UPDATE users_info SET article_price="{now_price}" WHERE article_number={article}')
            con.commit()
    cur.close()
    con.close()
    print(f"checker - finished в {datetime.datetime.now()}")


schedule.every(15).minutes.do(checker)
print(f"Утилита успешно запущена в {datetime.datetime.now()}!")
while True:
    schedule.run_pending()

