from functools import wraps

from pytiktok.error import PyTiktokError


def function_only_for_api_v13(func):
    @wraps(func)
    def decorated(self, *args, **kwargs):
        if self.api_version != "v1.3":
            raise PyTiktokError(f"This method only for api version 1.3")
        return func(self, *args, **kwargs)

    return decorated
