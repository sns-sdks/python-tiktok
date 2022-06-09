"""
    Core API impl.
"""

from typing import Optional, Union

import requests
from requests import Response

import pytiktok.models as mds
from pytiktok.error import PyTiktokError


class BusinessAccountApi:
    BASE_URL = "https://business-api.tiktok.com/open_api"

    def __init__(
        self,
        app_id: Optional[str] = None,
        app_secret: Optional[str] = None,
        access_token: Optional[str] = None,
        timeout: Optional[int] = None,
        proxies: Optional[dict] = None,
        base_url: Optional[str] = None,
        api_version: Optional[str] = "v1.2",
    ) -> None:
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = access_token
        self.session = requests.Session()
        self.timeout = timeout
        self.proxies = proxies
        self.api_version = api_version

        # base url prefix
        self.base_url = base_url or self.BASE_URL

    def generate_access_token(
        self, code: str, return_json: bool = False
    ) -> Union[mds.BusinessAccessToken, dict]:
        """
        Generate access token by the auth code.
        :param code: The code when user logged into TikTok and authorized your application for access to their account insights.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Access token
        """
        if not self.app_id or not self.app_secret:
            raise PyTiktokError(f"Need app id and app secret.")
        resp = self._request(
            verb="POST",
            path=f"{self.base_url}/oauth2/token/",
            params={"business": "tt_user"},
            json={
                "client_id": self.app_id,
                "client_secret": self.app_secret,
                "grant_type": "authorization_code",
                "auth_code": code,
            },
            enforce_auth=False,
        )
        data = self.parse_response(response=resp)
        return data if return_json else mds.BusinessAccessToken.new_from_json_dict(data)

    def refresh_access_token(
        self, refresh_token: str, return_json: bool = False
    ) -> Union[mds.BusinessAccessToken, dict]:
        """
        Generate access token by the refresh token.
        :param refresh_token: The refresh token for exchange access token.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Access token
        """
        if not self.app_id or not self.app_secret:
            raise PyTiktokError(f"Need app id and app secret.")
        resp = self._request(
            verb="POST",
            path=f"{self.base_url}/oauth2/token/",
            params={"business": "tt_user"},
            json={
                "client_id": self.app_id,
                "client_secret": self.app_secret,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            enforce_auth=False,
        )
        data = self.parse_response(response=resp)
        return data if return_json else mds.BusinessAccessToken.new_from_json_dict(data)

    def _request(
        self,
        path: str,
        verb: str = "GET",
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        json: Optional[dict] = None,
        enforce_auth: bool = True,
    ) -> Response:
        """
        Request for TikTok api url
        :param path: The api location for TikTok
        :param verb: HTTP Method, like GET,POST,PUT.
        :param params: The url params to send in the body of the request.
        :param data: The form data to send in the body of the request.
        :param json: The json data to send in the body of the request.
        :param enforce_auth: Does the request require authentication.
        :return: A json object
        """
        headers = None
        if enforce_auth:
            if not self.access_token:
                raise PyTiktokError("The request must be authenticated.")
            headers = {"Access-Token": self.access_token}

        if not path.startswith("http"):
            path = f"{self.base_url}/{self.api_version}/{path}"

        resp = self.session.request(
            url=path,
            method=verb,
            headers=headers,
            params=params,
            data=data,
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
            raise PyTiktokError(f"Unknown error: {response.content}")

        return data

    def get_account_data(
        self,
        business_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        fields: Optional[list] = None,
        return_json: bool = False,
    ) -> Union[mds.BusinessAccountResponse, dict]:
        """
        Access detailed analytics and insights about a TikTok business account's follower base and profile engagement.

        :param business_id: Application specific unique identifier for the TikTok account.
        :param start_date: Query start date, closed interval, format such as: 2021-06-01.
        :param end_date: Query end date, closed interval, format such as: 2021-06-01.
        :param fields: Requested fields. If not set, returns the default fields only.
            Default fields: ["display_name", "profile_image"]
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Account data.
        """
        data = {"business_id": business_id}
        if start_date is not None:
            data["start_date"] = start_date
        if end_date is not None:
            data["end_date"] = end_date
        if fields is not None:
            data["fields"] = fields

        resp = self._request(verb="POST", path="/business/get/", json=data)
        data = self.parse_response(resp)
        return (
            data
            if return_json
            else mds.BusinessAccountResponse.new_from_json_dict(data)
        )

    def get_account_videos(
        self,
        business_id: str,
        fields: Optional[list] = None,
        filters: Optional[dict] = None,
        cursor: Optional[int] = None,
        max_count: Optional[int] = None,
        return_json: bool = False,
    ) -> Union[mds.BusinessVideosResponse, dict]:
        """
        Get reach and engagement data for a business accounts organic posts.

        :param business_id: Application specific unique identifier for the TikTok account.
        :param fields: Requested fields. If not set, returns the default fields only. Default value: ["item_id"]
        :param filters: Filters to apply to the result set.
        :param cursor: Cursor for pagination.
        :param max_count: The maximum number of videos that will be returned for each page. [1..20]
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Account's videos data.
        """

        data = {"business_id": business_id}
        if fields is not None:
            data["fields"] = fields
        if filters is not None:
            data["filters"] = filters
        if cursor is not None:
            data["cursor"] = cursor
        if max_count is not None:
            data["max_count"] = max_count

        resp = self._request(verb="POST", path="business/videos/list/", json=data)
        data = self.parse_response(resp)
        return (
            data if return_json else mds.BusinessVideosResponse.new_from_json_dict(data)
        )

    def create_video(
        self,
        business_id: str,
        video_url: str,
        post_info: Optional[dict] = None,
        return_json: bool = False,
    ) -> Union[mds.BusinessVideoPublishResponse, dict]:
        """
        Publish a public video to an owned account.

        :param business_id: Application specific unique identifier for the TikTok account.
        :param video_url: A publicly accessible HTTP(s) URL for the video content to be published -
            with a minimum recommended TTL of 30 minutes.
        :param post_info: Required field.
            Pass empty object if not using caption, disable_comment, disable_duet or disable_stitch.
        :param return_json:
        :return:
        """
        post_info = {} if post_info is None else post_info
        data = {
            "business_id": business_id,
            "video_url": video_url,
            "post_info": post_info,
        }
        resp = self._request(verb="POST", path="business/videos/publish/", json=data)
        data = self.parse_response(resp)
        return (
            data
            if return_json
            else mds.BusinessVideoPublishResponse.new_from_json_dict(data)
        )

    def get_video_comments(
        self,
        business_id: str,
        video_id: str,
        status: Optional[str] = None,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
        cursor: Optional[int] = None,
        max_count: Optional[int] = None,
        return_json: bool = False,
    ) -> Union[mds.BusinessCommentsResponse, dict]:
        """
        Access all the comments (along with related information) - both public and hidden -
        that have been created against a specific organic video posted by an owned business account.

        :param business_id: Application specific unique identifier for the TikTok account.
        :param video_id: Unique identifier for owned TikTok video to list comments on.
        :param status: Enumerated status of comment visibility. ["PUBLIC", "ALL"]
        :param sort_field: Specific field to sort comments by. ["create_time", "likes", "replies"]
        :param sort_order: Specific field to sort comments by. ["asc", "desc"]
        :param cursor: Cursor for pagination.
        :param max_count: The maximum number of comments that will be returned for each page of data. [0...30]
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Video's comments data.
        """
        data = {"business_id": business_id, "video_id": video_id}
        if status is not None:
            data["status"] = status
        if sort_field is not None:
            data["sort_field"] = sort_field
        if sort_order is not None:
            data["sort_order"] = sort_order
        if cursor is not None:
            data["cursor"] = cursor
        if max_count is not None:
            data["max_count"] = max_count

        resp = self._request(verb="POST", path="business/comments/list/", json=data)
        data = self.parse_response(resp)
        return (
            data
            if return_json
            else mds.BusinessCommentsResponse.new_from_json_dict(data)
        )

    def get_comment_replies(
        self,
        business_id: str,
        video_id: str,
        comment_id: str,
        status: Optional[str] = None,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = None,
        cursor: Optional[int] = None,
        max_count: Optional[int] = None,
        return_json: bool = False,
    ) -> Union[mds.BusinessCommentsResponse, dict]:
        """
        Access all replies to a specific comment (along with related information) - both public and hidden -
        that have been created against a comment on an organic video posted by an owned business account.

        :param business_id: Application specific unique identifier for the TikTok account.
        :param video_id: Unique identifier for owned TikTok video to list comments on.
        :param comment_id: Unique identifier for comment on an owned TikTok video to list replies on.
        :param status: Enumerated status of comment visibility. ["PUBLIC", "ALL"]
        :param sort_field: Specific field to sort comments by. ["create_time", "likes", "replies"]
        :param sort_order: Specific field to sort comments by. ["asc", "desc"]
        :param cursor: Cursor for pagination.
        :param max_count: The maximum number of comments that will be returned for each page of data. [0...30]
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Comment's replies data.
        """
        data = {
            "business_id": business_id,
            "video_id": video_id,
            "comment_id": comment_id,
        }
        if status is not None:
            data["status"] = status
        if sort_field is not None:
            data["sort_field"] = sort_field
        if sort_order is not None:
            data["sort_order"] = sort_order
        if cursor is not None:
            data["cursor"] = cursor
        if max_count is not None:
            data["max_count"] = max_count

        resp = self._request(
            verb="POST", path="business/comments/replies/list/", json=data
        )
        data = self.parse_response(resp)
        return (
            data
            if return_json
            else mds.BusinessCommentsResponse.new_from_json_dict(data)
        )

    def create_comment(
        self, business_id: str, video_id: str, text: str, return_json: bool = False
    ) -> Union[mds.BusinessCommentResponse, dict]:
        """
        :param business_id: Application specific unique identifier for the TikTok account.
        :param video_id: Unique identifier for owned TikTok video to create comments on.
        :param text: Text content of the comment to create. Max length of 150 characters.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Comment's data.
        """
        data = {"business_id": business_id, "video_id": video_id, "text": text}
        resp = self._request(verb="POST", path="business/comments/create/", json=data)
        data = self.parse_response(resp)
        return (
            data
            if return_json
            else mds.BusinessCommentResponse.new_from_json_dict(data)
        )

    def create_reply(
        self,
        business_id: str,
        video_id: str,
        comment_id: str,
        text: str,
        return_json: bool = False,
    ) -> Union[mds.BusinessCommentResponse, dict]:
        """
        :param business_id: Application specific unique identifier for the TikTok account.
        :param video_id: Unique identifier for owned TikTok video to create comments on.
        :param comment_id: Unique identifier for comment on an owned TikTok video to create reply on.
        :param text: Text content of the comment to create. Max length of 150 characters.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Comment's data.
        """
        data = {
            "business_id": business_id,
            "video_id": video_id,
            "comment_id": comment_id,
            "text": text,
        }
        resp = self._request(
            verb="POST", path="business/comments/replies/create/", json=data
        )
        data = self.parse_response(resp)
        return (
            data
            if return_json
            else mds.BusinessCommentResponse.new_from_json_dict(data)
        )

    def like_comment(
        self,
        business_id: str,
        comment_id: str,
        action: str = "like",
        return_json: bool = False,
    ) -> Union[mds.BusinessBaseResponse, dict]:
        """
        Like/unlike an existing comment on an organic video posted by an owned business account.

        :param business_id: Application specific unique identifier for the TikTok account.
        :param comment_id: Unique identifier for comment on an owned TikTok video to like/unlike.
        :param action: Specific operation to be performed on the comment. ["like", "unlike"].
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Comment like status response.
        """
        data = {"business_id": business_id, "comment_id": comment_id, "action": action}
        resp = self._request(verb="POST", path="business/comments/like/", json=data)
        data = self.parse_response(resp)
        return (
            data if return_json else mds.BusinessBaseResponse.new_from_json_dict(data)
        )

    def pin_comment(
        self,
        business_id: str,
        comment_id: str,
        action: str = "pin",
        return_json: bool = False,
    ) -> Union[mds.BusinessBaseResponse, dict]:
        """
        Pin/unpin an existing comment on an organic video posted by an owned business account.

        :param business_id: Application specific unique identifier for the TikTok account.
        :param comment_id: Unique identifier for comment on an owned TikTok video to pin/unpin.
        :param action: Specific operation to be performed on the comment. ["pin", "unpin"].
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Comment pin status response.
        """
        data = {"business_id": business_id, "comment_id": comment_id, "action": action}
        resp = self._request(verb="POST", path="business/comments/like/", json=data)
        data = self.parse_response(resp)
        return (
            data if return_json else mds.BusinessBaseResponse.new_from_json_dict(data)
        )

    def hide_comment(
        self,
        business_id: str,
        comment_id: str,
        action: str = "hide",
        return_json: bool = False,
    ) -> Union[mds.BusinessBaseResponse, dict]:
        """
        Hide/unhide an existing comment on an organic video posted by an owned business account.

        :param business_id: Application specific unique identifier for the TikTok account.
        :param comment_id: Unique identifier for comment on an owned TikTok video to like/unlike.
        :param action: Specific operation to be performed on the comment. ["hide", "unhide"].
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Comment hide status response.
        """
        data = {"business_id": business_id, "comment_id": comment_id, "action": action}
        resp = self._request(verb="POST", path="business/comments/hide/", json=data)
        data = self.parse_response(resp)
        return (
            data if return_json else mds.BusinessBaseResponse.new_from_json_dict(data)
        )

    def delete_comment(
        self, business_id: str, comment_id: str, return_json: bool = False
    ) -> Union[mds.BusinessBaseResponse, dict]:
        """
        Delete an owned comment on an organic video posted by an owned business account.

        :param business_id: Application specific unique identifier for the TikTok account.
        :param comment_id: Unique identifier for comment on an owned TikTok video to like/unlike.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Comment delete status response.
        """
        data = {"business_id": business_id, "comment_id": comment_id}
        resp = self._request(verb="POST", path="business/comments/delete/", json=data)
        data = self.parse_response(resp)
        return (
            data if return_json else mds.BusinessBaseResponse.new_from_json_dict(data)
        )
