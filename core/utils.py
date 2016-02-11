import datetime

from peewee import Model
from playhouse.shortcuts import model_to_dict, dict_to_model
from aiohttp.web_exceptions import HTTPNotFound, HTTPBadRequest

from models import Group, Host


def create_tables():
    from models.base import database
    database.connect()
    database.create_tables([Group, Host])


def serialize(data) -> dict:

    s = Serializer()

    if isinstance(data, Model):
        return s.serialize_object(data)
    elif data.count() > 0:
        return [s.serialize_object(q) for q in data]
    else:
        return {}


def get_object_or_404(model, *expressions):
    try:
        return model.get(*expressions)
    except model.DoesNotExist:
        raise HTTPNotFound()


def get_data_or_400(request_data, param_name, raise_exception=True):

    value = request_data.get(param_name)

    if not value and raise_exception:
        raise HTTPBadRequest()

    return value


class Serializer(object):

    date_format = '%Y-%m-%d'
    time_format = '%H:%M:%S'
    datetime_format = ' '.join([date_format, time_format])

    def convert_value(self, value):
        if isinstance(value, datetime.datetime):
            return value.strftime(self.datetime_format)
        elif isinstance(value, datetime.date):
            return value.strftime(self.date_format)
        elif isinstance(value, datetime.time):
            return value.strftime(self.time_format)
        elif isinstance(value, Model):
            return value.get_id()
        else:
            return value

    def clean_data(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                self.clean_data(value)
            elif isinstance(value, (list, tuple)):
                data[key] = map(self.clean_data, value)
            else:
                data[key] = self.convert_value(value)
        return data

    def serialize_object(self, obj, fields=None, exclude=None):
        data = model_to_dict(obj, fields, exclude)
        return self.clean_data(data)


class Deserializer(object):

    def deserialize_object(self, model, data):
        return dict_to_model(model, data)
