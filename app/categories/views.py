from rest_framework.generics import ListAPIView

from movies.models import MoviesModel
from movies.serializers import MoviesListSerializer


class MoviesByGenreCategoryListAPIView(ListAPIView):
    serializer_class = MoviesListSerializer

    def get_queryset(self):
        genre_id = self.kwargs['genre_id']
        return MoviesModel.objects.filter(genres__id=genre_id, is_active=True,).distinct()


class MoviesByActorCategoryListAPIView(ListAPIView):
    serializer_class = MoviesListSerializer

    def get_queryset(self):
        actor_id = self.kwargs['actor_id']
        return MoviesModel.objects.filter(actors__id=actor_id, is_active=True,).distinct()



class MoviesByDirectorCategoryListAPIView(ListAPIView):
    
    serializer_class = MoviesListSerializer
    def get_queryset(self):
        director_id = self.kwargs['director_id']
        return MoviesModel.objects.filter(directors__id=director_id, is_active=True,).distinct()

