from rest_framework import status
from rest_framework.exceptions import APIException
from django.core import exceptions


class BlacklistedTokenException(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Token is blacklisted.'
    default_code = 'token_not_valid'

    def __init__(self, detail=None, code=None):
        if detail is not None:
            self.detail = detail
        else:
            self.detail = self.default_detail

        if code is not None:
            self.code = code
        else:
            self.code = self.default_code
