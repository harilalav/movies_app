from rest_framework import serializers

from .models import Movie, MovieCollection


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["uuid", "title", "description", "genres"]


class MovieCollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = MovieCollection
        fields = ["uuid", "title", "description", "movies"]

    def __init__(self, *args, **kwargs):
        super(MovieCollectionSerializer, self).__init__(*args, **kwargs)
        """
        Check if the serializer is for updating and
        Set 'required' to False for the fields that 
        are not mandatory in updates
        """
        if self.context.get("is_update", False):
            self.fields["title"].required = False
            self.fields["description"].required = False
            self.fields["movies"].required = False

    def create(self, validated_data):
        movies_data = validated_data.pop("movies")
        collection = MovieCollection.objects.create(**validated_data)
        for movie_data in movies_data:
            movie, _ = Movie.objects.get_or_create(**movie_data)
            collection.movies.add(movie)
        return collection

    def update(self, instance, validated_data):
        movies_data = validated_data.pop("movies")
        instance = super().update(instance, validated_data)
        for movie_data in movies_data:
            movie, _ = Movie.objects.get_or_create(**movie_data)
            instance.movies.add(movie)
        return instance


class MovieCollectionMinimalSerializer(serializers.Serializer):
    collection_uuid = serializers.UUIDField(source="uuid")


class MovieCollectionListSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    uuid = serializers.UUIDField()
