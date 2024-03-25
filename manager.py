import updater
import time
from datetime import datetime
from logs import logging
import client


cnt = 0
while True:
    if datetime.utcnow().minute % 5 == 0:
        time.sleep(60)
        logging.info('ping!')
        #client.ping()
        while datetime.utcnow().minute % 5 == 0:
            time.sleep(10)
    time.sleep(10)
