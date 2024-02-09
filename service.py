import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import logging

import parser_pages
from functions.crud.read import read_info
from functions.crud.update import update_info
from functions.sender_in_bot import send_message

logging.basicConfig(level=logging.INFO, filename="./logs/service.log",filemode="a+", # при ошибке - заменить с абсолютный путь
                    format="%(asctime)s %(levelname)s %(message)s")

class AppServerSvc (win32serviceutil.ServiceFramework):
    _svc_name_ = "WildberriesNotifService"
    _svc_display_name_ = "Сервис для мониторинга и отправки уведомлений о изменении цены на площадке Wildberries"

    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        self.hWaitStop = win32event.CreateEvent(None,0,0,None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                          servicemanager.PYS_SERVICE_STARTED,
                          (self._svc_name_,''))
        self.main()

    def main(self):
        while True:
            self.service_process()
            time.sleep(60)

    def service_process(self):
        check = read_info(column='mess_id, article_number, article_name, article_price',
                          table='users_info')
        for item_check in check:
            telegram_id = item_check[0]
            article_number = item_check[1]
            prod_name = item_check[2]
            now_price = item_check[3]

            prod_info = parser_pages.search_prod(article_number)
            if prod_info != []:
                new_price = prod_info[2]

                if int(new_price) < int(now_price):
                    msg = f'Обрати внимание! Цена на позицию: {prod_name} снижена!\n\nСтарая цена: {now_price}\nНовая цена: {new_price}'
                    result_send = send_message(telegram_id=telegram_id,
                                               msg_text=msg)
                    update_info(table_name='users_info',
                                column='article_price',
                                new_data=new_price,
                                where_name='article_number',
                                where_text=article_number)
                    if result_send == True:
                        logging.info(
                            f'Сообщение о изменении цены успешно доставлено пользователю с telegram_id: {telegram_id}')
                    else:
                        logging.info(
                            f'Сообщение о изменении цены не было доставлено пользователю с telegram_id: {telegram_id}')
                else:
                    pass
            else:
                pass

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)