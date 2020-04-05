import os, time
import random
import threading, queue
from handyfunctions import *
from plyer import notification
from sys import platform
import webbrowser
# The other candidate for notification windows is https://github.com/malja/zroya
import json
from datetime import datetime

class SettingFile():
    def __init__(self):
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

    def writeConfigToJsonFile(self, config, filename="config.json"):
        if self.isLocking == True:
            return None
        self.isLocking = True
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)
        self.isLocking = False
        return True

    def verify_config(config):
        # TODO: verify config with actual state of data. 
        # (notification->dict_dbs_to_notify may not contain dict_db table in our database)
        if True:
            return ""
        return "Verify failed. Check input."

class NotifierThead(threading.Thread):

    def __init__(self, g_config_queue, encoded_u):
        super(NotifierThead, self).__init__()
        self.daemon = True
        self.g_config_queue = g_config_queue
        self.stoprequest = threading.Event()
        self.encoded_u = encoded_u
    def open_browser_tab(url):
        try:
            webbrowser.open(url, new=0)
        except:
            print("error opening web")

    def run(self):
        last_show = datetime.now()
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
            # Prevent error import on other platform
            from win10toast import ToastNotifier
            toast = ToastNotifier()

            while not self.stoprequest.isSet():
                # Fetching new config from queue. Dirty trick to communicate with main thread.
                try:
                    new_config = self.g_config_queue.get(True, 0.05)
                except queue.Empty:
                    # print("no new config")
                    new_config = None
                    pass
                if new_config:
                    self.global_config = new_config
                    # print("new interval_sec:"+str(self.global_config["system_notification"]["interval_sec"]))
                # Compare escalated time with interval_sec
                now = datetime.now()
                if ((now-last_show).seconds < self.global_config["system_notification"]["interval_sec"]):
                    time.sleep(1)
                    continue
                # Push notification
                try:
                    rand_dict_index = random.randint(
                        0, len(self.global_config["notification"]["dict_dbs_to_notify"]))
                    json_response, url_full = get_dict_with_param(
                        self.encoded_u, dict_db=self.global_config["notification"]["dict_dbs_to_notify"][rand_dict_index])

                    toast.show_toast(
                        title='id: {0}'.format(json_response[0]["id"]),
                        msg='content: {0}'.format(json_response[0]["line"]),
                        icon_path=None,
                        duration=self.global_config["system_notification"]["duration_sec"],
                        threaded=False,
                        callback_on_click=(lambda: open_browser_tab(url_full)))
                except:
                    print('error: creating toast notification')
                    # Update last notification time to "now"
                last_show = now

    def join(self, timeout=None):
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)