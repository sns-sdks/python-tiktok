"""
    Tests for the access token API
"""

import pytest
import responses

from pytiktok import BusinessAccountApi, PyTiktokError


@responses.activate
def test_generate_access_token(bus_api, helpers):
    with pytest.raises(PyTiktokError):
        BusinessAccountApi().generate_access_token(code="test_code")

    data = helpers.load_json("testsdata/business/access_token/token_resp.json")
    responses.add(
        responses.POST,
        "https://business-api.tiktok.com/open_api/v1.3/tt_user/oauth2/token/",
        json=data,
    )
    resp = bus_api.generate_access_token(code="test_code")
    assert resp.access_token == "act.token"


@responses.activate
def test_refresh_access_token(bus_api, helpers):
    with pytest.raises(PyTiktokError):
        BusinessAccountApi().refresh_access_token(refresh_token="test_refresh_token")

    data = helpers.load_json("testsdata/business/access_token/refresh_resp.json")
    responses.add(
        responses.POST,
        "https://business-api.tiktok.com/open_api/v1.3/tt_user/oauth2/refresh_token/",
        json=data,
    )
    resp = bus_api.refresh_access_token(refresh_token="test_refresh_token")
    assert resp.access_token == "act.token"


@responses.activate
def test_revoke_access_token(bus_api, helpers):
    with pytest.raises(PyTiktokError):
        BusinessAccountApi().revoke_access_token(access_token="test_access_token")

    data = helpers.load_json("testsdata/business/access_token/revoke_resp.json")
    responses.add(
        responses.POST,
        "https://business-api.tiktok.com/open_api/v1.3/tt_user/oauth2/revoke/",
        json=data,
    )
    resp = bus_api.revoke_access_token(access_token="test_access_token")
    assert resp.code == 0


@responses.activate
def test_get_token_info(bus_api, helpers):
    with pytest.raises(PyTiktokError):
        BusinessAccountApi().get_token_info(access_token="test_access_token")

    data = helpers.load_json("testsdata/business/access_token/token_info_resp.json")
    responses.add(
        responses.POST,
        "https://business-api.tiktok.com/open_api/v1.3/tt_user/token_info/get/",
        json=data,
    )
    resp = bus_api.get_token_info(access_token="test_access_token")
    assert resp.app_id == "app_id"
