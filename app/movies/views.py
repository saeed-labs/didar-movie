from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import MovieOwnership
from rest_framework.permissions import IsAuthenticated

from permissions.movie_owner import CanAccessMovie
from .models import MoviesModel
from .serializers import MoviesListSerializer, MoviesDetailSerializer
from utils.customPagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MoviesFilter
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter



class MoviesListView(APIView):
    serializer_class = MoviesListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MoviesFilter
    pagination_class = CustomPagination


    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                description="Filter products by title",
                required=False,
                type=str,
            ),
        ],
        responses=MoviesListSerializer(many=True),
    )


    def get(self, request, format=None):
        queryset = MoviesModel.objects.filter(is_active=True)
        filterset = self.filterset_class(data=request.query_params, queryset=queryset)
        if filterset.is_valid():
            queryset = filterset.qs
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = MoviesListSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)
        return Response(filterset.errors, status=status.HTTP_400_BAD_REQUEST)


class MoviesDetailView(APIView):
    serializer_class = MoviesDetailSerializer
    permission_classes = [IsAuthenticated, CanAccessMovie]

    def get(self, request, slug, pk,):
        movie = get_object_or_404(
            MoviesModel.objects.filter(is_active=True).prefetch_related('movie_videos', 'genres__parent', 'actors',
                                                                        'directors', ), slug=slug, id=pk )

        self.check_object_permissions(request, movie)
        movie.most_viewed += 1
        movie.save(update_fields=['most_viewed'])

        serializer = self.serializer_class(movie, context={'request': request})
        return Response(serializer.data)
