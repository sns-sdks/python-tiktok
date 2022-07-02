## Video

### Get User videos 

Get a paginated list of given user's public TikTok video posts

```python
api.get_user_videos(open_id="Open id for user", return_json=True)
# Response: {'data':{'videos':[{'create_time':1654670085,'share_url':'https://www.tiktok.com/@klein_kunkun/video/7106753891953347842?utm_campaign=tt4d_open_api&utm_source=aw46lwwtsqjeapig','duration':5,'id':'7106753891953347842'},{'create_time':1654658105,'share_url':'https://www.tiktok.com/@klein_kunkun/video/7106702437926407426?utm_campaign=tt4d_open_api&utm_source=aw46lwwtsqjeapig','duration':6,'id':'7106702437926407426'}],'cursor':1654658105000,'has_more':False},'error':{'code':0,'message':''}}
```

### Query user videos

Given a user and a list of video ids, can check if the videos belong to the requesting user and fetch the data of videos belonging to the user. 

```python
api.query_videos(open_id="Open id for user", filters={"video_ids": ["7106753891953347842"]}, return_json=True)
# Response: {'data':{'videos':[{'create_time':1654670085,'share_url':'https://www.tiktok.com/@klein_kunkun/video/7106753891953347842?utm_campaign=tt4d_open_api&utm_source=aw46lwwtsqjeapig','duration':5,'id':'7106753891953347842'}],'cursor':0,'has_more':False},'error':{'code':0,'message':''}}
```

### Share Video for user

Share Video API allows users to share videos from your Web or Desktop app into TikTok.


```python

filename = "your mp4 file path"
with open(filename, "rb") as fb:
    response = api.share_video(open_id="Open id for user", video="Video file object")
# Response: {'data':{'err_code':0,'error_code':0,'share_id':'v_inbox.7115544584662829102'},'extra':{'error_detail':'','logid':'2022070206304301000400300500600301908104B50'}}
```
