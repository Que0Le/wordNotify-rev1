import threading
import time
from handyfunctions import *
from plyer import notification
from sys import platform
from win10toast import ToastNotifier
import webbrowser
# The other candidate for notification windows is https://github.com/malja/zroya

class myGame(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.board = 1

    def run(self):
        if platform == "linux" or platform == "linux2":
            # linux
            pass
        elif platform == "darwin":
            # OS X
            while True:
                # print("----------------------game running----------------------")
                time.sleep(5)
                try:
                    json_response = get_dict_with_param(lang="FR_DE")
                    print(json_response)
                    # time.sleep(10)
                    notification.notify(
                        title='id: {0}'.format(json_response[0]["id"]),
                        message='content: {0}'.format(json_response[0]["line"]),
                        app_name='wordNotify',
                        # app_icon="beat_brick.ico",  # e.g. 'C:\\icon_32x32.ico'
                        timeout=2,  # seconds
                    )
                except:
                    print('error: get_dict_with_param(lang="FR_DE")')

        elif platform == "win32":
            print("windows")
            def open_browser_tab(url):
                try:
                    webbrowser.open(url, new=0)
                except:
                    print("error opening web")

            toast = ToastNotifier()
            while True:
                # print("----------------------game running----------------------")
                time.sleep(10)
                try:
                    json_response, url_full = get_dict_with_param(lang="FR_DE")
                    print(json_response)
                    # time.sleep(10)
                    toast.show_toast(
                        title='id: {0}'.format(json_response[0]["id"]),
                        msg='content: {0}'.format(json_response[0]["line"]),
                        icon_path=None,
                        duration=5,
                        threaded=False,
                        callback_on_click=(lambda: open_browser_tab(get_dict_with_param(lang="FR_DE", id=json_response[0]["id"], url_only=True))))
                except:
                    print('error: creating toast notification')
            
        pass