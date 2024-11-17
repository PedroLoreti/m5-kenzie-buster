from django.urls import path
from movies.views import MoviesView


urlpatterns = [
    path('movies/', MoviesView.as_view()),
    path('movies/<int:movie_id>/', MoviesView.as_view()),
]
