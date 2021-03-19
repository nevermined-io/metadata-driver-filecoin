import os

from metadata_driver_interface.data_plugin import AbstractPlugin
from pygate_grpc.client import PowerGateClient


class Plugin(AbstractPlugin):
    POWERGATE_GATEWAY_ENVVAR = 'POWERGATE_GATEWAY'
    POWERGATE_IS_SECURE_ENVVAR = 'POWERGATE_IS_SECURE'
    POWERGATE_TOKEN_ENVVAR = 'POWERGATE_TOKEN'
    DEFAULT_POWERGATE_GATEWAY = 'localhost:5002'
    DEFAULT_POWERGATE_IS_SECURE = 'False'
    PROTOCOL = 'cid://'

    def __init__(self, config=None):
        self.config = config
        self._powergate_gateway = os.getenv(Plugin.POWERGATE_GATEWAY_ENVVAR, Plugin.DEFAULT_POWERGATE_GATEWAY)
        self._is_secure = os.getenv(Plugin.POWERGATE_IS_SECURE_ENVVAR, Plugin.DEFAULT_POWERGATE_IS_SECURE)
        self._client = PowerGateClient(self._powergate_gateway, is_secure=(self._is_secure == 'True'))
        self._token = os.getenv(Plugin.POWERGATE_TOKEN_ENVVAR, None)


    def type(self):
        """str: the type of this plugin (``'filecoin'``)"""
        return 'filecoin'

    def connect(self):
        try:
            if self._token is None:
                self._user = self._client.admin.users.create()
                self._token = self._user.token
        except Exception as e:
            raise

    def upload(self, local_file, remote_file):
        pass

    def download(self, remote_file, local_file='/tmp/filecoin-test.raw'):
        self.connect()
        file_bytes = self._client.data.get(self.parse_url(remote_file), self._token)
        if local_file is not None:  # Write to a file on disk
            with open(local_file, "wb") as f:
                f.write(file_bytes)
        return file_bytes

    def list(self, remote_folder):
        pass

    @staticmethod
    def parse_url(url):
        assert url and isinstance(url, str) \
               and url.startswith(Plugin.PROTOCOL), \
            f'Bad argument type `{url}`, expected ' \
            f'a str URL starting with "cid://"'

        cid = url.split(Plugin.PROTOCOL)[1]
        return cid

    def generate_url(self, remote_file):
        return f'{self.parse_url(remote_file)}'

    def delete(self, remote_file):
        pass

    def copy(self, source_path, dest_path):
        pass

    def create_directory(self, remote_folder):
        pass

    def retrieve_availability_proof(self):
        pass
