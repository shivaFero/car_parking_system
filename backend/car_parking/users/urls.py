from django.urls import path
from . import views

urlpatterns = [
  path("login/", views.UserLogIn.as_view()),
  path('register/', views.RegisterUserAPIView.as_view()),
  path('logout/', views.LogoutAPIView.as_view()),
  path("retrieve_or_update/<int:pk>/", views.UserRetrieveUpdateAPIView.as_view()),
]