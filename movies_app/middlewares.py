from django.core.cache import cache


class RequestCountMiddleware:
    REQUEST_COUNT_KEY = "request_count"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Update the request count in redis
        cache.incr(self.REQUEST_COUNT_KEY, delta=1)
        response = self.get_response(request)
        return response
