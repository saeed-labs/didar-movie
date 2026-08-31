from rest_framework.views import APIView
from rest_framework.response import Response

from movies.models import MoviesModel
from movies.serializers import MoviesListSerializer


class HomeListView(APIView):

    def get(self, request):
        created_movies = (MoviesModel.objects.filter(is_active=True).order_by('-created_on')[:5])
        beloved_movies = (MoviesModel.objects.filter(is_active=True).order_by('-beloved')[:5])
        most_viewed_movies = (MoviesModel.objects.filter(is_active=True).order_by('-most_viewed')[:5])

        return Response({
            'created_movies': MoviesListSerializer(created_movies, many=True, context={'request': request}).data,
            'beloved_movies': MoviesListSerializer(beloved_movies, many=True, context={'request': request}).data,
            'most_viewed_movies': MoviesListSerializer(most_viewed_movies, many=True, context={'request': request}).data
        })
