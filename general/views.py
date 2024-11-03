# views.py

from django.core.cache import cache
from django.http import JsonResponse
from movies_app.middlewares import RequestCountMiddleware
from rest_framework.decorators import api_view


@api_view(["GET"])
def get_request_count(request):
    # Fetch the current request count from Redis
    request_count = cache.get(RequestCountMiddleware.REQUEST_COUNT_KEY, 0)
    return JsonResponse({"requests": request_count})


@api_view(["POST"])
def reset_request_count(request):
    # Reset the request count in Redis
    cache.set(RequestCountMiddleware.REQUEST_COUNT_KEY, 0)
    return JsonResponse({"message": "request count reset successfully"})
