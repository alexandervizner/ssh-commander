from unittest import TestCase

from models.host import Host
from models.group import Group
from core.utils import create_tables
from core.serializer import Serializer, Deserializer


class SerializerTest(TestCase):
    def setUp(self):
        create_tables()

    def test_basic_host_serialization(self):

        serializer = Serializer()
        group = Group.create(name='Test_group')
        host = Host.create(
            group=group,
            hostname='linux',
            ip_address='1.1.1.1',
            username='admin',
            password='qwe123',
            ssh_key='AAAAB3Nz',
            post_login_cmd='pwd'
        )

        expected = {
            'ip_address': '1.1.1.1',
            'id': 1,
            'updated_at': host.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'group': 1,
            'username': 'admin',
            'created_at': host.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'hostname': 'linux',
            'password': 'qwe123',
            'post_login_cmd': 'pwd',
            'ssh_key': 'AAAAB3Nz'}

        result = serializer.serialize_object(host)

        self.assertDictEqual(result, expected)
