# Authorization for Business

Before you use the Business Account API, you(the developer) need to first get authorization from the business to manage their accounts.

See more detail at [docs](https://ads.tiktok.com/marketing_api/docs?id=1733079856582657)


## Procedure

### Prerequisites

- Your app ID
- Your app secret
- Authorization URL

These can be found in `My Apps` > `App Detail` > `Basic Information`.

### Do Authorize

When the target business account user to visit the `Authorization URL`, user will reviews and approves the authorization request.

Once the user authorizes the application for the requested permission scopes, they are redirected to the applications specified redirect URL, with an authorization code included as an added query parameter in the URL (along with the state query parameter if initially included).

Example: `https://example.com/callback?code=xxxxxx-aw%2A3%214964&scopes=user.info.basic%2Cvideo.list`

### Generate Access Token

If you got the redirect url, you can use the code to get access token.

```python
from pytiktok import BusinessAccountApi

api = BusinessAccountApi(app_id="Your app ID", app_secret="Your app secret")

api.generate_access_token(code="Code in redirect url", return_json=True)
# Response: {'access_token':'xxxxx','creator_id':'xxxxxxx','expires':86400,'refresh_expires':31536000,'refresh_token':'xxxxx','scope':'user.info.basic,video.list,video.insights,comment.list,comment.list.manage,video.publish,user.insights','token_type':'bearer'}
```

Now the current instance `api` has hold the access token, you can to get some data from TikTok.

```python
api.get_account_data(business_id="creator_id in response", return_json=True)
# Response: {'code':0,'message':'OK','request_id':'20220701063301010002006005005006003019117A7E27','data':{'profile_image':'https://p16-sign-va.tiktokcdn.com/tos-maliva-avt-0068/accb4aeac4ec812e2bdc45ce1da1ed39~c5_168x168.jpeg?x-expires=1656828000&x-signature=MmXPWeImP%2BRGBwAOqN3wjPpDiZE%3D','display_name':'kiki'}}
```

### Refresh Access Token

The access token is valid for one day. Once an access token has expired, you need to make a request to this endpoint to renew the access token. Remember to pass in the refresh_token for a token renewal request.

```python
api.refresh_access_token(refresh_token="refresh_token in response", return_json=True)
# Response: {'access_token':'xxxxx','creator_id':'xxxxxxx','expires':86400,'refresh_expires':31536000,'refresh_token':'xxxxx','scope':'user.info.basic,video.list,video.insights,comment.list,comment.list.manage,video.publish,user.insights','token_type':'bearer'}
```
