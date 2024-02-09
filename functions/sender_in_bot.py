import configparser
import requests

config = configparser.ConfigParser()
config.read("./settings.ini") # при ошибке - заменить с абсолютный путь

TOKEN = config['bot']['token']
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
def send_message(telegram_id: int, msg_text: str):
    """Функция для отправки сообщения пользователю в бота. Вернется True - если отправка успешна, False - произошла
    ошибка (часто причиной является блокировка и (или) удаление бота пользователем)\n
           • telegram_id [int] - пользовательский идентификатор в телеграм
           • msg_text [str] - текст сообщения для пользователя
    """
    try:
        data = {'chat_id': telegram_id, 'text': msg_text}
        requests.post(URL, data=data)
        return {'result': True}
    except:
        return {'result': False}