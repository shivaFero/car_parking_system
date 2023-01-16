from django.urls import path
from . import views
urlpatterns = [
  path("login/", views.UserLogIn.as_view()),
  path('register/', views.RegisterUserAPIView.as_view()),
]