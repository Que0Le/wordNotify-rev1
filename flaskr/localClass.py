import os, time
import random
import threading, queue
from flaskr import handyfunctions
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

class NotifierThead(threading.Thread):
    """ A worker thread that takes care of system notification 
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

    def get_random_word(self, global_config):
        rand_dict_index = random.randint(
            0, len(global_config["notification"]["dict_dbs_to_notify"])-1)
        rand_dict_name = global_config["notification"]["dict_dbs_to_notify"][rand_dict_index]
        rand_dict_id = -1
        # Get all dict to find out id
        json_response, url_full = handyfunctions.get_dict_by_param(
            encoded_u=current_app.config["ENCODED_U"],
            dict_id="")
        if not json_response:
            print("could not fetch from server!")
            time.sleep(1)
            return None, None, None, None
        for r in json_response["response"]:
            if r["table_name"] == rand_dict_name:
                rand_dict_id = r["w_id"]
                break
        if rand_dict_id<0:
            print(f"dict with name {rand_dict_name} not found in server!")
            time.sleep(1)
            return None, None, None, None
        json_response, url_full = handyfunctions.get_word_by_param(
            encoded_u=current_app.config["ENCODED_U"], 
            dict_id=rand_dict_id,
            word_id="random")
        return rand_dict_id, rand_dict_name, json_response, url_full

    def run(self):
        with self.app.app_context():
            last_show = datetime.now()
            while not self.stoprequest.isSet():
                global_config = current_app.config["GLOBAL_CONFIG"]
                if not global_config["system_notification"]["enable"]:
                    current_app.config["THREAD_STARTED"] = 0
                    print("notifier stopped")
                    time.sleep(1)
                    continue
                # Check if we should comback later until interval_sec passed:
                now = datetime.now()
                if ((now-last_show).seconds < global_config["system_notification"]["interval_sec"]):
                    time.sleep(1)
                    continue
                # Get data to push:
                try:
                    rand_dict_id, rand_dict_name, json_response, url_full = \
                        self.get_random_word(global_config)
                    if not (rand_dict_id and rand_dict_name and json_response and url_full):
                        print("Could not get_random_word")
                        time.sleep(1)
                        continue
                except:
                    traceback.print_exc()
                    print('error: getting notification material.')
                    continue
                # Push notification
                # TODO: Consider a while True here to prevent exception db busy (openned by other thread)
                notify_w_id = json_response["response"][0]["w_id"]
                title_name = global_config["notification"]["entries_to_notify"][0]
                notify_title = json_response["response"][0][title_name] + f" (from {rand_dict_name})"
                # Construct content
                notify_content = ""
                for entry in global_config["notification"]["entries_to_notify"][1:]:
                    if json_response["response"][0][entry]:
                        notify_content += json_response["response"][0][entry] + "\n"
                # Construct link onclick
                u = handyfunctions.url_base + "/api/v1/dicts/" + str(rand_dict_id) + "/words/" + str(notify_w_id)
                if platform == "linux":
                    from plyer import notification
                    try:
                        notification.notify(
                            title=notify_title,
                            message=notify_content,
                            app_name='wordNotify',
                            # app_icon="beat_brick.ico",  # e.g. 'C:\\icon_32x32.ico'
                            timeout=global_config["system_notification"]["duration_sec"],
                        )
                    except Exception:
                        traceback.print_exc()
                        print('error: creating linux notification')

                elif platform == "darwin":
                    try:
                        notify_methods = global_config["system_notification"]["methods"]["macos"]
                        if notify_methods["terminal-notifier"]:
                            os.system("""
                            terminal-notifier -title '{}' -message '{}' -open '{}'
                            """.format(notify_title, notify_content, u))
                        elif notify_methods["plyer"]:
                            from plyer import notification
                            notification.notify(
                                title=notify_title,
                                message=notify_content,
                                app_name='wordNotify',
                                # app_icon="beat_brick.ico",  # e.g. 'C:\\icon_32x32.ico'
                                timeout=global_config["system_notification"]["duration_sec"],
                            )
                    except Exception:
                        traceback.print_exc()
                        print('error: creating macos notification')

                elif platform == "win32":
                    from win10toast import ToastNotifier
                    toast = ToastNotifier()
                    try:
                        # http://127.0.0.1:5000/dicts/6/words/13359
                        toast.show_toast(
                            title=notify_title,
                            msg=notify_content,
                            icon_path=None,
                            duration=global_config["system_notification"]["duration_sec"],
                            threaded=False,
                            callback_on_click=(lambda: self.open_browser_tab(u)))
                    except Exception:
                        traceback.print_exc()
                        print('error: creating windows toast notification')

                # Update last notification time to "now"
                last_show = now

    def join(self, timeout=None):
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)