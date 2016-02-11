import os
import datetime
from core.configuration import settings
from peewee import SqliteDatabase, Model, DateTimeField


if os.getenv('DB') == 'test':
    database = SqliteDatabase(':memory:')
else:
    database = SqliteDatabase(settings.database['name'], threadlocals=True)


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField()

    class Meta:
        database = database

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)