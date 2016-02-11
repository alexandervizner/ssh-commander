from peewee import CharField
from playhouse.fields import ForeignKeyField

from .base import BaseModel
from models.group import Group


class Host(BaseModel):

    group = ForeignKeyField(Group, related_name='hosts', null=True)

    hostname = CharField(max_length=24, unique=True)

    ip_address = CharField(max_length=16, unique=True)

    username = CharField(max_length=24)

    password = CharField(max_length=24)

    ssh_key = CharField(max_length=1024)

    post_login_cmd = CharField()