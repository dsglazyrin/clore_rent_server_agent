import requests
from settings import app_settings
from logs import logging


def ping():
    res = requests.post(compose_url('ping'), headers=basic_headers(), data={})
    if res.status_code == 200:
        logging.info('Ping ok')
        return True
    logging.info('Ping failed')
    return False


def basic_headers():
    return {
        "content-type": "application/json",
        "server-id": app_settings.server_id,
        "auth-key": app_settings.auth_key
    }


def compose_url(method):
    return 'http://' + app_settings.server + ':' + app_settings.port + '/crypto/hs/c/' + method




print(ping())