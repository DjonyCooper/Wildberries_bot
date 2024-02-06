import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sqlite3

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
            con = sqlite3.connect('C:/scripts/sendlerservice/tasks.db')
            cur = con.cursor()
            cur.execute('SELECT * FROM new_tasks WHERE status_task="new"')
            new_tasks = cur.fetchall()
            if new_tasks != []:
                cur.execute(f'UPDATE new_tasks SET status_task="progress"')
                con.commit()
                self.sched()
            else:
                pass
            cur.close()
            con.close()
            time.sleep(30)

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(AppServerSvc)