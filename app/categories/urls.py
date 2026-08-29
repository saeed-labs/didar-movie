from django.urls import path, include

from .views import MoviesByGenreCategoryListAPIView, MoviesByActorCategoryListAPIView, MoviesByDirectorCategoryListAPIView


urlpatterns = [
    path('genres/<int:genre_id>/movies/', MoviesByGenreCategoryListAPIView.as_view()),
    path('actors/<int:actor_id>/movies/', MoviesByActorCategoryListAPIView.as_view()),
    path('directors/<int:director_id>/movies/', MoviesByDirectorCategoryListAPIView.as_view())
]