# Setup for Ubuntu/debian:
``` bash
apt-get install python3-venv
# venv
python3 -m venv venv
. venv/bin/activate
# Flask
# Make sure to be in this projects root
pip install -e .

# Dependencies. TODO: add those packages to setup.cfg
# We need now:
python3 -m pip install flask flask_httpauth flask_cors
python3 -m pip install requests
# python3 -m pip install git+http://github.com/kivy/pyobjus/ --user
# python3 -m pip install dbus-python

# For notification. Consider only use notify-send:y
# sudo apt-get install python3-dev
# sudo apt-get install libcairo2-dev libjpeg-dev libgif-dev
# sudo apt-get --reinstall install libnotify-bin notify-osd
# python3 -m pip install notify-send
python3 -m pip install plyer

# Create DB
cd tools/
python3 dictcc2sql.py

# Run this once
cd ..
chmod +x start_flask.sh

# From now to start server:
./start_flask.sh

# Testing url
# http://localhost:5000/
# http://localhost:5000/api/v1/resources/settings
# http://localhost:5000/api/v1/resources/dicts?dict_db=DE_FR&random=true
```

# Setup for Windows 10: DO NOT USE POWERSHELL!!! USE CMD!
``` bash
# Official guide: https://flask.palletsprojects.com/en/1.1.x/cli/#application-discovery
python -m venv venv
# CMD ONLY:
venv\Scripts\activate.bat
# 'deactivate' to exit venv

# venv\Scripts\activate.bat not work anymore with Windows PowerShell
# Consider also 'Set-ExecutionPolicy Unrestricted -Force' if this line doesnt work
# venv\Scripts\activate.ps1

pip install -e .

python -m pip install flask flask_httpauth flask_cors
python -m pip install requests
python -m pip install git+https://github.com/Charnelx/Windows-10-Toast-Notifications

# Create DB
cd tools/
python dictcc2sql.py

# Register env
set FLASK_APP=flaskr
set FLASK_ENV=development
set FLASK_DEBUG=0
flask init-db

# From now run:
flask run --no-reload --host=0.0.0.0

# Testing url
# http://localhost:5000/
# http://localhost:5000/api/v1/resources/settings
# http://localhost:5000/api/v1/resources/dicts?dict_db=DE_FR&random=true
```

# Setup for Windows 7
``` bash
python -m venv venv
venv\Scripts\activate.bat

pip install -e .

python -m pip install flask flask_httpauth flask_cors
python -m pip install requests
python -m pip install git+https://github.com/Charnelx/Windows-10-Toast-Notifications

# Create DB
cd tools/
python dictcc2sql.py

# Register env
set FLASK_APP=flaskr
set FLASK_ENV=development
set FLASK_DEBUG=0
flask init-db

# From now run:
flask run --no-reload --host=0.0.0.0

# Testing url
# http://localhost:5000/
# http://localhost:5000/api/v1/resources/settings
# http://localhost:5000/api/v1/resources/dicts?dict_db=DE_FR&random=true
```


# Setup for macOS
``` bash
# venv
python3 -m venv venv
. venv/bin/activate
# Flask
pip install -e .

# Dependencies. TODO: add those packages to setup.cfg
# We need now:
python3 -m pip install flask flask_httpauth flask_cors
python3 -m pip install Cython
python3 -m pip install git+http://github.com/kivy/pyobjus/ #--user #macos

# terminal-notifier offer much better features. default choice...
brew install terminal-notifier
# ... OR crossplatform plyer. Set in config.json.
python3 -m pip install plyer

# Create DB
cd tools/
python3 dictcc2sql.py

# Run this once
chmod +x start_flask.sh

# From now to start server:
./start_flask.sh

# Testing url
# http://localhost:5000/
# http://localhost:5000/api/v1/resources/settings
# http://localhost:5000/api/v1/resources/dicts?dict_db=DE_FR&random=true
```


---------------------------------------------
<br>
# DONT TOUCH THIS

``` bash
# packging
pip install pyinstaller
pyinstaller yourprogram.py
```

Some example:
``` bash
# Enter this in browser
http://127.0.0.1:5000/api/v1/resources/dicts?dict_db=DE_FR&random=true
http://127.0.0.1:5000/api/v1/resources/settings
```
