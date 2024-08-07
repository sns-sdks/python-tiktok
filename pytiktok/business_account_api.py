"""
    Core API impl.
"""

from typing import Optional, List, Union

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
        api_version: Optional[str] = "v1.3",
        oauth_redirect_uri: Optional[str] = None,
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

        # oauth redirect uri
        # Must be the same as the TikTok account holder redirect URL set in the app.
        self.oauth_redirect_uri = oauth_redirect_uri

    def generate_access_token(
        self, code: str, redirect_uri: Optional[str] = None, return_json: bool = False
    ) -> Union[mds.BusinessAccessToken, dict]:
        """
        Generate access token by the auth code.
        :param code: The authorization code you get from the creator
        :param redirect_uri: The redirect URL which the client will be directed to.
            Its value must be the same as the TikTok account holder redirect URL set in the app.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Access Token
        """
        redirect_uri = redirect_uri or self.oauth_redirect_uri

        if not self.app_id or not self.app_secret or not redirect_uri:
            raise PyTiktokError(f"Need app id, app secret and redirect_uri.")

        resp = self._request(
            verb="POST",
            path="tt_user/oauth2/token/",
            json={
                "client_id": self.app_id,
                "client_secret": self.app_secret,
                "grant_type": "authorization_code",
                "auth_code": code,
                "redirect_uri": redirect_uri,
            },
            enforce_auth=False,
        )

        data = self.parse_response(response=resp)
        data = data["data"]
        self.access_token = data["access_token"]
        return data if return_json else mds.BusinessAccessToken.new_from_json_dict(data)

    def refresh_access_token(
        self, refresh_token: str, return_json: bool = False
    ) -> Union[mds.BusinessAccessToken, dict]:
        """
        Use this endpoint to renew an access token by refresh_token.
        :param refresh_token: Refresh token,
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Access Token
        """
        if not self.app_id or not self.app_secret:
            raise PyTiktokError(f"Need app id and app secret.")
        resp = self._request(
            verb="POST",
            path="tt_user/oauth2/refresh_token/",
            json={
                "client_id": self.app_id,
                "client_secret": self.app_secret,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
            },
            enforce_auth=False,
        )

        data = self.parse_response(response=resp)
        data = data["data"]
        self.access_token = data["access_token"]
        return data if return_json else mds.BusinessAccessToken.new_from_json_dict(data)

    def revoke_access_token(self, access_token: str, return_json: bool = False) -> dict:
        if not self.app_id or not self.app_secret:
            raise PyTiktokError(f"Need app id and app secret.")
        resp = self._request(
            verb="POST",
            path="tt_user/oauth2/revoke/",
            json={
                "client_id": self.app_id,
                "client_secret": self.app_secret,
                "access_token": access_token,
            },
            enforce_auth=False,
        )

        data = self.parse_response(response=resp)
        return (
            data
            if return_json
            else mds.BusinessAccessTokenRevokeResponse.new_from_json_dict(data)
        )

    def get_token_info(
        self, access_token: str, app_id: Optional[str] = None, return_json: bool = False
    ) -> Union[mds.BusinessAccessTokenInfo, dict]:
        """
        Get the permission scopes of a TikTok Business Account or a TikTok Personal Account that are authorized by the TikTok account user.
        :param access_token: Access token authorized by TikTok Creator Marketplace accounts.
        :param app_id: ID of your developer application.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Access token info.
        """
        app_id = app_id or self.app_id
        if not app_id:
            raise PyTiktokError(f"Need app id.")

        resp = self._request(
            verb="POST",
            path="tt_user/token_info/get/",
            json={
                "app_id": app_id,
                "access_token": access_token,
            },
            enforce_auth=False,
        )

        data = self.parse_response(response=resp)
        data = data["data"]
        return (
            data
            if return_json
            else mds.BusinessAccessTokenInfo.new_from_json_dict(data)
        )

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
            response.close()
        except ValueError:
            raise PyTiktokError(f"Unknown error: {response.content}")

        # error handler
        if "code" in data and data["code"] != 0:
            raise PyTiktokError(data)

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
        params = {"business_id": business_id}
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        if fields is not None:
            params["fields"] = fields

        resp = self._request(path="business/get/", params=params)
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

        params = {"business_id": business_id}
        if fields is not None:
            params["fields"] = fields
        if filters is not None:
            params["filters"] = filters
        if cursor is not None:
            params["cursor"] = cursor
        if max_count is not None:
            params["max_count"] = max_count
        resp = self._request(
            path="business/video/list/",
            params=params,
        )
        data = self.parse_response(resp)
        return (
            data if return_json else mds.BusinessVideosResponse.new_from_json_dict(data)
        )

    def create_video(
        self,
        business_id: str,
        video_url: str,
        post_info: dict,
        return_json: bool = False,
    ) -> Union[mds.BusinessVideoPublishResponse, dict]:
        """
        Publish a public video to an owned account.

        :param business_id: Application specific unique identifier for the TikTok account.
        :param video_url: A publicly accessible HTTP(s) URL for the video content to be published -
            with a minimum recommended TTL of 30 minutes.
        :param post_info: Required field.
            Pass empty object if not using caption, disable_comment, disable_duet or disable_stitch.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Video publish response.
        """
        data = {
            "business_id": business_id,
            "video_url": video_url,
            "post_info": post_info,
        }

        resp = self._request(verb="POST", path="business/video/publish/", json=data)
        data = self.parse_response(resp)
        return (
            data
            if return_json
            else mds.BusinessVideoPublishResponse.new_from_json_dict(data)
        )

    def create_photo(
        self,
        business_id: str,
        photo_images: List[str],
        post_info: dict,
        photo_cover_index: int = 0,
        return_json: bool = False,
    ) -> Union[mds.BusinessPhotoPublishResponse, dict]:
        """
        Publish a photo post to an owned TikTok Account.
        :param business_id: Application specific unique identifier for the TikTok account.
        :param photo_images: A list of up to 35 publicly accessible HTTP(s) URLs for the photo content to be published.
        :param post_info: Information about the photo post.
            - privacy_level is Required field.
            - Other fields are optional
        :param photo_cover_index: The index of the photo to be used as the cover for the post.
            O is the first photo.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Photo publish response.
        """

        data = {
            "business_id": business_id,
            "photo_images": photo_images,
            "photo_cover_index": photo_cover_index,
            "post_info": post_info,
        }
        resp = self._request(verb="POST", path="business/photo/publish/", json=data)
        data = self.parse_response(resp)
        return (
            data
            if return_json
            else mds.BusinessPhotoPublishResponse.new_from_json_dict(data)
        )

    def get_video_comments(
        self,
        business_id: str,
        video_id: str,
        comment_ids: Optional[List[str]] = None,
        include_replies: Optional[bool] = None,
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
        :param comment_ids: A list of IDs for comments or comment replies that you want to filter the results by.
            Max size: 30.
        :param include_replies: Whether to include replies to the top-level comments in the results. Max size 3.
        :param status: Enumerated status of comment visibility. ["PUBLIC", "ALL"]
        :param sort_field: Specific field to sort comments by. ["create_time", "likes", "replies"]
        :param sort_order: Specific field to sort comments by. ["asc", "desc"]
        :param cursor: Cursor for pagination.
        :param max_count: The maximum number of comments that will be returned for each page of data. [0...30]
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Video's comments data.
        """
        params = {"business_id": business_id, "video_id": video_id}
        if comment_ids is not None:
            params["comment_ids"] = comment_ids
        if include_replies is not None:
            params["include_replies"] = include_replies
        if status is not None:
            params["status"] = status
        if sort_field is not None:
            params["sort_field"] = sort_field
        if sort_order is not None:
            params["sort_order"] = sort_order
        if cursor is not None:
            params["cursor"] = cursor
        if max_count is not None:
            params["max_count"] = max_count

        resp = self._request(verb="GET", path="business/comment/list/", params=params)
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
        :param sort_order: Specific field to sort comments by. ["asc", "desc", "smart"]
        :param cursor: Cursor for pagination.
        :param max_count: The maximum number of comments that will be returned for each page of data. [0...30]
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Comment's replies data.
        """
        params = {
            "business_id": business_id,
            "video_id": video_id,
            "comment_id": comment_id,
        }
        if status is not None:
            params["status"] = status
        if sort_field is not None:
            params["sort_field"] = sort_field
        if sort_order is not None:
            params["sort_order"] = sort_order
        if cursor is not None:
            params["cursor"] = cursor
        if max_count is not None:
            params["max_count"] = max_count

        resp = self._request(
            verb="GET", path="business/comment/reply/list/", params=params
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

        resp = self._request(verb="POST", path="business/comment/create/", json=data)
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
            verb="POST", path="business/comment/reply/create/", json=data
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
        action: str = "LIKE",
        return_json: bool = False,
    ) -> Union[mds.BusinessBaseResponse, dict]:
        """
        Like/unlike an existing comment on an organic video posted by an owned business account.

        :param business_id: Application specific unique identifier for the TikTok account.
        :param comment_id: Unique identifier for comment on an owned TikTok video to like/unlike.
        :param action: Specific operation to be performed on the comment. ["LIKE", "UNLIKE"].
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Comment like status response.
        """
        data = {"business_id": business_id, "comment_id": comment_id, "action": action}
        resp = self._request(verb="POST", path="business/comment/like/", json=data)
        data = self.parse_response(resp)
        return (
            data if return_json else mds.BusinessBaseResponse.new_from_json_dict(data)
        )

    def pin_comment(
        self,
        business_id: str,
        video_id: str,
        comment_id: str,
        action: str = "PIN",
        return_json: bool = False,
    ) -> Union[mds.BusinessBaseResponse, dict]:
        """
        Pin/unpin an existing comment on an organic video posted by an owned business account.

        :param business_id: Application specific unique identifier for the TikTok account.
        :param video_id: Unique identifier for owned TikTok video to create comments on.
        :param comment_id: Unique identifier for comment on an owned TikTok video to pin/unpin.
        :param action: Specific operation to be performed on the comment. ["PIN", "UNPIN"].
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Comment pin status response.
        """
        data = {
            "business_id": business_id,
            "video_id": video_id,
            "comment_id": comment_id,
            "action": action,
        }
        resp = self._request(verb="POST", path="business/comment/pin/", json=data)
        data = self.parse_response(resp)
        return (
            data if return_json else mds.BusinessBaseResponse.new_from_json_dict(data)
        )

    def hide_comment(
        self,
        business_id: str,
        video_id: str,
        comment_id: str,
        action: str = "HIDE",
        return_json: bool = False,
    ) -> Union[mds.BusinessBaseResponse, dict]:
        """
        Hide/unhide an existing comment on an organic video posted by an owned business account.

        :param business_id: Application specific unique identifier for the TikTok account.
        :param video_id: Unique identifier for owned TikTok video to create comments on.
        :param comment_id: Unique identifier for comment on an owned TikTok video to hide/unhide.
        :param action: Specific operation to be performed on the comment. ["HIDE", "UNHIDE"].
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Comment hide status response.
        """
        data = {
            "business_id": business_id,
            "video_id": video_id,
            "comment_id": comment_id,
            "action": action,
        }
        resp = self._request(verb="POST", path="business/comment/hide/", json=data)
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
        resp = self._request(verb="POST", path="business/comment/delete/", json=data)
        data = self.parse_response(resp)
        return (
            data if return_json else mds.BusinessBaseResponse.new_from_json_dict(data)
        )

    def get_hashtag_suggestions(
        self,
        business_id: str,
        keyword: str,
        language: str = "en",
        return_json: bool = False,
    ) -> Union[dict, mds.BusinessHashtagSuggestionResponse]:
        """Specify a keyword and get a list of recommended hashtags to be used for your Business Account videos.

        :param business_id: Application specific unique identifier for the TikTok account.
        :param keyword: The keyword that you want to get recommended hashtags for.
        :param language: Keyword language.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: Suggestion hashtags.
        """
        data = {
            "business_id": business_id,
            "keyword": keyword,
            "language": language,
        }
        resp = self._request(
            verb="GET", path="business/hashtag/suggestion/", params=data
        )
        data = self.parse_response(resp)
        return (
            data
            if return_json
            else mds.BusinessHashtagSuggestionResponse.new_from_json_dict(data)
        )

    def add_url_property(
        self,
        app_id: str,
        property_type: int,
        url: str,
        return_json: bool = False,
    ) -> Union[mds.BusinessUrlPropertyInfoResponse, dict]:
        """
        Add a URL property (domain or URL prefix) that you want to verify ownership of, to an advertiser account.
        :param app_id: ID of your developer application.
        :param property_type: Type of the URL property.
            - 1: Domain
            - 2: URL prefix
        :param url: An owned URL that you want to add.
            - If property_type is 1, specify a base domain or subdomain. ex: example.com.
            - If property_type is 2, specify a URL prefix which consists of:
                https:// + host (must be a domain) + path + /. ex: https://example.com/folder/.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: URL property info.
        """
        data = {
            "app_id": app_id,
            "url_property_meta": {
                "property_type": property_type,
                "url": url,
            },
        }
        resp = self._request(verb="POST", path="business/property/add/", json=data)
        data = self.parse_response(resp)
        return (
            data
            if return_json
            else mds.BusinessUrlPropertyInfoResponse.new_from_json_dict(data)
        )

    def check_url_property_verification(
        self,
        app_id: str,
        property_type: int,
        url: str,
        return_json: bool = False,
    ) -> Union[mds.BusinessUrlPropertyInfoResponse, dict]:
        """
        Check the result of the ownership verification for a URL property (domain or URL prefix).
        :param app_id: ID of your developer application.
        :param property_type: Type of the URL property.
            - 1: Domain
            - 2: URL prefix
        :param url: An owned URL that you want to add.
            - If property_type is 1, specify a base domain or subdomain. ex: example.com.
            - If property_type is 2, specify a URL prefix which consists of:
                https:// + host (must be a domain) + path + /. ex: https://example.com/folder/.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: URL property verification info.
        """
        data = {
            "app_id": app_id,
            "url_property_meta": {
                "property_type": property_type,
                "url": url,
            },
        }
        resp = self._request(verb="POST", path="business/property/verify/", json=data)
        data = self.parse_response(resp)
        return (
            data
            if return_json
            else mds.BusinessUrlPropertyInfoResponse.new_from_json_dict(data)
        )

    def delete_url_property(
        self,
        app_id: str,
        property_type: int,
        url: str,
        return_json: bool = False,
    ) -> Union[mds.BusinessBaseResponse, dict]:
        """
        Check the result of the ownership verification for a URL property (domain or URL prefix).
        :param app_id: ID of your developer application.
        :param property_type: Type of the URL property.
            - 1: Domain
            - 2: URL prefix
        :param url: An owned URL that you want to add.
            - If property_type is 1, specify a base domain or subdomain. ex: example.com.
            - If property_type is 2, specify a URL prefix which consists of:
                https:// + host (must be a domain) + path + /. ex: https://example.com/folder/.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: url property delete status response
        """
        data = {
            "app_id": app_id,
            "url_property_meta": {
                "property_type": property_type,
                "url": url,
            },
        }
        resp = self._request(verb="POST", path="business/property/delete/", json=data)
        data = self.parse_response(resp)
        return (
            data if return_json else mds.BusinessBaseResponse.new_from_json_dict(data)
        )

    def get_url_property_list(
        self,
        app_id: str,
        return_json: bool = False,
    ) -> Union[mds.BusinessUrlPropertyInfoListResponse, dict]:
        """
        Get the list of URL properties that have been added to an advertiser account.
        :param app_id: ID of your developer application.
        :param return_json: Type for returned data. If you set True JSON data will be returned.
        :return: URL property list response
        """
        params = {"app_id": app_id}
        resp = self._request(verb="GET", path="business/property/list/", params=params)
        data = self.parse_response(resp)
        return (
            data
            if return_json
            else mds.BusinessUrlPropertyInfoListResponse.new_from_json_dict(data)
        )
