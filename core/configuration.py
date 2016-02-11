import os, json

SETTINGS_FILE = 'settings.json'
CORE_ROOT = os.path.dirname(os.path.abspath(__file__))
SETTINGS_FILE_PATH = os.path.join(CORE_ROOT, SETTINGS_FILE)

DEFAULTS = {
    'application': {
        'host': 'localhost',
        'port': 8080,
        'debug': False,
    },
    'database': {
        'name': 'data.db',
        'user': 'root',
        'password': '',
    }
}


class Configuration():
    def __init__(self, file=None):

        if file:
            with open(SETTINGS_FILE_PATH) as file:
                self.settings = json.load(file)
        else:
            self.settings = DEFAULTS

    @property
    def application(self):
        return self.settings['application']

    @property
    def database(self):
        return self.settings['database']

    @property
    def is_debug(self):
        return settings.application['debug']


settings = Configuration(SETTINGS_FILE_PATH)
