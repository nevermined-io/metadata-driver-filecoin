import os

from metadata_driver_interface.data_plugin import AbstractPlugin
from metadata_driver_interface.exceptions import DriverError
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

    def connect(self, gateway_url=None, is_secure=False, token=None):
        try:
            if gateway_url is not None:
                self._powergate_gateway = gateway_url
                self._client = PowerGateClient(self._powergate_gateway, is_secure=is_secure)
                if token is not None:
                    self._token = token
            if self._token is None:
                self._user = self._client.admin.users.create()
                self._token = self._user.token
        except DriverError as e:
            raise

    def upload(self, local_file, gateway_url=DEFAULT_POWERGATE_GATEWAY, is_secure=False, token=None):
        try:
            self.connect(gateway_url, is_secure, token)
            staged_file = self._client.data.stage_file(local_file, self._token)

            # Apply the default storage config to the given file
            job = self._client.config.apply(staged_file.cid, override=False, token=self._token)
            return staged_file.cid
        except DriverError as e:
            raise

    def download(self, remote_file, local_file='/tmp/filecoin-test.raw', is_secure=False):
        try:
            filecoin_url = self.parse_url(remote_file, is_secure)
            self.connect(filecoin_url.gateway_url(), is_secure)
            if filecoin_url.deal_id is not None:
                self._client.config.apply(filecoin_url.cid_hash, import_deal_ids=[filecoin_url.deal_id], token=self._token)
            file_bytes = self._client.data.get(filecoin_url.cid_hash, self._token)
            if local_file is not None:  # Write to a file on disk
                with open(local_file, "wb") as f:
                    f.write(file_bytes)
            return file_bytes
        except DriverError as e:
            raise

    def list(self, remote_folder):
        pass

    @staticmethod
    def parse_url(url, is_secure=False):
        """
        It parses a url with the following formats:
        cid://POWERGATE_TOKEN:DEAL_ID@POWERGATE_HOST:POWERGATE_PORT/CID_HASH
        cid://POWERGATE_HOST:POWERGATE_PORT/CID_HASH
        cid://POWERGATE_TOKEN:DEAL_ID@CID_HASH
        cid://POWERGATE_TOKEN:@CID_HASH
        cid://:DEAL_ID@CID_HASH
        cid://CID_HASH
        :param url: the cid url
        :return: FilecoinUrl
        """
        assert url and isinstance(url, str) \
               and url.startswith(Plugin.PROTOCOL), \
            f'Bad argument type `{url}`, expected ' \
            f'a str URL starting with "cid://"'

        filecoin_url = FilecoinUrl()

        url_no_protocol = url.replace(Plugin.PROTOCOL, '')
        at_elements = url_no_protocol.split('@')
        if len(at_elements) > 1:  # We have a url with token and/or deal id
            access_info = at_elements[0].split(':')
            if len(access_info) > 1 and access_info[1] is not '':
                filecoin_url.deal_id = access_info[1]
            if access_info[0] is not '':
                filecoin_url.user_token = access_info[0]
            url_info = at_elements[1].split('/')
        else:
            url_info = at_elements[0].split('/')

        if len(url_info) > 1:  # We have hostname information
            host_info = url_info[0].split(':')
            if len(host_info) > 1:  # We have a port
                filecoin_url.powergate_port = host_info[1]
            filecoin_url.powergate_host = host_info[0]
            filecoin_url.cid_hash = url_info[1]
        else:
            filecoin_url.cid_hash = url_info[0]

        filecoin_url.is_secure = is_secure
        return filecoin_url

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


class FilecoinUrl:
    cid_hash = ''
    user_token = None
    deal_id = None
    powergate_host = 'localhost'
    powergate_port = '5002'
    is_secure = False

    def __init__(self, _cid_hash=None, _user_token=None, _deal_id=None, _host='localhost', _port='5002', _is_secure=False):
        self.cid_hash = _cid_hash
        self.user_token = _user_token
        self.deal_id = _deal_id
        self.powergate_host = _host
        self.powergate_port = _port
        self.is_secure = _is_secure

    def gateway_url(self):
        return self.powergate_host + ':' + self.powergate_port