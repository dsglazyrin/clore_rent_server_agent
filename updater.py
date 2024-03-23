import os
from logs import logging


def self_update():
    logging.info('Self updating...')
    os.system('cd /miner/clore_rent_server_agent')
    os.system('git pull https://github.com/dsglazyrin/clore_rent_server_agent.git')
    exit()


