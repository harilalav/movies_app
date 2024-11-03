from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from movies_app.middlewares import RequestCountMiddleware


class RequestCountView(APIView):
    """
    API view to get the total number of requests.
    """

    def get(self, request):
        # Fetch the current request count from Redis
        request_count = cache.get(RequestCountMiddleware.REQUEST_COUNT_KEY, 0)
        return Response({"requests": request_count})


class ResetRequestCountView(APIView):
    """
    API view to reset the request count.
    """

    def post(self, request):
        # Reset the request count in Redis
        cache.set(RequestCountMiddleware.REQUEST_COUNT_KEY, 0)
        return Response({"message": "request count reset successfully"})
