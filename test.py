from sys import platform
from win10toast import ToastNotifier
import webbrowser
if platform == "linux" or platform == "linux2":
    # linux
    pass
elif platform == "darwin":
    # OS X
    pass
elif platform == "win32":
    print("windows")
    def open_browser_tab(url):
        try:
            webbrowser.open(url, new=0)
        except:
            print("error opening web")
    def say_hello(url):
        print('Hello!')
        open_browser_tab(url)
    toast = ToastNotifier()
    toast.show_toast( title="Notification", msg="Here comes the message",
                        icon_path=None, duration=5, threaded=False, callback_on_click=lambda: say_hello("https://google.com"))