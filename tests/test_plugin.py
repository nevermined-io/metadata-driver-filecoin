# THIS FILE IMPLEMENTS AN INTEGRATION TEST ASSUMING A LOCAL
# POWERGATE NODE AVAILABLE IN localhost:5002
import tempfile

import pytest
from metadata_driver_interface.exceptions import DriverError

from metadata_driver_filecoin.data_plugin import Plugin

plugin = Plugin()


def test_url_parser():
    filecoin_url = plugin.parse_url('cid://POWERGATE_TOKEN:DEAL_ID@POWERGATE_HOST:1111/CID_HASH')
    assert filecoin_url.user_token == 'POWERGATE_TOKEN'
    assert filecoin_url.deal_id == 'DEAL_ID'
    assert filecoin_url.powergate_host == 'POWERGATE_HOST'
    assert filecoin_url.powergate_port == '1111'
    assert filecoin_url.cid_hash == 'CID_HASH'

    filecoin_url = plugin.parse_url('cid://POWERGATE_HOST:1111/CID_HASH')
    assert filecoin_url.user_token is None
    assert filecoin_url.deal_id is None
    assert filecoin_url.powergate_host == 'POWERGATE_HOST'
    assert filecoin_url.powergate_port == '1111'
    assert filecoin_url.cid_hash == 'CID_HASH'

    filecoin_url = plugin.parse_url('cid://POWERGATE_TOKEN:DEAL_ID@CID_HASH')
    assert filecoin_url.user_token == 'POWERGATE_TOKEN'
    assert filecoin_url.deal_id == 'DEAL_ID'
    assert filecoin_url.powergate_host == 'localhost'
    assert filecoin_url.powergate_port == '5002'
    assert filecoin_url.cid_hash == 'CID_HASH'

    filecoin_url = plugin.parse_url('cid://POWERGATE_TOKEN:@CID_HASH')
    assert filecoin_url.user_token == 'POWERGATE_TOKEN'
    assert filecoin_url.deal_id is None
    assert filecoin_url.powergate_host == 'localhost'
    assert filecoin_url.powergate_port == '5002'
    assert filecoin_url.cid_hash == 'CID_HASH'

    filecoin_url = plugin.parse_url('cid://:DEAL_ID@CID_HASH')
    assert filecoin_url.user_token is None
    assert filecoin_url.deal_id == 'DEAL_ID'
    assert filecoin_url.powergate_host == 'localhost'
    assert filecoin_url.powergate_port == '5002'
    assert filecoin_url.cid_hash == 'CID_HASH'

    filecoin_url = plugin.parse_url('cid://CID_HASH')
    assert filecoin_url.user_token is None
    assert filecoin_url.deal_id is None
    assert filecoin_url.powergate_host == 'localhost'
    assert filecoin_url.powergate_port == '5002'
    assert filecoin_url.cid_hash == 'CID_HASH'


def test_plugin_config():
    assert plugin.type() == 'filecoin'


