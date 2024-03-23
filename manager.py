import updater
import time
from datetime import datetime
from logs import logging
import client


cnt = 0
while True:
    if datetime.utcnow().minute == 53:
        time.sleep(60)
        print('Self update')
        updater.self_update()
    if datetime.utcnow().minute % 5 == 0:
        time.sleep(60)
        logging.info('ping!')
        print('ping')
        #updater.self_update()
        #client.ping()
    time.sleep(10)
