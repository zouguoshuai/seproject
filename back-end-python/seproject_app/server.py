# 导入所需模块
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import os
import sys
import subprocess
import time
import signal

# 定义FastAPI应用程序的路径
APP_PATH = "main.py"


# 定义服务类
class FastAPIService(win32serviceutil.ServiceFramework):
    _svc_name_ = "FastAPIService"
    _svc_display_name_ = "FastAPI Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_running = True

    # 启动服务
    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    # 停止服务
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_running = False

    # 运行主函数
    def main(self):
        while self.is_running:
            # 启动FastAPI应用程序
            self.start_fastapi_app()
            # 检测FastAPI应用程序是否正在运行，如果不在运行则重启
            while self.is_running and self.is_fastapi_app_running():
                time.sleep(5)
            time.sleep(5)

    # 启动FastAPI应用程序
    def start_fastapi_app(self):
        subprocess.Popen([sys.executable, APP_PATH])

    # 检测FastAPI应用程序是否正在运行
    def is_fastapi_app_running(self):
        with subprocess.Popen(["tasklist", "/FI", "IMAGENAME eq python.exe"], stdout=subprocess.PIPE,
                              shell=True, preexec_fn=os.setsid) as proc:
            output = proc.stdout.read().decode('gbk')
            return APP_PATH in output


# 定义服务入口函数
def main():
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(FastAPIService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(FastAPIService)


# 运行服务
if __name__ == '__main__':
    main()
