from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from general.views import RequestCountView, ResetRequestCountView
from movies.views import MovieCollectionViewSet, MovieListView
from users.views import RegisterView

router = DefaultRouter()
router.register(r"", MovieCollectionViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("register/", RegisterView.as_view(), name="join"),
    path("movies/", MovieListView.as_view(), name="movie_list"),
    path("movies/", MovieListView.as_view(), name="movie_list"),
    path("request-count/", RequestCountView.as_view(), name="request_count"),
    path(
        "request-count/reset/",
        ResetRequestCountView.as_view(),
        name="reset_request_count",
    ),
]
