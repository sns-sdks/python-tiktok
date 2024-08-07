## Video Data

You can get account video data or publish video for account.

### Get Account Videos

```python
api.get_account_videos(business_id="Your business id", return_json=True)
# Response: {'code':0,'message':'OK','request_id':'2022070107152301000200300500600300009C51712','data':{'has_more':False,'cursor':1655118106000,'videos':[{'item_id':'7109065174526479622'},{'item_id':'7109064881462152453'},{'item_id':'7108684822863760646'},{'item_id':'7108678102229781766'}]}}
```

### Get Account Video by filter videos

```python
api.get_account_videos(
    business_id="Your business id",
    filters={"video_ids": ["7108684822863760646", "7109064881462152453"]}, 
    return_json=True
)
# Response: {'code':0,'message':'OK','request_id':'20220701071724010004003007735002053068B3FD9','data':{'videos':[{'item_id':'7108684822863760646'},{'item_id':'7109064881462152453'}],'has_more':False,'cursor':0}}
```

### Publish public video

Publish a video to your account, you need have video url(A publicly accessible HTTP(s) URL for the video content to be
published - with a minimum recommended TTL of 30 minutes).

```python
api.create_video(
    business_id="Your business id", video_url="https://s3.amazonaws.com/tiktok-videos/video.mp4",
    post_info={
        "caption": "Caption for video",
        "disable_comment": False,
        "disable_duet": False,
        "disable_stitch": False,
    },
    return_json=True
)
# Response: {"code":0,"message":"Ok","request_id":"20210817034316010245031056097316BA","data":{"share_id":"videopublish.8111673464968467978"}}
```

### Publish photo post

Publish a photo post to an owned TikTok Account.

```python
api.create_photo(
    business_id="business id",
    photo_images=[
        "https://example.com/photo1.jpg",
        "https://example.com/photo2.jpg",
        "https://example.com/photo3.jpg"
    ],
    post_info={
        "privacy_level": "PUBLIC_TO_EVERYONE",
        "title": "Photo post title",
        "auto_add_music": True
    }
)
# Response: {"code":0,"message":"Ok","request_id":"20210817034316010245031056097316BA","data":{"share_id":"p_pub_url~v1.2345123456789123456"}}
```

Now your video or photo post has submitted to TikTok, Once video or photo post been processed, video publish status will send by webhook.

More see [Video Webhook events](https://business-api.tiktok.com/portal/docs?id=1759992576757762), [Photo Webhook events](https://business-api.tiktok.com/portal/docs?id=1803634363436034).
