from aiohttp.hdrs import *
from web.views import GroupView, HostView

routes = [
    (METH_GET, '/groups', GroupView),
    (METH_POST, '/groups', GroupView),
    # (METH_PATCH, '/groups/{group_id}', Group),
    # (METH_GET, '/hosts', Host)
]