from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import fetch_movies_with_retries


class MovieListView(APIView):
    def get(self, request):
        try:
            movies = fetch_movies_with_retries()
            return Response(movies, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
