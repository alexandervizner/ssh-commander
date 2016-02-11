from playhouse.shortcuts import dict_to_model
from aiohttp.web_exceptions import HTTPBadRequest, HTTPOk, HTTPInternalServerError

from models.group import Group
from aiohttp.web import json_response, View
from core.utils import serialize, get_object_or_404


class GroupView(View):

    async def get(self):

        group_id = self.request.match_info.get('id')

        if group_id:
            data = serialize(Group.get(Group.id == group_id))
        else:
            data = serialize(Group.select())

        return json_response({'data': data})

    async def post(self):

        data = await self.request.post()

        if data and Group.filter(**data).exists():
            raise HTTPBadRequest()

        group = dict_to_model(Group, data)
        group.save()

        return HTTPOk()

    async def patch(self):

        data = await self.request.post()
        group_name = data.get('name')
        group_id = self.request.match_info.get('group_id')
        group = Group.get(Group.id == group_id)

        if group and group_name == group.name:
            raise HTTPBadRequest()

        if Group.filter(Group.name == group_name).exists():
            raise HTTPBadRequest()

        group.name = group_name

        if group.save():
            return HTTPOk()

        return HTTPInternalServerError()

    async def delete(self):

        group_id = self.request.match_info.get('group_id')

        group = get_object_or_404(Group, Group.id == group_id)

        if group.delete_instance():
            return HTTPOk()

        return HTTPInternalServerError()
