from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register("slot_booking", views.SlotBookViewSets, basename='slot-booking')

urlpatterns = [
    path("", include(router.urls)),
    path("slot_availability/", views.GetSlotAvailability().as_view()),
    path("payment_info/", views.GetPaymentChargesInfoAPIView().as_view()),
]
