from django.http import JsonResponse

from user.exections import BlacklistedTokenException
from user.services import check_blacklisted_token, get_token_from_header


class BlacklistTokenMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        try:
            token = get_token_from_header(request)
            check_blacklisted_token(token)
        except BlacklistedTokenException as error:
            return JsonResponse(
                status=error.status_code,
                data={'detail': error.detail}
            )

        response = self._get_response(request)
        return response
