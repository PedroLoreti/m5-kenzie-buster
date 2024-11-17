from django.urls import path
from users.views import UsersView
from rest_framework_simplejwt import views

urlpatterns = [
    path('users/', UsersView.as_view()),
    path('users/login/', views.TokenObtainPairView.as_view()),
    path('token/refresh/', views.TokenRefreshView.as_view()),
]
