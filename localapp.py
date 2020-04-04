import threading
import time
from handyfunctions import *
from plyer import notification


class myGame(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.board = 1

    def run(self):
        while True:
            print("----------------------game running----------------------")
            time.sleep(4)
            try:
                json_response = get_dict_with_param(lang="FR_DE")
                print(json_response)
                notification.notify(
                    title='id: {0}'.format(json_response[0]["id"]),
                    message='content: {0}'.format(json_response[0]["line"]),
                    app_icon=None,  # e.g. 'C:\\icon_32x32.ico'
                    timeout=5,  # seconds
                )
            except:
                print('error: get_dict_with_param(lang="FR_DE")')
        pass