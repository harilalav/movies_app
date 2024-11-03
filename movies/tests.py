import json
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from movies.models import Movie, MovieCollection
from movies.serializers import MovieCollectionMinimalSerializer

from .factories import MovieCollectionFactory, MovieFactory, UserFactory


class MovieListViewTests(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.client.force_login(self.user)

    @patch("movies.views.fetch_movies_with_retries")
    def test_movie_list_view_success(self, mock_fetch_movies):
        mock_fetch_movies.return_value = {
            "results": [{"title": "Movie 1"}, {"title": "Movie 2"}],
            "next": "http://testserver/movie_list?page=2",
            "previous": None,
        }

        response = self.client.get(reverse("movie_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["title"], "Movie 1")
        self.assertEqual(response.data["results"][1]["title"], "Movie 2")


class MovieCollectionViewSetTests(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.client.force_login(self.user)
        self.collection = MovieCollectionFactory.create(user=self.user)

    def test_list_collections(self):
        response = self.client.get(reverse("moviecollection-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("collections", response.data["data"])
        self.assertIsInstance(response.data["data"]["collections"], list)

    def test_create_collection(self):
        movie = MovieFactory.create()
        data = {
            "title": "My Collection",
            "description": "A collection of my favorite movies.",
            "movies": [
                {
                    "title": "Queerama",
                    "description": "50 years after.",
                    "genres": "queen",
                    "uuid": "57baf4f4-c9ef-4197-9e4f-acf04eae5b4d",
                },
            ],
        }
        response = self.client.post(
            reverse("moviecollection-list"), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("collection_uuid", response.data)

    def test_update_collection(self):
        movie = MovieFactory.create()
        self.collection.movies.add(movie)

        data = {
            "title": "Updated Collection",
            "description": "Updated description.",
        }
        response = self.client.put(
            reverse("moviecollection-detail", args=[self.collection.uuid]),
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Collection")

    def test_update_collection_partial(self):
        movie = MovieFactory.create()
        self.collection.movies.add(movie)

        data = {
            "description": "New description only.",
        }
        response = self.client.patch(
            reverse("moviecollection-detail", args=[self.collection.uuid]),
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "New description only.")

    def test_delete_collection(self):
        self.assertTrue(
            MovieCollection.objects.filter(uuid=self.collection.uuid).exists()
        )
        response = self.client.delete(
            reverse("moviecollection-detail", args=[self.collection.uuid])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            MovieCollection.objects.filter(uuid=self.collection.uuid).exists()
        )

    def test_delete_collection_not_found(self):
        # Attempt to delete a non-existing collection
        response = self.client.delete(
            reverse("moviecollection-detail", args=["non-existing-uuid"])
        )

        # Check the response status code for not found
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MovieCollectionViewSetUnauthorizedTests(APITestCase):
    def test_unauthorized_access(self):
        response = self.client.get(reverse("moviecollection-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
