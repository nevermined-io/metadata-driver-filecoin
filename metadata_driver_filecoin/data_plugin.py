import json
import os
import tempfile
import time

import requests
from metadata_driver_interface.data_plugin import AbstractPlugin
from metadata_driver_interface.exceptions import DriverError
from requests_toolbelt.multipart import encoder


class Plugin(AbstractPlugin):
    PROTOCOL = 'cid://'

    ESTUARY_GATEWAY_ENVVAR = 'ESTUARY_GATEWAY'
    ESTUARY_TOKEN_ENVVAR = 'ESTUARY_TOKEN'
    IPFS_GATEWAY_ENVVAR = 'IPFS_GATEWAY'
    DEFAULT_ESTUARY_GATEWAY = 'https://shuttle-4.estuary.tech'
    DEFAULT_IPFS_GATEWAY = 'https://dweb.link/ipfs/:cid'
    URI_ADD_CONTENT = '/content/add'
    URI_GET_BY_CID = '/content/by-cid/:cid'

    def __init__(self, config=None):
        self.config = config
        self._gateway = os.getenv(Plugin.ESTUARY_GATEWAY_ENVVAR, Plugin.DEFAULT_ESTUARY_GATEWAY)
        self._ipfs_gateway = os.getenv(Plugin.IPFS_GATEWAY_ENVVAR, Plugin.DEFAULT_IPFS_GATEWAY)
        self._token = os.getenv(Plugin.ESTUARY_TOKEN_ENVVAR, '')
        self._headers = {
            'Authorization': 'Bearer ' + self._token,
            'Accept': 'application/json',
        }

    def type(self):
        """str: the type of this plugin (``'filecoin'``)"""
        return 'filecoin'

    def upload(self, local_file, gateway_url=DEFAULT_ESTUARY_GATEWAY, token=None):
        try:
            url = self._gateway + Plugin.URI_ADD_CONTENT
            _file = {'data': (os.path.basename(local_file), open(local_file, 'rb'))}
            e = encoder.MultipartEncoder(_file)

            headers = self._headers
            headers['Content-Type'] = e.content_type

            r = requests.post(
                url,
                data=e,
                headers=headers
            )
            if r.status_code == 200 or r.status_code == 201:
                return json.loads(r.text)['cid']
            raise Exception('Unable to upload file: ' + r.status_code.__str__() + ' - ' + r.text)
        except DriverError as e:
            raise Exception('Unexpected error:' + repr(e))

    def download(self, cid_url, local_file=None, attempts=3):
        """
        Downloads a Filecoin content into a file (with large file support by streaming)

        :param cid_url: URL to download
        :param local_file: Local file name to contain the data downloaded
        :param attempts: Number of attempts
        :return: Boolean if file was downloaded or not
        """
        try:
            filecoin_url = self.parse_url(cid_url)

            for attempt in range(1, attempts + 1):
                if attempt > 1:
                    time.sleep(3)  # 3 seconds wait time between downloads
                with requests.get(
                        self._ipfs_gateway.replace(':cid', filecoin_url.cid_hash),
                        stream=True
                ) as r:
                    r.raise_for_status()
                    if local_file is None:
                        new_file, local_file = tempfile.mkstemp()
                    with open(local_file, 'wb') as out_file:
                        for chunk in r.iter_content(chunk_size=1024 * 1024):  # 1MB chunks
                            out_file.write(chunk)
                        return True
        except DriverError as e:
            raise Exception('Unexpected error:' + repr(e))
        return False

    def list(self, remote_folder):
        pass

    @staticmethod
    def parse_url(url):
        """
        It parses a url with the following formats:
        cid://USER_TOKEN:DEAL_ID@ESTUARY_TOKEN/CID_HASH
        cid://ESTUARY_TOKEN/CID_HASH
        cid://USER_TOKEN:DEAL_ID@CID_HASH
        cid://USER_TOKEN:@CID_HASH
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
        filecoin_url.url = url

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

        if len(url_info) > 1:  # We have gateway information
            filecoin_url.gateway_url = url_info[0]
            filecoin_url.cid_hash = url_info[1]
        else:
            filecoin_url.gateway_url = Plugin.DEFAULT_ESTUARY_GATEWAY
            filecoin_url.cid_hash = url_info[0]

        return filecoin_url

    def generate_url(self, remote_file):
        return f'{self.parse_url(remote_file).url}'

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
    gateway_url = 'https://shuttle-4.estuary.tech'
    url = None

    def __init__(self, _cid_hash=None, _user_token=None, _deal_id=None, _gateway='localhost'):
        self.cid_hash = _cid_hash
        self.user_token = _user_token
        self.deal_id = _deal_id
        self.gateway_url = _gateway

