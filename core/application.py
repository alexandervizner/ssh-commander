from aiohttp import web


class Application():

    def __init__(self, config):
        if isinstance(config, dict):
            self._config = config

    app = web.Application()

