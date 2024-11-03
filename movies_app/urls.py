from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from movies.views import MovieCollectionViewSet, MovieListView
from users.views import RegisterView

router = DefaultRouter()
router.register(r"", MovieCollectionViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("general/", include("general.urls")),
    path("register/", RegisterView.as_view(), name="join"),
    path("movies/", MovieListView.as_view(), name="movie_list"),
    path("collection/", include(router.urls)),
]
