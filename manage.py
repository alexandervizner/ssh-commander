import logging, asyncio, aiohttp_debugtoolbar
from aiohttp import web

logging.basicConfig(filename='logs/application.log',level=logging.DEBUG)
logger = logging.getLogger(__name__)


def db_handler():

    @asyncio.coroutine
    def factory(app, handler):

        @asyncio.coroutine
        def middleware(request):
            if request.path.startswith('/static/') or request.path.startswith('/_debugtoolbar'):
                response = yield from handler(request)
                return response

            from models.base import database
            database.connect()
            request.db = database

            response = yield from handler(request)
            if not database.is_closed():
                database.close()

            return response
        return middleware
    return factory


def setup():

    from web.routes import routes
    from core.configuration import settings

    middlewares = [db_handler(), aiohttp_debugtoolbar.middleware]

    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop, middlewares=middlewares)

    if settings.is_debug:
        aiohttp_debugtoolbar.setup(app)

    handler = app.make_handler()

    for route in routes:
        app.router.add_route(*route)

    host = settings.application['host']
    port = settings.application['port']

    server_generator = loop.create_server(handler, host, port)
    server = loop.run_until_complete(server_generator)

    logger.info('Server launched %s.', server.sockets[0].getsockname())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info('Stopping server...')
    finally:
        loop.run_until_complete(handler.finish_connections(1.0))
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.run_until_complete(app.finish())
    loop.close()
    logger.info('Server stopped.')


if __name__ == '__main__':
    setup()
