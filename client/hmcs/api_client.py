from hmcs.utils import read_configs


class APIClient():
    def __init__(self):
        self.server_url = read_configs()['server_url']

    def set_baby_magnet_mode(self, mode):
        print(self.server_url, mode)
