from peewee import CharField
from .base import BaseModel


class Group(BaseModel):

    name = CharField(unique=True)

