from kivy.network.urlrequest import UrlRequest
from kivymd.app import MDApp
import json
import urllib

HOST = 'http://127.0.0.1:8000/'


def add_url_params(params):
    string = '?'
    for parm in params:
        string += parm + '=' + urllib.parse.quote(str(params[parm]), encoding="UTF-8") + '&'
    return string[:-1]


def requests_failure(request, data):
    pass


def api_request(url, on_success, full_url="", params={}, on_failure=requests_failure, method='GET', body=None, headers=None, on_finish=None):
    params = add_url_params({'format': 'json', **params})
    login = MDApp.get_running_app().user_api_token
    if login:
        heads = headers or {}
        headers = {'Authorization': 'Token '+login, **heads}

    if body:
        heads = headers or {}
        headers = heads
        if not headers.get("Content-type"):
            body = json.dumps(body, indent=4)
            headers['Content-type'] = 'Application/json'

        headers['Content-length'] = len(body)

    if not full_url:
        full_url = HOST + "api/" + url + params

    UrlRequest(full_url, on_success, on_failure=on_failure, method=method, req_body=body,
               req_headers=headers, debug=True, on_error=on_failure, on_finish=on_finish)

