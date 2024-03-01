"""
    Tests for the access token API
"""

import pytest
import responses

from pytiktok import BusinessAccountApi, PyTiktokError


@responses.activate
def test_revoke_access_token(bus_api, helpers):
    with pytest.raises(PyTiktokError):
        BusinessAccountApi(access_token="test_access_token").revoke_access_token(
            access_token="test_access_token"
        )

    data = helpers.load_json("testsdata/business/access_token/revoke_resp.json")
    responses.add(
        responses.POST,
        "https://business-api.tiktok.com/open_api/v1.3/tt_user/oauth2/revoke/",
        json=data,
    )
    resp = bus_api.revoke_access_token(access_token="test_access_token")
    assert resp.code == 0
