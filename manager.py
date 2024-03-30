import updater
import time
from datetime import datetime
from logs import logging
import sched
import time
import client
from settings import app_settings


def send_ping():
    logging.info('ping!')
    #print(time.time())
    client.ping()
    shed = sched.scheduler(time.time, time.sleep)
    shed.enter(app_settings.ping_interval, 1, send_ping)
    shed.run()


logging.info('Starting manager')
logging.info('Ping interval:' + str(app_settings.ping_interval) + 'sec')

send_ping()
