# THIS FILE IMPLEMENTS AN INTEGRATION TEST USING A REMOTE ESTUARY GATEWAY
import os
import tempfile

import pytest
from metadata_driver_interface.exceptions import DriverError

from metadata_driver_filecoin.data_plugin import Plugin

plugin = Plugin()


def test_upload_download():
    try:
        test_file = 'NOTICE'
        cid_hash = plugin.upload(test_file)
        print('CID: ' + cid_hash)
        cid_url = 'cid://' + cid_hash
        copy_file_path = tempfile.mktemp()
        print('Copy file: ' + copy_file_path)
        downloaded = plugin.download(cid_url, copy_file_path)
        assert downloaded
        uploaded_size = os.path.getsize(test_file)
        downloaded_size = os.path.getsize(copy_file_path)
        assert uploaded_size == downloaded_size
    except DriverError:
        pytest.fail("Upload problem ..")


