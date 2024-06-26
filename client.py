import requests
from settings import app_settings, self_dir
from logs import logging
import json
import updater
import miner_manager
import sols
import os


def ping():
    res = requests.post(compose_url('ping'), headers=basic_headers(), data=ping_data())
    if res.status_code == 200:
        logging.info('Ping ok')
        flush_tasks()
        process_server_data(res.content)
        return True
    logging.info('Ping failed')
    return False


def process_server_data(content):
    server_data = json.loads(content)
    if 'epoch' in server_data:
        if server_data['epoch'] != app_settings.epoch:
            logging.info('Qubic epoch changed to' + server_data['epoch'])
            app_settings.epoch = server_data['epoch']
            app_settings.save_config()

    if 'new_auth_key' in server_data:
        app_settings.auth_key = server_data.new_auth_key
        app_settings.save_config()

    if 'updaterversion' in server_data:
        if server_data['updaterversion'] != app_settings.updater_version:
            logging.info('New version available:' + server_data['updaterversion'] + 'Updating...')
            updater.self_update(server_data['updaterversion'])

    if 'tasks' in server_data:
        for task in server_data['tasks']:
            if 'restartminers' in task:
                logging.info('Got command RESTART_MINERS')
                miner_manager.restart_miners()
                mark_task_completed('restartminers')
            if 'resendsols' in task:
                logging.info('Got command RESEND_SOLUTIONS')
                sols.resend_sols('latest')
                mark_task_completed('resendsols')


def mark_task_completed(task):
    t = load_completed_tasks()
    if task in t:
        return
    if isinstance(task, str):
        t.append({
            'name': task,
            'result': True
        })
    else:
        t.append(task)

    with open('tasks.json', 'w') as f:
        f.write(json.dump(t))
        f.close()


def flush_tasks():
    with open('tasks.json', 'w') as f:
        f.write('[]')
        f.close()


def load_completed_tasks():
    if os.path.isfile(self_dir + 'tasks.json'):
        with open(self_dir + 'tasks.json', 'r') as f:
            t = json.load(f)
            f.close()
            return t
    else:
        return []


def ping_data():
    res = {
        "tasks": load_completed_tasks()
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




