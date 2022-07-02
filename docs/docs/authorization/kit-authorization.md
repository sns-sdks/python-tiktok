# Authorization for developers

Before you use the developer kit API, you (the developer) need to have an app.

Please obtain a client key and secret from the developer portal on `https://developers.tiktok.com` under "My apps".

## Procedure

### Prerequisites

- Your app client ID
- Your app client secret
- Redirect URL

These can be found in `Manage apps` > `App Detail`.

### Initial Api

Initial Api instance to call api.

```python
from pytiktok import KitApi

api = KitApi(client_id="Your client ID", client_secret="Your client secret")
```

By default, The callback uri is https://localhost/, You need add this url to App's settings.


### Get Authorize url

Get authorize url for user to login

```python
api.get_authorize_url()
# Response" ('https://www.tiktok.com/auth/authorize/?client_key=xxx&scope=user.info.basic%2Cvideo.list&response_type=code&redirect_uri=https%3A%2F%2Flocalhost%2F&state=DzHqVZFdmiWhvIXU', 'DzHqVZFdmiWhvIXU')
```

Once the user authorizes the application for the requested permission scopes, they are redirected to the applications specified redirect URL, with an authorization code included as an added query parameter in the URL (along with the state query parameter if initially included).

Example: `https://localhost/?code=code&scopes=user.info.basic%2Cvideo.list&state=DzHqVZFdmiWhvIXU`

### Generate Access Token

# https://apiprod.onesight.com/tiktokcallback?code=0ZTN0kZ5ds2M4JXaY92zmAEAvuayatQBVDBhWkUAny0SA0ttMh1RQ2Wa5NlH0oMMMSN9-SpR8S1U7RstvYbRVf95LJUONKt4fODG_69XU64%2A0%215413&scopes=user.info.basic%2Cvideo.list&state=DzHqVZFdmiWhvIXU
```python
api.generate_access_token(code="Code in redirect url")
# Response: {"data":{"access_token":"access_token","captcha":"","desc_url":"","description":"","error_code":0,"expires_in":86400,"log_id":"20220701091238010004004007735002017070F8D12","open_id":"_000Hqnyyz5UYe39YWBZwFnaQGfyaoh3s4IY","refresh_expires_in":31536000,"refresh_token":"refresh_token","scope":"user.info.basic,video.list"},"message":"success"}
```

Now the current instance `api` has hold the access token, you can to get some data from TikTok.


### Refresh Access Token

```python
api.refresh_access_token(refresh_token="Your refresh token", return_json=True)
# Response: {"data":{"access_token":"access_token","captcha":"","desc_url":"","description":"","error_code":0,"expires_in":86400,"log_id":"20220701091238010004004007735002017070F8D12","open_id":"_000Hqnyyz5UYe39YWBZwFnaQGfyaoh3s4IY","refresh_expires_in":31536000,"refresh_token":"refresh_token","scope":"user.info.basic,video.list"},"message":"success"}
```

### Revoke Access Token

```python
api.revoke_access_token(open_id="", access_token="", return_json=True)
# Response: {'data':{'captcha':'','desc_url':'','description':'','error_code':0,'log_id':'202207011230000100040030050060030000071B538'},'message':'success'}
```
