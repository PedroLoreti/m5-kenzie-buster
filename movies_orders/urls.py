from django.urls import path
from movies_orders.views import MoviesOrdersView


urlpatterns = [
    path('movies/<int:movie_id>/orders/', MoviesOrdersView.as_view()),

]
