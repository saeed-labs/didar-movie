from django.urls import path
from .views import  MoviesListView, MoviesDetailView


urlpatterns = [
    path('movies/', MoviesListView.as_view()),
    path('movies/<int:pk>/<slug:slug>/', MoviesDetailView.as_view()),
]