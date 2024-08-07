"""
    Models for business account.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseModel


@dataclass
class BusinessBaseResponse(BaseModel):
    code: Optional[int] = field(default=None)
    message: Optional[str] = field(default=None)
    request_id: Optional[str] = field(default=None)


@dataclass
class BusinessAccessToken(BaseModel):
    """
    Refer:
        v1.2: https://ads.tiktok.com/marketing_api/docs?id=1733224966619138
        v1.3: https://business-api.tiktok.com/portal/docs?id=1738084387220481
    """

    access_token: Optional[str] = field(default=None)
    token_type: Optional[str] = field(default=None)
    scope: Optional[str] = field(default=None, repr=False)
    expires: Optional[int] = field(default=None, repr=False)
    expires_in: Optional[int] = field(default=None, repr=False)
    refresh_token: Optional[str] = field(default=None, repr=False)
    refresh_expires: Optional[int] = field(default=None, repr=False)
    refresh_token_expires_in: Optional[int] = field(default=None, repr=False)
    creator_id: Optional[str] = field(default=None, repr=False)
    open_id: Optional[str] = field(default=None, repr=False)


@dataclass
class BusinessAccessTokenInfo(BaseModel):
    """
    Refer: https://business-api.tiktok.com/portal/docs?id=1765927978092545
    """

    app_id: Optional[str] = field(default=None)
    creator_id: Optional[str] = field(default=None)
    scope: Optional[str] = field(default=None)


class BusinessAccessTokenRevokeResponse(BusinessBaseResponse):
    """
    Refer: https://business-api.tiktok.com/portal/docs?id=1738084387220481
    """

    ...


@dataclass
class BusinessAccountAudienceCountry(BaseModel):
    country: Optional[str] = field(default=None)
    percentage: Optional[float] = field(default=None)


@dataclass
class BusinessAccountAudienceGender(BaseModel):
    gender: Optional[str] = field(default=None)
    percentage: Optional[float] = field(default=None)


@dataclass
class BusinessAccountMetricAudienceActivity(BaseModel):
    hour: Optional[str] = field(default=None)
    count: Optional[int] = field(default=None)


@dataclass
class BusinessAccountMetric(BaseModel):
    date: Optional[str] = field(default=None)
    followers_count: Optional[int] = field(default=None)
    profile_views: Optional[int] = field(default=None)
    video_views: Optional[int] = field(default=None)
    likes: Optional[int] = field(default=None)
    comments: Optional[int] = field(default=None)
    shares: Optional[int] = field(default=None)
    audience_activity: Optional[List[BusinessAccountMetricAudienceActivity]] = field(
        default=None, repr=False
    )


@dataclass
class BusinessAccount(BaseModel):
    """
    Refer: https://business-api.tiktok.com/portal/docs?id=1762228399168514
    """

    is_business_account: Optional[bool] = field(default=None)
    username: Optional[str] = field(default=None)
    display_name: Optional[str] = field(default=None)
    profile_image: Optional[str] = field(default=None)
    followers_count: Optional[int] = field(default=None)
    audience_countries: Optional[List[BusinessAccountAudienceCountry]] = field(
        default=None, repr=False
    )
    audience_genders: Optional[List[BusinessAccountAudienceGender]] = field(
        default=None, repr=False
    )
    metrics: Optional[List[BusinessAccountMetric]] = field(default=None, repr=False)


@dataclass
class BusinessAccountResponse(BusinessBaseResponse):
    data: Optional[BusinessAccount] = field(default=None)


@dataclass
class BusinessVideoImpressionSource(BaseModel):
    impression_source: Optional[str] = field(default=None)
    percentage: Optional[float] = field(default=None)


@dataclass
class BusinessVideoAudienceCountry(BaseModel):
    country: Optional[str] = field(default=None)
    percentage: Optional[float] = field(default=None)


@dataclass
class BusinessVideo(BaseModel):
    """
    Refer: https://ads.tiktok.com/marketing_api/docs?id=1733327057319937
    """

    item_id: Optional[str] = field(default=None)
    create_time: Optional[str] = field(default=None)
    thumbnail_url: Optional[str] = field(default=None, repr=False)
    share_url: Optional[str] = field(default=None, repr=False)
    embed_url: Optional[str] = field(default=None, repr=False)
    caption: Optional[str] = field(default=None)
    video_views: Optional[int] = field(default=None, repr=False)
    video_duration: Optional[float] = field(default=None, repr=False)
    likes: Optional[int] = field(default=None, repr=False)
    comments: Optional[int] = field(default=None, repr=False)
    shares: Optional[int] = field(default=None, repr=False)
    reach: Optional[int] = field(default=None, repr=False)
    full_video_watched_rate: Optional[float] = field(default=None, repr=False)
    total_time_watched: Optional[float] = field(default=None, repr=False)
    average_time_watched: Optional[float] = field(default=None, repr=False)
    impression_sources: Optional[BusinessVideoImpressionSource] = field(
        default=None, repr=False
    )
    audience_countries: Optional[List[BusinessVideoAudienceCountry]] = field(
        default=None, repr=False
    )


@dataclass
class BusinessVideosData(BaseModel):
    videos: Optional[List[BusinessVideo]] = field(default=None)
    cursor: Optional[int] = field(default=None)
    has_more: Optional[bool] = field(default=None)


@dataclass
class BusinessVideosResponse(BusinessBaseResponse):
    data: Optional[BusinessVideosData] = field(default=None)


@dataclass
class BusinessVideoPublish(BaseModel):
    """
    Refer: https://ads.tiktok.com/marketing_api/docs?id=1733584024973313
    """

    share_id: Optional[str] = field(default=None)


@dataclass
class BusinessVideoPublishResponse(BusinessBaseResponse):
    data: Optional[BusinessVideoPublish] = field(default=None)


@dataclass
class BusinessPhotoPublish(BusinessVideoPublish):
    """
    https://business-api.tiktok.com/portal/docs?id=1803630424390658
    """

    ...


@dataclass
class BusinessPhotoPublishResponse(BusinessBaseResponse):
    data: Optional[BusinessPhotoPublish] = field(default=None)


@dataclass
class BusinessComment(BaseModel):
    """
    Refer: https://ads.tiktok.com/marketing_api/docs?id=1733329505077250
    """

    comment_id: Optional[str] = field(default=None)
    unique_identifier: Optional[str] = field(default=None)
    video_id: Optional[str] = field(default=None, repr=False)
    # Note: user_id now is To-be-deprecated, will be deprecated in the next API version.
    # Please use unique_identifier instead.
    user_id: Optional[str] = field(default=None, repr=False)
    create_time: Optional[int] = field(default=None)
    text: Optional[str] = field(default=None)
    likes: Optional[int] = field(default=None, repr=False)
    replies: Optional[int] = field(default=None, repr=False)
    owner: Optional[bool] = field(default=None, repr=False)
    liked: Optional[bool] = field(default=None, repr=False)
    pinned: Optional[bool] = field(default=None, repr=False)
    status: Optional[str] = field(default=None, repr=False)
    username: Optional[str] = field(default=None, repr=False)
    profile_image: Optional[str] = field(default=None, repr=False)
    parent_comment_id: Optional[str] = field(default=None)
    reply_list: Optional[List["BusinessComment"]] = field(default=None, repr=False)


@dataclass
class BusinessCommentsData(BaseModel):
    comments: Optional[List[BusinessComment]] = field(default=None)
    cursor: Optional[int] = field(default=None)
    has_more: Optional[bool] = field(default=None)


@dataclass
class BusinessCommentResponse(BusinessBaseResponse):
    data: Optional[BusinessComment] = field(default=None)


@dataclass
class BusinessCommentsResponse(BusinessBaseResponse):
    data: Optional[BusinessCommentsData] = field(default=None)


@dataclass
class BusinessHashtagSuggestion(BaseModel):
    name: Optional[str] = field(default=None)
    view_count: Optional[int] = field(default=None)


@dataclass
class BusinessHashtagSuggestionsData(BaseModel):
    suggestions: Optional[List[BusinessHashtagSuggestion]] = field(default=None)


@dataclass
class BusinessHashtagSuggestionResponse(BusinessBaseResponse):
    """
    Refer: https://ads.tiktok.com/marketing_api/docs?id=1749827124568130
    """

    data: Optional[BusinessHashtagSuggestionsData] = field(default=None)


@dataclass
class BusinessUrlPropertyInfo(BaseModel):
    """
    Refer: https://business-api.tiktok.com/portal/docs?id=1769325280876545
    """

    property_type: Optional[int] = field(default=None)
    url: Optional[str] = field(default=None)
    property_status: Optional[int] = field(default=None, repr=False)
    signature: Optional[str] = field(default=None, repr=False)
    file_name: Optional[str] = field(default=None, repr=False)


@dataclass
class BusinessUrlPropertyInfoData(BaseModel):
    url_property_info: Optional[BusinessUrlPropertyInfo] = field(default=None)


@dataclass
class BusinessUrlPropertyInfoResponse(BusinessBaseResponse):
    data: Optional[BusinessUrlPropertyInfoData] = field(default=None)


@dataclass
class BusinessUrlPropertyInfoListData(BaseModel):
    url_property_info_list: Optional[List[BusinessUrlPropertyInfo]] = field(
        default=None
    )


@dataclass
class BusinessUrlPropertyInfoListResponse(BusinessBaseResponse):
    data: Optional[BusinessUrlPropertyInfoListData] = field(default=None)
