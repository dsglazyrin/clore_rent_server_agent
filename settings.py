import json

main_dir = '/miner/'
CPU_dir = '/miner/CPU/'
GPU_dir = '/miner/GPU/'
self_dir = '/miner/clore_rent_server_agent/'


class AppSettings:
    def __init__(self):
        with open('app.json', 'r') as f:
            data = json.load(f)
            self.server = data['server']
            self.port = data['port']
            self.server_id = data['server_id']
            self.auth_key = data['auth_key']
            if 'updater_version' in data:
                self.updater_version = data['updater_version']
            else:
                self.updater_version = 0
            if 'ping_interval' in data:
                self.ping_interval = data['ping_interval']
            else:
                self.ping_interval = 300

            f.close()

    def save_config(self):
        data = {
            'server': self.server,
            'port': self.port,
            'server_id': self.server_id,
            'auth_key': self.auth_key,
            'updater_version': self.updater_version,
            'ping_interval': self.ping_interval
        }
        with open('app.json', 'w') as f:
            f.write(json.dumps(data))
            f.close()



app_settings = AppSettings()
