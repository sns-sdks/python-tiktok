# Login Kit with QR Code

This doc will provide instruction on how to integrate QR code authorization capability with TikTok in your web application. This will enable your app to access TikTok user data within approved scopes using obtained access token.

More detail in [docs](https://developers.tiktok.com/doc/login-kit-qr-code-authorization/).

## Get QR Code Endpoint

```python
api.get_qrcode(return_json=True)
# Response: {'data':{'error_code':0,'qrcode':'iVBxxxx,   'scan_qrcode_url': 'aweme://authorize?authType=1&client_key=xxxx&client_ticket=tobefilled&next_url=https%3A%2F%2F127.0.0.1%3A9338%2Foauth%2Fscan_qrcode%2F%3Fclient_ticket%3Dtobefilled&qr_source_aid=0&scope=user.info.basic%2Cvideo.list&token=token,'token':'token},  'extra': {'error_detail': '',   'logid': '202207020612540100040030077350020071BBBF03A'},  'message': 'success'}
```

## Check QR code Endpoint

```python
api.check_qrcode(token="token", return_json=True)
# Response: {'data':{'error_code':0,'status':'expired'},'extra':{'error_detail':'','logid':'202207020615200100040040250040050060030120105295B'},'message':'success'}
```
