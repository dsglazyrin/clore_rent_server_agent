import json

main_dir = '/miner/'
CPU_dir = '/miner/CPU/'
GPU_dir = '/miner/GPU/'


class AppSettings:
    def __init__(self):
        with open('app.json', 'r') as f:
            data = json.load(f)
            self.server = data['server']
            self.port = data['port']
            self.server_id = data['server_id']
            self.auth_key = data['auth_key']


app_settings = AppSettings()
