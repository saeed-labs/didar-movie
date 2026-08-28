from rest_framework import serializers

from .models import MoviesModel, MovieVideoModel
from categories.serializers import ActorsSerializer, DirectorsSerializer, GenreSerializer


class MovieVideoSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    class Meta:
        model = MovieVideoModel
        fields = ['id', 'file', 'is_trailer', 'created_on', 'updated_on']

    def get_file(self, obj):
        if not obj.file:
            return None

        request = self.context.get('request')

        if request:
            return request.build_absolute_uri(obj.file.url)

        return obj.file.url


class MoviesListSerializer(serializers.ModelSerializer):
    # genres = GenreSerializer(many=True, read_only=True)
    # actors = ActorsSerializer(many=True, read_only=True)
    # directors = DirectorsSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()


    class Meta:
        model = MoviesModel
        fields = ['id', 'title','image', 'slug', 'short_description', 'Release_date',]

    def get_image(self, obj):
        if not obj.image:
            return None

        request = self.context.get('request')

        if request:
            return request.build_absolute_uri(obj.image.url)

        return obj.image.url


class MoviesDetailSerializer(serializers.ModelSerializer):
    movie_videos = MovieVideoSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorsSerializer(many=True, read_only=True)
    directors = DirectorsSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()


    class Meta:
        model = MoviesModel
        fields = ['id', 'title', 'slug', 'image', 'description', 'short_description', 'Release_date', 'is_featured',
                  'movie_videos', 'genres', 'actors', 'directors', ]


    def get_image(self, obj):
        if not obj.image:
            return None

        request = self.context.get('request')

        if request:
            return request.build_absolute_uri(obj.image.url)

        return obj.image.url