"""
    Models for business account.
"""

from dataclasses import dataclass, field
from typing import List, Optional

from .base import BaseModel


class BaseResponse(BaseModel):
    code: int = field()
    message: str = field()
    request_id: str = field()


class AccessToken(BaseModel):
    """
    Refer: https://ads.tiktok.com/marketing_api/docs?id=1733224966619138
    """

    access_token: Optional[str] = field(default=None)
    token_type: Optional[str] = field(default=None)
    scope: Optional[str] = field(default=None, repr=False)
    expires: Optional[int] = field(default=None, repr=False)
    refresh_token: Optional[str] = field(default=None, repr=False)
    refresh_expires: Optional[int] = field(default=None, repr=False)
    creator_id: Optional[str] = field(default=None, repr=False)


class AccountAudienceCountry(BaseModel):
    country: Optional[str] = field(default=None)
    percentage: Optional[float] = field(default=None)


class AccountAudienceGender(BaseModel):
    gender: Optional[str] = field(default=None)
    percentage: Optional[float] = field(default=None)


class AccountMetricAudienceActivity(BaseModel):
    hour: Optional[str] = field(default=None)
    count: Optional[int] = field(default=None)


class AccountMetric(BaseModel):
    date: Optional[str] = field(default=None)
    followers_count: Optional[int] = field(default=None)
    profile_views: Optional[int] = field(default=None)
    video_views: Optional[int] = field(default=None)
    likes: Optional[int] = field(default=None)
    comments: Optional[int] = field(default=None)
    shares: Optional[int] = field(default=None)
    audience_activity: Optional[List[AccountMetricAudienceActivity]] = field(
        default=None, repr=False
    )


class Account(BaseModel):
    """
    Refer: https://ads.tiktok.com/marketing_api/docs?id=1733326495444994
    """

    username: Optional[str] = field(default=None)
    display_name: Optional[str] = field(default=None)
    profile_image: Optional[str] = field(default=None)
    followers_count: Optional[int] = field(default=None)
    audience_countries: Optional[List[AccountAudienceCountry]] = field(
        default=None, repr=False
    )
    audience_genders: Optional[List[AccountAudienceGender]] = field(
        default=None, repr=False
    )
    metrics: Optional[List[AccountMetric]] = field(default=None, repr=False)


class AccountResponse(BaseResponse):
    data: Optional[Account] = field(default=None)


class VideoImpressionSource(BaseModel):
    impression_source: Optional[str] = field(default=None)
    percentage: Optional[float] = field(default=None)


class VideoAudienceCountry(BaseModel):
    country: Optional[str] = field(default=None)
    percentage: Optional[float] = field(default=None)


class Video(BaseModel):
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
    impression_sources: Optional[VideoImpressionSource] = field(
        default=None, repr=False
    )
    audience_countries: Optional[List[VideoAudienceCountry]] = field(
        default=None, repr=False
    )


class VideosData(BaseModel):
    videos: Optional[Video] = field(default=None)
    cursor: Optional[int] = field(default=None)
    has_more: Optional[bool] = field(default=None)


class VideosResponse(BaseResponse):
    data: Optional[VideosData] = field(default=None)


class VideoPublish(BaseResponse):
    """
    Refer: https://ads.tiktok.com/marketing_api/docs?id=1733584024973313
    """

    share_id: Optional[str] = field(default=None)


class VideoPublishResponse(BaseResponse):
    data: Optional[VideoPublish] = field(default=None)


class Comment(BaseModel):
    """
    Refer: https://ads.tiktok.com/marketing_api/docs?id=1733329505077250
    """

    comment_id: Optional[str] = field(default=None)
    video_id: Optional[str] = field(default=None, repr=False)
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


class CommentsData(BaseModel):
    comments: Optional[Comment] = field(default=None)
    cursor: Optional[int] = field(default=None)
    has_more: Optional[bool] = field(default=None)


class CommentResponse(BaseResponse):
    data: Optional[Comment] = field(default=None)


class CommentsResponse(BaseResponse):
    data: Optional[CommentsData] = field(default=None)
