from django.contrib import admin

from movies.models import Movie, MovieCollection

admin.site.register(Movie)
admin.site.register(MovieCollection)
