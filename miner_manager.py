import os
from logs import logging
import time


class DeviceTypes:
    CPU = 'CPU'
    GPU = 'GPU'


class Executables:
    CPU_MINER = 'minerproc_cpu'
    GPU_MINER = 'minerproc_gpu'


class ProcNames:
    CPU_MINER_NAME = 'miner_cpu'
    GPU_MINER_NAME = 'miner_gpu'


def disable_miners():
    logging.info('Disabling miners')
    os.system('rm /etc/supervisor/conf.d/miner.conf')
    os.system('supervisorctl reload')
    logging.info('Supervisor updated')
    kill_miner_process(DeviceTypes.CPU)
    kill_miner_process(DeviceTypes.GPU)
    logging.info('Miners have been disabled')


def enable_miners():
    logging.info('Enabling miners')
    if get_miner_pid(DeviceTypes.GPU) is not None or get_miner_pid(DeviceTypes.CPU) is not None:
        logging.error('Miners processes are running! First disable them')
        return
    logging.info('Copying miner.conf')
    os.system('cp ./miner.conf /etc/supervisor/conf.d/miner.conf')
    logging.info('Reloading supervisor')
    os.system('supervisorctl reload')
    logging.info('Waiting for miners to start')
    time.sleep(5)
    pid = get_miner_pid(DeviceTypes.CPU, False)
    if pid is None:
        logging.error('CPU miner have not started!')
    else:
        logging.info('CPU miner started. PID ' + pid)
    pid = get_miner_pid(DeviceTypes.GPU, False)
    if pid is None:
        logging.error('GPU miner have not started!')
    else:
        logging.info('GPU miner started. PID ' + pid)
    logging.info('Miners have been enabled')


def kill_miner_process(devtype):
    pid = get_miner_pid(devtype)
    if pid is None:
        logging.error(devtype + ' miner is not running')
        return None
    logging.info('Killing ' + devtype + ' miner PID ' + pid)
    os.system('kill ' + pid)
    time.sleep(5)
    return pid


def restart_miners():
    logging.info('Restarting miners...')
    restart_miner(DeviceTypes.CPU)
    restart_miner(DeviceTypes.GPU)


def restart_miner(devtype):
    logging.info('Restarting ' + devtype + ' miner...')
    pid = kill_miner_process(devtype)
    if pid is None:
        logging.info(devtype + ' miner is not running')
        return
    new_pid = get_miner_pid(devtype)
    if new_pid != pid:
        logging.info(devtype + ' miner restarted.')
    else:
        logging.error('Troubles with ' + devtype + ' miner restarting')


def get_miner_pid(devtype, only_running=True):
    supervisor_status = os.popen("supervisorctl status").read().replace('  ', ' ').split('\n')
    for row in supervisor_status:
        proc = [r for r in row.split(' ') if r != '']

        if len(proc) < 2:
            continue

        if not only_running:
            if (proc[0] == ProcNames.CPU_MINER_NAME and devtype == DeviceTypes.CPU or
                    proc[0] == ProcNames.GPU_MINER_NAME and devtype == DeviceTypes.GPU):
                return proc[1]

        if (proc[0] == ProcNames.CPU_MINER_NAME and devtype == DeviceTypes.CPU or
                proc[0] == ProcNames.GPU_MINER_NAME and devtype == DeviceTypes.GPU) \
                and proc[1] == 'RUNNING':
            return proc[3].replace(',', '')
    return None


#restart_miners()
