import os


class DeviceTypes:
    CPU = 'CPU'
    GPU = 'GPU'


def restart_miners():
    restart_miner(DeviceTypes.CPU)
    restart_miner(DeviceTypes.GPU)


def restart_miner(devtype):
    print(os.popen("ls -l").read())

restart_miners()