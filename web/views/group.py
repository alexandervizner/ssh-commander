from aiohttp import web
from models.group import Group
from core.serializer import Serializer


class GroupView(web.View):

    async def get(self):

        group = Group.select().order_by(Group.name).get()

        serializer = Serializer()
        groups_str = serializer.serialize_object(group)

        return web.Response(text=str(groups_str))


class GroupSerializer(Serializer):
    pass
