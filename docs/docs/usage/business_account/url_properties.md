## Manage URL properties

Verifying ownership of video URLs is an essential step to comply with TikTok's policies around copyrighted content and user safety.

More to see [Manage URL properties](https://business-api.tiktok.com/portal/docs?id=1769324038780930)

### Add URL property

Add a URL property (domain or URL prefix) that you want to verify ownership of, to an advertiser account.

More to see [Add URL property](https://business-api.tiktok.com/portal/docs?id=1769325280876545)

```python
api.add_url_property(
    app_id="app id",
    property_type=1,
    url="example.com"
)
# BusinessUrlPropertyInfoResponse(code=0, message='OK', request_id='202408070935578A03C337841C0A6EB22B', data=BusinessUrlPropertyInfoData(url_property_info=BusinessUrlPropertyInfo(property_type=1, url='example.com')))
```

### Check URL property verification

Check the result of the ownership verification for a URL property (domain or URL prefix).

More to see [Check URL property verification](https://business-api.tiktok.com/portal/docs?id=1769325308162050)

```python
api.check_url_property_verification(
    app_id="app id",
    property_type=1,
    url="example.com"
)
# BusinessUrlPropertyInfoResponse(code=0, message='OK', request_id='202408070935578A03C337841C0A6EB22B', data=BusinessUrlPropertyInfoData(url_property_info=BusinessUrlPropertyInfo(property_type=1, url='example.com')))
```

### Delete URL property

Delete an advertiser account's verified ownership of a URL property (domain or URL prefix).

More to see [Delete URL property](https://business-api.tiktok.com/portal/docs?id=1769325351919617)

```python
api.delete_url_property(
    app_id="app id",
    property_type=1,
    url="example.com"
)
# BusinessBaseResponse(code=0, message='OK', request_id='202408070935578A03C337841C0A6EB22B')
```

### Get added URL properties

Get the list of URL properties that have been added to an advertiser account.

More to see [Get added URL properties](https://business-api.tiktok.com/portal/docs?id=1769325368603650)

```python
api.get_added_url_properties(
    app_id="app id"
)
# BusinessUrlPropertyInfoListResponse(code=0, message='OK', request_id='2024080709351926240BB44FDD60705E4E', data=BusinessUrlPropertyInfoListData(url_property_info_list=[BusinessUrlPropertyInfo(property_type=1, url='example.com'), BusinessUrlPropertyInfo(property_type=1, url='sub.example.com')]))
``` 
