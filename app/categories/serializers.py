from rest_framework import serializers

from .models import GenreModel, DirectorModel, ActorsModel


class GenreParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreModel
        fields = ['id', 'name', 'slug']


class GenreSerializer(serializers.ModelSerializer):
    parent = GenreParentSerializer(read_only=True)

    class Meta:
        model = GenreModel
        fields = ['id', 'name', 'slug', 'parent']



class ActorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActorsModel
        fields = ['id', 'name', 'slug', 'image']



class DirectorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorModel
        fields = ['id', 'name', 'slug', 'image']