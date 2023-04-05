from django.http import JsonResponse


class Process500Middleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception):
        return JsonResponse(
            status=exception.status_code,
            data={'detail': exception.detail}
        )
