# THIS FILE IMPLEMENTS AN INTEGRATION TEST ASSUMING A LOCAL
# POWERGATE NODE AVAILABLE IN localhost:5002
import tempfile

import pytest
from metadata_driver_interface.exceptions import DriverError

from metadata_driver_filecoin.data_plugin import Plugin

plugin = Plugin()


def test_connect():
    try:
        plugin.connect()
    except DriverError:
        pytest.fail("Connection problem ..")


def test_upload_download():
    try:
        cid_hash = plugin.upload('README.md')
        print('CID: ' + cid_hash)
        cid_url = 'cid://' + cid_hash
        copy_file_path = tempfile.mktemp()
        print('Copy file: ' + copy_file_path)
        file_content = plugin.download(cid_url, copy_file_path)
        assert len(file_content) > 0
    except DriverError:
        pytest.fail("Upload problem ..")


