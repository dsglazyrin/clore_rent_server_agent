# Sols manager
import settings
import json
import os
from minerManager import DeviceTypes


def resend_sols(epoch):
    mark_as_not_submitted(DeviceTypes.CPU, epoch)
    mark_as_not_submitted(DeviceTypes.GPU, epoch)


def mark_as_not_submitted(devtype, epoch):
    if devtype == DeviceTypes.CPU:
        file_name = settings.CPU_dir + 'stats.' + epoch + '.lock'
    else:
        file_name = settings.GPU_dir + 'stats.' + epoch + '.lock'

    if not os.path.exists(file_name):
        return

    stats_file = open(file_name)
    sols = json.load(stats_file)
    stats_file.close()
    for sol in sols['Solutions']:
        sol['Submitted'] = False

    stats_file = open(file_name, 'w')
    json.dump(sols, stats_file)
    stats_file.close()


class SolsManager:
    def __init__(self):
        self.sols_history_file = './solsh.json'
        self.sols = []
        self.sols_files = []

        with open(self.sols_history_file) as json_file:
            history = json.load(json_file)
            for sol in history:
                new_sol = Sol(sol)
                self.sols.append(new_sol)
                self.sols_files.append(new_sol.filename + '.' + new_sol.epoch)
            json_file.close()

    def find_new_sols(self):
        self._find_sols_files(settings.CPU_dir + 'sols/', DeviceTypes.CPU)
        self._find_sols_files(settings.GPU_dir + 'sols/', DeviceTypes.GPU)

    def _find_sols_files(self, path, dev_type):
        new_files = []
        for root, dirs, files in os.walk(path):
            for f_name in files:
                if f_name not in self.sols_files:
                    new_files.append(f_name)

        for f_name in new_files:
            new_sol = Sol(None)
            new_sol.from_file(f_name, dev_type)
            self.sols.append(new_sol)
            self.sols_files.append(f_name)

    def save_history(self):
        sols_as_list = []
        for sol in self.sols:
            sols_as_list.append(sol.as_dict())
        with open(self.sols_history_file, 'w') as outfile:
            json.dump(sols_as_list, outfile)
            outfile.close()

    def have_new(self):
        for sol in self.sols:
            if not sol.saved:
                return True
        return False

    def get_send_data(self):
        res = []
        for sol in self.sols:
            if sol.saved:
                continue
            with open(sol.full_path()) as sol_file:
                res.append({
                    'filename': sol.filename,
                    'epoch': sol.epoch,
                    'device_type': sol.device_type,
                    'content': json.load(sol_file)
                })
                sol_file.close()
        return res

    def all_new_sent(self):
        for sol in self.sols:
            if not sol.saved:
                sol.mark_saved()
        self.save_history()

    def sols_count(self):
        cpu, gpu = (0, 0)
        for sol in self.sols:
            if sol.device_type == DeviceTypes.CPU:
                cpu += 1
            else:
                gpu += 1
        return cpu, gpu


class Sol:
    def __init__(self, json_data=None):
        # json_data
        # {
        # 'filename' = '6ada11c1-bac3-46a4-a832-8fe98f1ec312',
        # 'epoch' = 'e100',
        # 'device_type' = 'GPU',
        # 'saved' = False
        # }

        if json_data is None:
            self.filename = ''
            self.epoch = ''
            self.device_type = ''
            self.saved = False
        else:
            self.filename = json_data['filename']
            self.epoch = json_data['epoch']
            self.device_type = json_data['device_type']
            self.saved = json_data['saved']

    def full_path(self):
        if self.device_type == DeviceTypes.CPU:
            return settings.CPU_dir + 'sols/' + self.filename + '.' + self.epoch
        else:
            return settings.GPU_dir + 'sols/' + self.filename + '.' + self.epoch

    def from_file(self, filename, device_type):
        self.filename, self.epoch = os.path.splitext(filename)
        self.device_type = device_type

    def mark_saved(self):
        self.saved = True

    def as_dict(self):
        return {
            'filename': self.filename,
            'epoch': self.epoch,
            'device_type': self.device_type,
            'saved': self.saved
        }

