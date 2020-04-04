import requests, base64
import json

url_base = 'http://127.0.0.1:5000'
get_dicts = '/api/v1/resources/dicts?' # lang=${lang}&random=true
user="tom"
password="thisIStom"
encoded_u = base64.b64encode((user+":"+password).encode()).decode()
headers = {'Content-Type': 'application/json',
           "Authorization": "Basic %s" % encoded_u}
# response = requests.get('http://127.0.0.1:5000/api/v1/resources/dicts?lang=DE_EN&random=true', auth=HTTPBasicAuth('tom', 'thisIStom')).content.decode('utf-8')
# json.loads(

def get_dict_with_param(lang="DE_EN", id="", url_only=False):
    callsign = "&random=true" if id=="" else f"&id={id}"
    url_full = f"{url_base}{get_dicts}lang={lang}{callsign}"
    print(url_full)
    response = requests.get(url_full, headers=headers)
    if url_only:
        return url_full
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8')), url_full
    else:
        return None

