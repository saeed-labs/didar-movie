from django.urls import path
from .views import  MoviesListView, MoviesDetailView


urlpatterns = [
    path('', MoviesListView.as_view()),
    path('<int:pk>/<slug:slug>/', MoviesDetailView.as_view()),
]