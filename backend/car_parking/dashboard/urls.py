from django.urls import path
from . import views
urlpatterns = [
  path("statics/", views.DashBoardAPIView().as_view()),
]
