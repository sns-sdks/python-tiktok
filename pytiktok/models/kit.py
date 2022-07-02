"""
    Models for TikTok kit api.
"""
from dataclasses import dataclass, field
from typing import Optional, List

from .base import BaseModel


@dataclass
class KitAccessToken(BaseModel):
    """
    Refer: https://developers.tiktok.com/doc/login-kit-manage-user-access-tokens
    """

    open_id: Optional[str] = field(default=None)
    access_token: Optional[str] = field(default=None)
    scope: Optional[str] = field(default=None)
    expires_in: Optional[int] = field(default=None, repr=False)
    refresh_token: Optional[str] = field(default=None, repr=False)
    refresh_expires_in: Optional[int] = field(default=None, repr=False)
    captcha: Optional[str] = field(default=None, repr=False)
    desc_url: Optional[str] = field(default=None, repr=False)
    description: Optional[str] = field(default=None, repr=False)
    error_code: Optional[int] = field(default=None)
    log_id: Optional[str] = field(default=None, repr=False)


@dataclass
class KitAccessTokenResponse(BaseModel):
    data: Optional[KitAccessToken] = field(default=None)
    message: Optional[str] = field(default=None)


@dataclass
class KitQrCodeData(BaseModel):
    scan_qrcode_url: Optional[str] = field(default=None)
    token: Optional[str] = field(default=None)
    status: Optional[str] = field(default=None)
    client_ticket: Optional[str] = field(default=None)
    redirect_url: Optional[str] = field(default=None)
    error_code: Optional[int] = field(default=None)
    description: Optional[str] = field(default=None)


@dataclass
class KitResponseExtra(BaseModel):
    error_detail: Optional[str] = field(default=None)
    logid: Optional[int] = field(default=None)


@dataclass
class KitQrCodeResponse(BaseModel):
    """
    Refer: https://developers.tiktok.com/doc/login-kit-qr-code-authorization
    """

    data: Optional[KitQrCodeData] = field(default=None)
    extra: Optional[KitResponseExtra] = field(default=None)
    message: Optional[str] = field(default=None)


@dataclass
class KitUser(BaseModel):
    """
    Refer: https://developers.tiktok.com/doc/login-kit-user-info-basic
    """

    open_id: Optional[str] = field(default=None)
    union_id: Optional[str] = field(default=None)
    display_name: Optional[str] = field(default=None)
    avatar_url: Optional[str] = field(default=None)
    avatar_url_100: Optional[str] = field(default=None, repr=False)
    avatar_url_200: Optional[str] = field(default=None, repr=False)
    avatar_large_url: Optional[str] = field(default=None, repr=False)


@dataclass
class KitResponseError(BaseModel):
    code: Optional[int] = field(default=None)
    message: Optional[str] = field(default=None)
    log_id: Optional[str] = field(default=None, repr=False)


@dataclass
class KitUserData(BaseModel):
    user: Optional[KitUser] = field(default=None)


@dataclass
class KitUserResponse(BaseModel):
    data: Optional[KitUserData] = field(default=None)
    error: Optional[KitResponseError] = field(default=None)


@dataclass
class KitVideo(BaseModel):
    """
    Refer: https://developers.tiktok.com/doc/login-kit-video-list
    """

    id: Optional[str] = field(default=None)
    create_time: Optional[int] = field(default=None)
    cover_image_url: Optional[str] = field(default=None, repr=False)
    share_url: Optional[str] = field(default=None, repr=False)
    video_description: Optional[str] = field(default=None, repr=False)
    duration: Optional[int] = field(default=None, repr=False)
    height: Optional[int] = field(default=None, repr=False)
    width: Optional[int] = field(default=None, repr=False)
    title: Optional[str] = field(default=None, repr=False)
    embed_html: Optional[str] = field(default=None, repr=False)
    embed_link: Optional[str] = field(default=None, repr=False)
    like_count: Optional[int] = field(default=None, repr=False)
    comment_count: Optional[int] = field(default=None, repr=False)
    share_count: Optional[int] = field(default=None, repr=False)
    view_count: Optional[int] = field(default=None, repr=False)


@dataclass
class KitVideosData(BaseModel):
    videos: Optional[List[KitVideo]] = field(default=None)
    cursor: Optional[int] = field(default=None)
    has_more: Optional[bool] = field(default=None)


@dataclass
class KitVideosResponse(BaseModel):
    data: Optional[KitVideosData] = field(default=None)
    error: Optional[KitResponseError] = field(default=None)


@dataclass
class KitShareVideoData(BaseModel):
    share_id: Optional[str] = field(default=None)
    error_code: Optional[int] = field(default=None)
    error_msg: Optional[KitVideosData] = field(default=None, repr=False)
    err_code: Optional[int] = field(default=None, repr=False)


@dataclass
class KitShareVideoResponse(BaseModel):
    data: Optional[KitShareVideoData] = field(default=None)
    extra: Optional[KitResponseExtra] = field(default=None)
