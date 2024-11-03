import factory

from users.factories import UserFactory

from .models import Movie, MovieCollection


class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Movie

    title = factory.Faker("sentence", nb_words=3)
    description = factory.Faker("paragraph")
    genres = factory.Faker("word")


class MovieCollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MovieCollection

    user = factory.SubFactory(UserFactory)
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("paragraph")
