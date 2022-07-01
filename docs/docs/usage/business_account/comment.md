## Comment Data

There have simple usage for manage comments for videos.

### Get all comments on an owned video

```python
api.get_video_comments(business_id="Your business id", video_id="Your video id", return_json=True)
# Response: {'code':0,'message':'OK','request_id':'20220701072655010002007637004005006003006134680EF','data':{'has_more':False,'comments':[{'video_id':'7109065174526479622','liked':False,'pinned':False,'user_id':'367b786990e8dcebcf493e035b820f5be4834422511c851b3bd0010f9690adbc','text':'nice','replies':11,'username':'phoenix202312121','status':'PUBLIC','likes':0,'create_time':'1655461098','owner':False,'comment_id':'7110150495453840130','profile_image':'https://p16-sign-sg.tiktokcdn.com/tiktok-obj/1666477470268417~c5_168x168.jpeg?x-expires=1656831600&x-signature=W%2FAanEtkfRORbU141d2UeZQnxzc%3D'},{'video_id':'7109065174526479622','liked':False,'pinned':False,'user_id':'6faa870ee45c1f68a2d98d50e09f222a04069380c1032f1919f3ffe25be1f085','text':'xxxxxxxx','replies':0,'username':'klein_kunkun','status':'PUBLIC','likes':0,'create_time':'1655870005','owner':False,'comment_id':'7111907185164763905','profile_image':'https://p16-sign-sg.tiktokcdn.com/tiktok-obj/7046311066329939970~c5_168x168.jpeg?x-expires=1656831600&x-signature=9GsDTVTn9%2Bvb%2FFBkxZGaOlIkTM4%3D'}],'cursor':2}}
```

### Get all replies to a comment

```python
api.get_comment_replies(
    business_id="Your business id", video_id="Your video id",
    comment_id="Comment id", return_json=True
)
# Response: {'code':0,'message':'OK','request_id':'202207010730350100020060050050060030001099BEF5','data':{'has_more':False,'cursor':1,'comments':[{'profile_image':'https://p16-sign-sg.tiktokcdn.com/tiktok-obj/7046311066329939970~c5_168x168.jpeg?x-expires=1656831600&x-signature=9GsDTVTn9%2Bvb%2FFBkxZGaOlIkTM4%3D','create_time':'1656660622','video_id':'7109065174526479622','status':'PUBLIC','owner':False,'comment_id':'7115302925501563650','likes':0,'parent_comment_id':'7111907185164763905','username':'klein_kunkun','text':'hh','liked':False,'user_id':'6faa870ee45c1f68a2d98d50e09f222a04069380c1032f1919f3ffe25be1f085'}]}}
```

### Create a new comment on an owned video

```python
api.create_comment(business_id="Your business id", video_id="Your video id", text="Comment text", return_json=True)
# Response: {"code":0,"message":"Ok","request_id":"20210817034316010245031056097316BA","data":{"comment_id":"6990565363377392901","video_id":"6990565363377392901","create_time":1627617835,"text":"this is a comment"}}
```

### Reply to an existing comment on an owned video

```python
api.create_reply(
    business_id="Your business id", video_id="Your video id",
    comment_id="Comment id", text="Reply text", return_json=True
)
# Response: {"code":0,"message":"Ok","request_id":"20210817034316010245031056097316BA","data":{"comment_id":"6990565363377392901","video_id":"6990565363377392901","create_time":1627617835,"text":"this is a comment"}}
```

### Like/unlike an existing comment on an owned video

```python
# like a comment
api.like_comment(business_id="Your business id", comment_id="Comment id", action="LIKE", return_json=True)
# Response: {"code":0,"message":"Ok","request_id":"20210817034316010245031056097316BA","data":{}}

# unlike a comment
api.like_comment(business_id="Your business id", comment_id="Comment id", action="UNLIKE", return_json=True)
# Response: {"code":0,"message":"Ok","request_id":"20210817034316010245031056097316BA","data":{}}
```

### Pin/unpin an existing comment on an owned video

```python
# pin a comment
api.pin_comment(business_id="Your business id", comment_id="Comment id", action="PIN", return_json=True)
# Response: {"code":0,"message":"Ok","request_id":"20210817034316010245031056097316BA","data":{}}

# unpin a comment
api.pin_comment(business_id="Your business id", comment_id="Comment id", action="UNPIN", return_json=True)
# Response: {"code":0,"message":"Ok","request_id":"20210817034316010245031056097316BA","data":{}}
```

### Hide/unhide an existing comment on an owned video

```python
# hide a comment
api.hide_comment(business_id="Your business id", comment_id="Comment id", action="HIDE", return_json=True)
# Response: {"code":0,"message":"Ok","request_id":"20210817034316010245031056097316BA","data":{}}

# unhide a comment
api.hide_comment(business_id="Your business id", comment_id="Comment id", action="UNHIDE", return_json=True)
# Response: {"code":0,"message":"Ok","request_id":"20210817034316010245031056097316BA","data":{}}
```

### Delete an existing comment on an owned video

```python
api.delete_comment(business_id="Your business id", comment_id="Comment id", return_json=True)
# Response: {"code":0,"message":"Ok","request_id":"20210817034316010245031056097316BA","data":{}}
```
