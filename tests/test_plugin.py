from metadata_driver_filecoin.data_plugin import Plugin

plugin = Plugin()


def test_url_parser():
    filecoin_url = plugin.parse_url('cid://USER_TOKEN:DEAL_ID@ESTUARY_GATEWAY/CID_HASH')
    assert filecoin_url.user_token == 'USER_TOKEN'
    assert filecoin_url.deal_id == 'DEAL_ID'
    assert filecoin_url.gateway_url == 'ESTUARY_GATEWAY'
    assert filecoin_url.cid_hash == 'CID_HASH'

    filecoin_url = plugin.parse_url('cid://ESTUARY_GATEWAY/CID_HASH')
    assert filecoin_url.user_token is None
    assert filecoin_url.deal_id is None
    assert filecoin_url.gateway_url == 'ESTUARY_GATEWAY'
    assert filecoin_url.cid_hash == 'CID_HASH'

    filecoin_url = plugin.parse_url('cid://USER_TOKEN:DEAL_ID@CID_HASH')
    assert filecoin_url.user_token == 'USER_TOKEN'
    assert filecoin_url.deal_id == 'DEAL_ID'
    assert filecoin_url.gateway_url == 'https://shuttle-4.estuary.tech'
    assert filecoin_url.cid_hash == 'CID_HASH'

    filecoin_url = plugin.parse_url('cid://USER_TOKEN:@CID_HASH')
    assert filecoin_url.user_token == 'USER_TOKEN'
    assert filecoin_url.deal_id is None
    assert filecoin_url.gateway_url == 'https://shuttle-4.estuary.tech'
    assert filecoin_url.cid_hash == 'CID_HASH'

    filecoin_url = plugin.parse_url('cid://:DEAL_ID@CID_HASH')
    assert filecoin_url.user_token is None
    assert filecoin_url.deal_id == 'DEAL_ID'
    assert filecoin_url.gateway_url == 'https://shuttle-4.estuary.tech'
    assert filecoin_url.cid_hash == 'CID_HASH'

    filecoin_url = plugin.parse_url('cid://CID_HASH')
    assert filecoin_url.user_token is None
    assert filecoin_url.deal_id is None
    assert filecoin_url.gateway_url == 'https://shuttle-4.estuary.tech'
    assert filecoin_url.cid_hash == 'CID_HASH'


def test_plugin_config():
    assert plugin.type() == 'filecoin'


