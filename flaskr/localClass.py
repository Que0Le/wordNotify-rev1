import os, time
import random
import threading, queue
# from handyfunctions import *
from flaskr import handyfunctions
# from flaskr import handyfunctions
# from flask import plyer
from sys import platform
import webbrowser
# The other candidate for notification windows is https://github.com/malja/zroya
import json
from datetime import datetime
import traceback
from flask import current_app

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

    def verify_config(self, config):
        # TODO: verify config with actual state of data. 
        # (notification->dict_dbs_to_notify may not contain dict_db table in our database)
        if True:
            return ""
        return "Verify failed. Check input."


class WorkerThread(threading.Thread):
    """ A worker thread that takes directory names from a queue, finds all
        files in them recursively and reports the result.

        Input is done by placing directory names (as strings) into the
        Queue passed in dir_q.

        Output is done by placing tuples into the Queue passed in result_q.
        Each tuple is (thread name, dirname, [list of files]).

        Ask the thread to stop by calling its join() method.
    """
    def __init__(self, app):
        super(WorkerThread, self).__init__()
        self.app = app
        self.daemon = True
        self.stoprequest = threading.Event()

    def run(self):
        # As long as we weren't asked to stop, try to take new tasks from the
        # queue. The tasks are taken with a blocking 'get', so no CPU
        # cycles are wasted while waiting.
        # Also, 'get' is given a timeout, so stoprequest is always checked,
        # even if there's nothing in the queue.

        with self.app.app_context():
            while not self.stoprequest.isSet():
                # print("from thread "+ str(threading.currentThread().getName()) + 
                #         " WorkerThread GLOBAL_CONFIG: " + 
                #         str(current_app.config['GLOBAL_CONFIG']))
                time.sleep(1)
    def join(self, timeout=None):
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)


class NotifierThead(threading.Thread):
    """ A worker thread that takes directory names from a queue, finds all
        files in them recursively and reports the result.

        Input is done by placing directory names (as strings) into the
        Queue passed in dir_q.

        Output is done by placing tuples into the Queue passed in result_q.
        Each tuple is (thread name, dirname, [list of files]).

        Ask the thread to stop by calling its join() method.
    """
    def __init__(self, app):
        super(NotifierThead, self).__init__()
        self.app = app
        self.daemon = True
        self.stoprequest = threading.Event()

    def open_browser_tab(self, url):
            try:
                webbrowser.open(url, new=0)
            except:
                print("error opening web")

    def run(self):
        # As long as we weren't asked to stop, try to take new tasks from the
        # queue. The tasks are taken with a blocking 'get', so no CPU
        # cycles are wasted while waiting.
        # Also, 'get' is given a timeout, so stoprequest is always checked,
        # even if there's nothing in the queue.

        with self.app.app_context():
            while not self.stoprequest.isSet(): 
                last_show = datetime.now()
                if platform == "linux":
                    # linux
                    from plyer import notification
                    while not self.stoprequest.isSet():
                        global_config = current_app.config["GLOBAL_CONFIG"]

                        now = datetime.now()
                        if ((now-last_show).seconds < global_config["system_notification"]["interval_sec"]):
                            time.sleep(1)
                            continue
                        # Push notification
                        # TODO: Consider a while True here to prevent exception db busy (openned by other thread)
                        try:
                            rand_dict_index = random.randint(
                                0, len(global_config["notification"]["dict_dbs_to_notify"])-1)
                            json_response, url_full = handyfunctions.get_dict_with_param(
                                encoded_u=current_app.config["ENCODED_U"], 
                                dict_db=global_config["notification"]["dict_dbs_to_notify"][rand_dict_index])
                            
                            notification.notify(
                                title='id: {0}'.format(json_response[0]["id"]),
                                message='content: {0}'.format(json_response[0]["line"]),
                                app_name='wordNotify',
                                # app_icon="beat_brick.ico",  # e.g. 'C:\\icon_32x32.ico'
                                timeout=global_config["system_notification"]["duration_sec"],
                            )
                        except Exception:
                            traceback.print_exc()
                            print('error: creating linux notification')
                        # Update last notification time to "now"
                        last_show = now

                if platform == "darwin":
                    while not self.stoprequest.isSet():
                        global_config = current_app.config["GLOBAL_CONFIG"]
                        notify_methods = global_config["system_notification"]["methods"]["macos"]

                        now = datetime.now()
                        if ((now-last_show).seconds < global_config["system_notification"]["interval_sec"]):
                            time.sleep(1)
                            continue
                        # Push notification
                        # TODO: Consider a while True here to prevent exception db busy (openned by other thread)
                        try:
                            rand_dict_index = random.randint(
                                0, len(global_config["notification"]["dict_dbs_to_notify"])-1)
                            json_response, url_full = handyfunctions.get_dict_with_param(
                                encoded_u=current_app.config["ENCODED_U"], 
                                dict_db=global_config["notification"]["dict_dbs_to_notify"][rand_dict_index])
                            
                            if notify_methods["terminal-notifier"]:
                                os.system("""
                                terminal-notifier -title '{}' -message '{}' -open '{}'
                                """.format(json_response[0]["id"], json_response[0]["line"], url_full))
                            elif notify_methods["plyer"]:
                                from plyer import notification
                                notification.notify(
                                    title='id: {0}'.format(json_response[0]["id"]),
                                    message='content: {0}'.format(json_response[0]["line"]),
                                    app_name='wordNotify',
                                    # app_icon="beat_brick.ico",  # e.g. 'C:\\icon_32x32.ico'
                                    timeout=global_config["system_notification"]["duration_sec"],
                                )
                        except Exception:
                            traceback.print_exc()
                            print('error: creating macos notification')
                        # Update last notification time to "now"
                        last_show = now

                elif platform == "win32":
                    # Prevent error import on other platform
                    from win10toast import ToastNotifier
                    toast = ToastNotifier()

                    while not self.stoprequest.isSet():
                        global_config = current_app.config["GLOBAL_CONFIG"]
                        # Compare escalated time with interval_sec
                        now = datetime.now()
                        if ((now-last_show).seconds < global_config["system_notification"]["interval_sec"]):
                            time.sleep(1)
                            continue
                        # Push notification
                        # TODO: Consider a while True here to prevent exception db busy (openned by other thread)
                        try:
                            rand_dict_index = random.randint(
                                0, len(global_config["notification"]["dict_dbs_to_notify"])-1)
                            json_response, url_full = handyfunctions.get_dict_with_param(
                                encoded_u=current_app.config["ENCODED_U"], 
                                dict_db=global_config["notification"]["dict_dbs_to_notify"][rand_dict_index])

                            toast.show_toast(
                                title='id: {0}'.format(json_response[0]["id"]),
                                msg='content: {0}'.format(json_response[0]["line"]),
                                icon_path=None,
                                duration=global_config["system_notification"]["duration_sec"],
                                threaded=False,
                                callback_on_click=(lambda: self.open_browser_tab(url_full)))
                        except Exception:
                            traceback.print_exc()
                            print('error: creating toast notification')
                            # Update last notification time to "now"
                        last_show = now


        
    def join(self, timeout=None):
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)