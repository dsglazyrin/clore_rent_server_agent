import updater
import time
from datetime import datetime
import client


cnt = 0
while True:
    if datetime.utcnow().minute == 3:
        time.sleep(60)
        updater.self_update()
    if datetime.utcnow().minute % 5 == 0:
        client.ping()

