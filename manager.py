from logs import logging
import sched
import time
import client
from settings import app_settings
import miner_manager
import os

def send_ping():
    logging.info('ping!')
    #print(time.time())
    client.ping()
    shed = sched.scheduler(time.time, time.sleep)
    shed.enter(app_settings.ping_interval, 1, send_ping)
    shed.run()


logging.info('Starting manager')
logging.info('Ping interval:' + str(app_settings.ping_interval) + 'sec')

if not os.path.isfile('/etc/supervisor/conf.d/miner.conf'):
    logging.info('No miner.conf. Configuring miners.')
    miner_manager.disable_miners()
    miner_manager.enable_miners()

send_ping()
