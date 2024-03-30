import os
from logs import logging
from settings import app_settings
from client import flush_tasks


def self_update(to_version):
    logging.info('Self updating...')
    os.system('cd /miner/clore_rent_server_agent')
    os.system('git pull https://github.com/dsglazyrin/clore_rent_server_agent.git')
    app_settings.updater_version = to_version
    app_settings.save_config()
    flush_tasks()
    os.system('supervisorctl reload')
    exit()


