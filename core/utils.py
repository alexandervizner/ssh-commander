from models import Group, Host


def create_tables():
    from models.base import database
    database.connect()
    database.create_tables([Group, Host])