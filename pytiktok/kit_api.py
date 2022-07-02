"""
    Api impl for tiktok developer
"""
import random
import string
from typing import Optional, List, Tuple, Union, IO

import requests
from requests import Request, Response

import pytiktok.models as mds
from pytiktok.error import PyTiktokError


class KitApi:
    BASE_URL = "https://open-api.tiktok.com"
    AUTHORIZE_URL = "https://www.tiktok.com/auth/authorize/"
    DEFAULT_SCOPE = "user.info.basic,video.list"
    DEFAULT_REDIRECT_URI = "https://localhost/"

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        access_token: Optional[str] = None,
        timeout: Optional[int] = None,
        proxies: Optional[dict] = None,
        redirect_uri: Optional[str] = None,
        scope: Optional[str] = None,
        base_url: Optional[str] = None,
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.session = requests.Session()
        self.timeout = timeout
        self.proxies = proxies
        self.redirect_uri = redirect_uri or self.DEFAULT_REDIRECT_URI
        self.scope = scope or self.DEFAULT_SCOPE
        self.base_url = base_url or self.BASE_URL

    @staticmethod
    def generate_state():
        """
        Generate custom state.
        """
        return "".join(random.sample(string.ascii_letters, 16))

    def get_authorize_url(
        self, scope: Optional[str] = None, redirect_uri: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Get url for user to authorize.
        :param scope: Comma-separated scope name. Need to be approved first
        :param redirect_uri: Callback url.
        :return: authorize url and state
        """
        if not self.client_id:
            raise PyTiktokError(f"Need app client id")

        if scope is None:
            scope = self.scope
        if redirect_uri is None:
            redirect_uri = self.redirect_uri

        state = self.generate_state()
        req = Request(
            url=self.AUTHORIZE_URL,
            params={
                "client_key": self.client_id,
                "scope": scope,
                "response_type": "code",
                "redirect_uri": redirect_uri,
                "state": state,
            },
        ).prepare()
        return req.url, state

    def generate_access_token(
        self, code: str, return_json: bool = False
    ) -> Union[mds.KitAccessTokenResponse, dict]:
        """
        Fetch Access Token using Authorization Code.

        :param code: Authorization code get from Web/iOS/Android authorization callback.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Access Token response.
        """
        if not self.client_id or not self.client_secret:
            raise PyTiktokError("Need app client id and client secret")

        resp = self._request(
            # To keep code not be encoding, set it in url.
            path=f"oauth/access_token/?code={code}",
            params={
                "client_key": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "authorization_code",
            },
            enforce_auth=False,
        )
        data = self.parse_response(resp)
        self.access_token = data.get("data", {}).get("access_token")
        return (
            data if return_json else mds.KitAccessTokenResponse.new_from_json_dict(data)
        )

    def refresh_access_token(
        self, refresh_token: str, return_json: bool = False
    ) -> Union[mds.KitAccessTokenResponse, dict]:
        """
        Refresh Access Token using Refresh Token.

        :param refresh_token: The user's refresh_token.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Access Token response.
        """
        if not self.client_id:
            raise PyTiktokError("Need app client id")
        resp = self._request(
            path="oauth/refresh_token/",
            params={
                "client_key": self.client_id,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            enforce_auth=False,
        )
        data = self.parse_response(resp)
        self.access_token = data.get("data", {}).get("access_token")
        return (
            data if return_json else mds.KitAccessTokenResponse.new_from_json_dict(data)
        )

    def revoke_access_token(
        self, open_id: str, access_token: str, return_json: bool = False
    ) -> Union[mds.KitAccessTokenResponse, dict]:
        """
        revoke access token.

        :param open_id: The TikTok user's unique identifier.
        :param access_token: The token that bears the authorization of the TikTok user.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: AccountToken revoke data.
        """
        resp = self._request(
            path="oauth/revoke/",
            params={
                "open_id": open_id,
                "access_token": access_token,
            },
            enforce_auth=False,
        )
        data = self.parse_response(resp)
        return (
            data if return_json else mds.KitAccessTokenResponse.new_from_json_dict(data)
        )

    def get_qrcode(
        self,
        scope: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        return_json: bool = False,
    ) -> Union[mds.KitQrCodeResponse, dict]:
        """
        Get qr code for user to authorize
        :param scope: Comma-separated scope name. Need to be approved first
        :param redirect_uri: Callback url.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: qr code and state.
        """
        if not self.client_id:
            raise PyTiktokError(f"Need app client id")

        if scope is None:
            scope = self.scope
        if redirect_uri is None:
            redirect_uri = self.redirect_uri

        state = self.generate_state()
        params = {
            "client_key": self.client_id,
            "scope": scope,
            "next": redirect_uri,
            "state": state,
        }
        resp = self._request(
            path="v0/oauth/get_qrcode", params=params, enforce_auth=False
        )
        data = self.parse_response(resp)
        return data if return_json else mds.KitQrCodeResponse.new_from_json_dict(data)

    def check_qrcode(
        self,
        token: str,
        scope: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        return_json: bool = False,
    ) -> Union[mds.KitQrCodeResponse, dict]:
        """
        Check QR code status.

        :param token: Token obtained along with QR code
        :param scope: Comma-separated scope name. Need to be approved first
        :param redirect_uri: Callback url.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: QR code status.
        """
        if not self.client_id:
            raise PyTiktokError(f"Need app client id")

        if scope is None:
            scope = self.scope
        if redirect_uri is None:
            redirect_uri = self.redirect_uri
        params = {
            "client_key": self.client_id,
            "scope": scope,
            "next": redirect_uri,
            "token": token,
        }
        resp = self._request(
            path="v0/oauth/check_qrcode", params=params, enforce_auth=False
        )
        data = self.parse_response(resp)
        return data if return_json else mds.KitQrCodeResponse.new_from_json_dict(data)

    def _request(
        self,
        path: str,
        verb: str = "POST",
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        files: Optional[dict] = None,
        json: Optional[dict] = None,
        enforce_auth: bool = True,
    ) -> Response:
        """
        Request for TikTok api url
        :param path: The api location for TikTok
        :param verb: HTTP Method, like GET,POST,PUT.
        :param params: The url params to send in the body of the request.
        :param data: The form data to send in the body of the request.
        :param files: The form files to send in the body of the request.
        :param json: The json data to send in the body of the request.
        :param enforce_auth: Does the request require authentication.
        :return: A json object
        """
        headers = None
        if enforce_auth:
            if not self.access_token:
                raise PyTiktokError("The request must be authenticated.")
            if json is not None:
                json["access_token"] = self.access_token
            elif params is not None:
                params["access_token"] = self.access_token

        if not path.startswith("http"):
            path = f"{self.base_url}/{path}"

        resp = self.session.request(
            url=path,
            method=verb,
            headers=headers,
            params=params,
            data=data,
            files=files,
            json=json,
            timeout=self.timeout,
            proxies=self.proxies,
        )

        return resp

    @staticmethod
    def parse_response(response: Response) -> dict:
        try:
            data = response.json()
        except ValueError:
            raise PyTiktokError(f"Unknown error: {response.text}")
        if "error" in data and data["error"].get("code") != 0:
            raise PyTiktokError(data["error"])
        return data

    def get_user_info(
        self,
        open_id: str,
        fields: Optional[List[str]] = None,
        return_json: bool = False,
    ) -> Union[mds.KitUserResponse, dict]:
        """
        Get some basic information of a given TikTok user.
        :param open_id: The TikTok user's unique identifier.
        :param fields: The set of user field. Default: ["open_id", "avatar"].
            Choose to include from: ["open_id", "union_id", "avatar_url", "avatar_url_100", "avatar_url_200", "avatar_large_url", "display_name"]
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: User data.
        """
        if fields is None:
            fields = ["open_id", "union_id", "display_name", "avatar_url"]
        resp = self._request(
            path="user/info/",
            json={
                "open_id": open_id,
                "fields": fields,
            },
        )
        data = self.parse_response(resp)
        return data if return_json else mds.KitUserResponse.new_from_json_dict(data)

    def get_user_videos(
        self,
        open_id: str,
        fields: Optional[List[str]] = None,
        cursor: Optional[int] = None,
        max_count: Optional[int] = None,
        return_json: bool = False,
    ) -> Union[mds.KitVideosResponse, dict]:
        """
        Get a paginated list of given user's public TikTok video posts, sorted by create_time in descending order.

        :param open_id: The TikTok user's unique identifier.
        :param fields: The set of optional video metadata.
        :param cursor: Cursor for pagination. The cursor value is a UTC Unix timestamp in milliseconds.
            You can pass in a customized timestamp to fetch the user's videos posted after the provided timestamp.
        :param max_count: The maximum number of videos that will be returned from each page.
            Default is 10. Maximum is 20.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Videos data.
        """
        if fields is None:
            fields = ["id", "create_time", "duration", "share_url"]
        data = {"open_id": open_id, "fields": fields}
        if cursor is not None:
            data["cursor"] = cursor
        if max_count is not None:
            data["max_count"] = max_count
        resp = self._request(
            path="video/list/",
            json=data,
        )
        data = self.parse_response(resp)
        return data if return_json else mds.KitVideosResponse.new_from_json_dict(data)

    def query_videos(
        self,
        open_id: str,
        filters: dict,
        fields: Optional[List[str]] = None,
        return_json: bool = False,
    ) -> Union[mds.KitVideosResponse, dict]:
        """
        Query video data by video ids.

        :param open_id: The TikTok user's unique identifier.
        :param filters: Fields: video_ids: set<string>, max 20 video ids at a time.
            Example: {"video_ids": ["6963640889373723909"]}
        :param fields: The set of optional video metadata.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Videos data.
        """
        if fields is None:
            fields = ["id", "create_time", "duration", "share_url"]
        data = {"open_id": open_id, "fields": fields, "filters": filters}
        resp = self._request(
            path="video/query/",
            json=data,
        )
        data = self.parse_response(resp)
        return data if return_json else mds.KitVideosResponse.new_from_json_dict(data)

    def share_video(
        self,
        open_id: str,
        video: IO,
        return_json: bool = False,
    ) -> Union[mds.KitShareVideoResponse, dict]:
        """
        Share Video API allows users to share videos from your Web or Desktop app into TikTok.

        :param open_id: The TikTok user's unique identifier.
        :param video: The video file obj.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Share response.
        """
        resp = self._request(
            path="share/video/upload/",
            params={"open_id": open_id},
            files={"video": video},
        )
        data = self.parse_response(resp)
        return (
            data if return_json else mds.KitShareVideoResponse.new_from_json_dict(data)
        )
