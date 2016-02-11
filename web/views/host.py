from aiohttp import web


class HostView(web.View):

    async def get(self):
        return {'return': 'test'}