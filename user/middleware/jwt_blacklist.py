import json

from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response

from user.utils.connection import get_redis_client
from user.exections import BlacklistedTokenException


class BlacklistTokenMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        raw_token = request.headers.get("Authorization", None)
        if raw_token:
            try:
                token = (raw_token.split()[1])
                self.check_blacklisted_token(token)
            except BlacklistedTokenException as error:
                return HttpResponse(
                    status=error.status_code,
                    content=json.dumps(
                        {
                            'code': error.code,
                            'content': error.detail
                        }
                    )
                )

        response = self._get_response(request)
        return response

    def check_blacklisted_token(self, token):
        redis_client = get_redis_client()
        if redis_client.sismember('blacklisted_jwt_tokens', token):
            raise BlacklistedTokenException()
