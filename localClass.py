import os, time
import threading, queue
from handyfunctions import *
from plyer import notification
from sys import platform
import webbrowser
# The other candidate for notification windows is https://github.com/malja/zroya
import json

class myGame(threading.Thread):
    def __init__(self, global_config):
        threading.Thread.__init__(self)
        self.daemon = True
        self.global_config = global_config

    def run(self):
        if platform == "linux" or platform == "linux2":
            # linux
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
                    print('error: notify')
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
                    print('error: notify')

        elif platform == "win32":
            from win10toast import ToastNotifier
            def open_browser_tab(url):
                try:
                    webbrowser.open(url, new=0)
                except:
                    print("error opening web")

            toast = ToastNotifier()
            while True:
                print("----------------------game running----------------------")
                print("interval:"+str(self.global_config["system_notification"]["interval_sec"]))
                print("duration:"+str(self.global_config["system_notification"]["duration_sec"]))
                time.sleep(self.global_config["system_notification"]["interval_sec"])
                try:
                    json_response, url_full = get_dict_with_param(lang="FR_DE")
                    toast.show_toast(
                        title='id: {0}'.format(json_response[0]["id"]),
                        msg='content: {0}'.format(json_response[0]["line"]),
                        icon_path=None,
                        duration=self.global_config["system_notification"]["duration_sec"],
                        threaded=False,
                        callback_on_click=(lambda: open_browser_tab(get_dict_with_param(lang="FR_DE", id=json_response[0]["id"], url_only=True))))
                except:
                    print('error: creating toast notification')
        pass

class SettingFile():
    def __init__(self):
        # self.isLocking = True
        # with open('config.json', 'r') as f:
        #     self.config = json.load(f)
        self.isLocking = False

    def parseConfig(self, config=None):
        config = self.readConfigFile()
        print(config)
        print(config["system_notification"]["enable"])

    def readConfigFile(self, filename="config.json"):
        if self.isLocking == True:
            return None
        self.isLocking = True
        with open(filename, 'r', encoding='utf-8') as f:
            config = json.load(f)
        self.isLocking = False
        return config

    # def addOnlineSource(self, name, search_url, option=None):
        # @param name Name of source
        # @param search_url Using this search_url+word to search will return
        # @param option Instruction for special condition, ...

    def writeConfigToJsonFile(self, config, filename="config.json"):
        if self.isLocking == True:
            return None
        self.isLocking = True
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        self.isLocking = False
        return True

# sf = SettingFile()
# sf.parseConfig()

class NotifierThead(threading.Thread):
    """ A worker thread that takes directory names from a queue, finds all
        files in them recursively and reports the result.

        Input is done by placing directory names (as strings) into the
        Queue passed in dir_q.

        Output is done by placing tuples into the Queue passed in result_q.
        Each tuple is (thread name, dirname, [list of files]).

        Ask the thread to stop by calling its join() method.
    """
    def __init__(self, dir_q):
        super(NotifierThead, self).__init__()
        self.daemon = True
        self.dir_q = dir_q
        self.stoprequest = threading.Event()

    def run(self):
        
        if platform == "linux" or platform == "linux2":
            # linux
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
                    print('error: notify')

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
                    print('error: notify')

        elif platform == "win32":
            from win10toast import ToastNotifier
            def open_browser_tab(url):
                try:
                    webbrowser.open(url, new=0)
                except:
                    print("error opening web")

            toast = ToastNotifier()
            while not self.stoprequest.isSet():
                try:
                    new_config = self.dir_q.get(True, 0.05)
                except queue.Empty:
                    print("no new config")
                    pass
                if new_config:
                    self.global_config = new_config
                    print("new interval_sec:"+str(self.global_config["system_notification"]["interval_sec"]))

                print("----------------------game running----------------------")
                print("interval:"+str(self.global_config["system_notification"]["interval_sec"]))
                print("duration:"+str(self.global_config["system_notification"]["duration_sec"]))
                time.sleep(self.global_config["system_notification"]["interval_sec"])
                try:
                    json_response, url_full = get_dict_with_param(lang="FR_DE")
                    toast.show_toast(
                        title='id: {0}'.format(json_response[0]["id"]),
                        msg='content: {0}'.format(json_response[0]["line"]),
                        icon_path=None,
                        duration=self.global_config["system_notification"]["duration_sec"],
                        threaded=False,
                        callback_on_click=(lambda: open_browser_tab(get_dict_with_param(lang="FR_DE", id=json_response[0]["id"], url_only=True))))
                except:
                    print('error: creating toast notification')
        pass

    def join(self, timeout=None):
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)