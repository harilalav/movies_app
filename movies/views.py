from urllib.parse import parse_qs, urlparse

from django.db.models import Count, Value
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from movies.models import Movie, MovieCollection
from movies.serializers import (
    MovieCollectionListSerializer,
    MovieCollectionMinimalSerializer,
    MovieCollectionSerializer,
)

from .utils import fetch_movies_with_retries


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


class MovieCollectionViewSet(viewsets.ModelViewSet):
    queryset = MovieCollection.objects.all()
    serializer_class = MovieCollectionSerializer

    def get_queryset(self):
        return MovieCollection.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return MovieCollectionListSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        result = self.get_serializer(qs, many=True).data
        collection_ids = qs.values_list("uuid", flat=True)
        favorite_genres = (
            Movie.objects.filter(movie_collections__uuid__in=collection_ids)
            .values("genres")
            .annotate(genre_count=Count("genres"))
            .order_by("-genre_count")
            .exclude(genres__in=["", None])
        ).values_list("genres")[:3]
        response_data = {
            "is_success": True,
            "data": {
                "collections": result,
                "favourite_genres": list(favorite_genres),
            },
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(user=self.request.user)
        return Response(
            MovieCollectionMinimalSerializer(instance).data,
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        collection = self.get_object()
        serializer = self.get_serializer(collection, data=request.data, partial=True)
        serializer.context["is_update"] = True
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
