import requests
from settings import app_settings
from logs import logging
import json
import updater
import miner_manager
import sols


def ping():
    res = requests.post(compose_url('ping'), headers=basic_headers(), data=ping_data())
    if res.status_code == 200:
        logging.info('Ping ok')
        process_server_data(res.content)

        return True
    logging.info('Ping failed')
    return False


def process_server_data(content):
    server_data = json.loads(content)
    if 'updaterversion' in server_data:
        if server_data['updaterversion'] != app_settings.updater_version:
            logging.info('New version available:' + server_data['updaterversion'] + 'Updating...')
            updater.self_update(server_data['updaterversion'])
    if 'tasks' in server_data:
        for task in server_data['tasks']:
            if 'restartminers' in task:
                logging.info('Got command RESTART_MINERS')
                miner_manager.restart_miners()
            if 'resendsols' in task:
                logging.info('Got command RESEND_SOLUTIONS')
                sols.resend_sols('latest')


def ping_data():
    res = {
        "tasks": []
    }

    return res


def basic_headers():
    return {
        "content-type": "application/json",
        "server-id": app_settings.server_id,
        "auth-key": app_settings.auth_key,
        "updater-version": str(app_settings.updater_version)
    }


def compose_url(method):
    return 'http://' + app_settings.server + ':' + app_settings.port + '/crypto/hs/c/' + method




