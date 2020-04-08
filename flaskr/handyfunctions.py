import base64, json

import requests
from werkzeug.security import generate_password_hash

url_base = 'http://127.0.0.1:5000'
get_dicts = '/api/v1/resources/dicts?' # lang=${lang}&random=true
# user="tom"
# password="thisIStom"
# encoded_u = base64.b64encode((user+":"+password).encode()).decode()
# headers = {'Content-Type': 'application/json',
#            "Authorization": "Basic %s" % encoded_u}
# response = requests.get('http://127.0.0.1:5000/api/v1/resources/dicts?lang=DE_EN&random=true', auth=HTTPBasicAuth('tom', 'thisIStom')).content.decode('utf-8')
# json.loads(

def get_dict_with_param(encoded_u, dict_db="DE_EN", id="", url_only=False):
    callsign = "&random=true" if id=="" else f"&id={id}"
    url_full = f"{url_base}{get_dicts}dict_db={dict_db}{callsign}"
    print(url_full)
    headers = {'Content-Type': 'application/json',
           "Authorization": "Basic %s" % encoded_u}
    response = requests.get(url_full, headers=headers)
    if url_only:
        return url_full
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8')), url_full
    else:
        return None

def update_config(app, new_config):
    app.config["GLOBAL_CONFIG"] = new_config
    user = new_config["settings"]["API_username"]
    password = new_config["settings"]["API_password"]
    users = {
        user: generate_password_hash(password),
        "jerry": generate_password_hash("ThatisJerry")
    }
    encoded_u = base64.b64encode((user+":"+password).encode()).decode()
    app.config.from_mapping(
        USERS=users,
        ENCODED_U=encoded_u,
    )