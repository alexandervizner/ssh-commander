from aiohttp.hdrs import *
from web.views import GroupView, HostView

routes = [
    (METH_GET, '/groups/', GroupView),
    (METH_GET, '/groups/{id}', GroupView),
    (METH_POST, '/groups/', GroupView),
    (METH_PATCH, '/groups/{group_id}', GroupView),
    (METH_DELETE, '/groups/{group_id}', GroupView),
    (METH_GET, '/hosts/', HostView),
    (METH_GET, '/hosts/{id}', HostView),
    (METH_POST, '/hosts/', HostView),
    (METH_PATCH, '/hosts/{host_id}', HostView),
    (METH_DELETE, '/hosts/{host_id}', HostView),
]