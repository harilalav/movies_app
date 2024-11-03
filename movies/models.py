import uuid

from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    genres = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.title


class MovieCollection(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    movies = models.ManyToManyField(Movie, related_name="movie_collections")

    def __str__(self) -> str:
        return self.title
