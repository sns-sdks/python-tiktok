python-tiktok

A simple Python wrapper around for Tiktok API :sparkles: :cake: :sparkles:.

.. image:: https://img.shields.io/badge/TikTok-%23000000.svg?style=for-the-badge&logo=TikTok&logoColor=white
   :target: https://developers.tiktok.com/
   :alt: tiktok

.. image:: https://img.shields.io/pypi/v/python-tiktok.svg
    :target: https://pypi.org/project/python-tiktok/
    :alt: PyPI

============
Introduction
============

This library provides a service to easily use TikTok official apis.

For now, include follows apis:

- `TikTok for developers <https://developers.tiktok.com/>`_
- `TikTok for Business Account <https://ads.tiktok.com/marketing_api/docs?id=1732701966223426>`_

==========
Installing
==========

You can install this library easily by `pypi`:

.. code-block:: shell

    $ pip install python-tiktok

More installing detail see `Installation docs <https://sns-sdks.lkhardy.cn/python-tiktok/installation/>`_

=====
Using
=====

You can see more usage detail at `usage docs <https://sns-sdks.lkhardy.cn/python-tiktok/usage/preparation/>`_

----------------
Business Account
----------------

Version Tips :

    API for Business Version ``1.3`` is now live! visit `here <https://ads.tiktok.com/marketing_api/docs?id=1740579480076290>`_ for more details.

    Now this library set default version to ``v1.3``.

    And ``v1.2`` will be deprecated on August 15, 2023.

If you have account access token, you can initialize api instance by it.

.. code-block:: python

    >>> from pytiktok import BusinessAccountApi
    >>> business_api = BusinessAccountApi(access_token="Your Access Token")

Or you can let account to give permission by `OAuth flow`. See `business authorization docs <https://sns-sdks.lkhardy.cn/python-tiktok/authorization/business-authorization/>`_

Now you can get account's data.

Get account profile:

.. code-block:: python

    >>> business_api.get_account_data(business_id="Business ID", return_json=True)
    >>> # {'code':0,'message':'OK','request_id':'2022070106561301000400402500400500600301500A52386','data':{'display_name':'kiki','profile_image':'https://p16-sign-va.tiktokcdn.com/tos-maliva-avt-0068/accb4aeac4ec812e2bdc45ce1da1ed39~c5_168x168.jpeg?x-expires=1656828000&x-signature=MmXPWeImP%2BRGBwAOqN3wjPpDiZE%3D'}}

If you set function parameter `return_json` to `True`, will return the json dict data. Otherwise will return a `dataclass` object representing the response.

Get account videos:

.. code-block:: python

    >>> business_api.get_account_videos(business_id="Business ID", return_json=True)
    >>> # {'code':0,'message':'OK','request_id':'20220701071724010004003007735002053068B3FD9','data':{'videos':[{'item_id':'7108684822863760646'},{'item_id':'7109064881462152453'}],'has_more':False,'cursor':0}}

-------
Kit Api
-------

If you have user access token, you can initialize api instance by it.

.. code-block:: python

    >>> from pytiktok import KitApi
    >>> kit_api = KitApi(access_token="Your Access Token")

Or you can let user to give permission by `OAuth flow`. See `kit authorization docs <https://sns-sdks.lkhardy.cn/python-tiktok/authorization/kit-authorization/>`_

Now you can get account's data.

Get user info:

.. code-block:: python

    >>> kit_api.get_user_info(open_id="User Openid", return_json=True)
    >>> # {'data':{'user':{'open_id':'open_id','union_id':'union_id','avatar_url':'https://p16-sign-sg.tiktokcdn.com/tiktok-obj/7046311066329939970~c5_168x168.jpeg?x-expires=1656907200&x-signature=w4%2FugSm2IOdma6p0D9V%2FZneIlPU%3D','display_name':'ki'}},'error':{'code':0,'message':''}}

Get user videos:

.. code-block:: python

    >>> kit_api.get_user_videos(open_id="_000Hqnyyz5UYe39YWBZwFnaQGfyaoh3s4IY", return_json=True)
    >>> # {'data':{'videos':[{'create_time':1654670085,'share_url':'https://www.tiktok.com/@klein_kunkun/video/7106753891953347842?utm_campaign=tt4d_open_api&utm_source=aw46lwwtsqjeapig','duration':5,'id':'7106753891953347842'},{'create_time':1654658105,'share_url':'https://www.tiktok.com/@klein_kunkun/video/7106702437926407426?utm_campaign=tt4d_open_api&utm_source=aw46lwwtsqjeapig','duration':6,'id':'7106702437926407426'}],'cursor':1654658105000,'has_more':False},'error':{'code':0,'message':''}}
