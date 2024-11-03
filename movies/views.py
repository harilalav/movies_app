from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import fetch_movies_with_retries

from django.urls import reverse
from urllib.parse import urlparse, parse_qs


class MovieListView(APIView):
    def get(self, request):
        try:
            data = fetch_movies_with_retries(request)

            # Build the current URL path
            base_url = request.build_absolute_uri(reverse("movie_list"))

            # Update next and previous URLs
            if data.get("next"):
                next_page = self.extract_page_number(data["next"])
                data["next"] = f"{base_url}?page={next_page}" if next_page else None
            if data.get("previous"):
                previous_page = self.extract_page_number(data["previous"])
                data["previous"] = (
                    f"{base_url}?page={previous_page}" if previous_page else base_url
                )
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    def extract_page_number(self, url):
        """
        Extracts the page number.
        """
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get("page", [None])[0]
