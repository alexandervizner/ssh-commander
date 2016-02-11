from playhouse.shortcuts import dict_to_model
from aiohttp.web_exceptions import HTTPBadRequest, HTTPOk, HTTPInternalServerError

from models import Group
from models.host import Host
from aiohttp.web import json_response, View
from core.utils import serialize, get_object_or_404, get_data_or_400


class HostView(View):

    async def get(self):

        group_id = self.request.match_info.get('id')

        if group_id:
            data = serialize(Host.get(Host.id == group_id))
        else:
            data = serialize(Host.select())

        return json_response({'data': data})

    async def post(self):

        data = await self.request.post()

        group_id = get_data_or_400(data, 'group_id', raise_exception=False)
        hostname = get_data_or_400(data, 'hostname')
        ip_address = get_data_or_400(data, 'ip_address')
        username = get_data_or_400(data, 'username')
        password = get_data_or_400(data, 'password')
        ssh_key = get_data_or_400(data, 'ssh_key')
        post_login_cmd = get_data_or_400(data, 'post_login_cmd')

        if data and Host.filter(**data).exists():
            raise HTTPBadRequest()

        if group_id is not None and not Group.filter(Group.id == group_id).exists():
            raise HTTPBadRequest()

        host = dict_to_model(Host, data)
        host.save()

        return HTTPOk()

    async def patch(self):

        data = await self.request.post()
        group_name = data.get('name')
        group_id = self.request.match_info.get('group_id')
        group = Host.get(Host.id == group_id)

        if group and group_name == group.name:
            raise HTTPBadRequest()

        if Host.filter(Host.name == group_name).exists():
            raise HTTPBadRequest()

        group.name = group_name
        
        if group.save():
            return HTTPOk()
        
        return HTTPInternalServerError()

    async def delete(self):

        group_id = self.request.match_info.get('group_id')

        group = get_object_or_404(Host, Host.id == group_id)

        if group.delete_instance():
            return HTTPOk()

        return HTTPInternalServerError()
