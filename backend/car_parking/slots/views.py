from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from common.helpers import get_date_based_on_user_type
from common.views import BaseViewSet
from . import models, serializers, filters, helpers
from common.constants import Action, HTTPMethod


class SlotBookViewSets(BaseViewSet):
    model = models.SlotBooking
    queryset = models.SlotBooking.objects.select_related('user').all()
    filterset_class = filters.SlotBookingFilter
    search_fields = ("vehicle_no", "user__username", "user__first_name", "user__last_name")

    view_serializers = {
        Action.LIST: serializers.SlotBookingListSerializers,
        Action.RETRIEVE: serializers.SlotBookingSerializers,
        Action.VIEW: serializers.SlotBookingDetailsSerializers,
    }

    def get_queryset(self):
        qs = self.model.objects.all()
        return get_date_based_on_user_type(self.request, qs=qs)

    @action(methods=[HTTPMethod.POST], detail=False)
    def collect_payment(self, request):
        serializer = serializers.SlotBookingPaymentSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(added_by=request.user.username)
            return Response("Payment Completed Successfully", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=[HTTPMethod.PATCH], detail=True)
    def cancel_booking(self, request, *args, **kwargs):
        instance = self.get_object()

        serializer = serializers.CancelSlotBookingSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            serializer.save(updated_by=request.user.username)
            return Response("Booking successfully cancelled", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetSlotAvailability(APIView):
    def get(self, request):
        try:
            booking_date = self.request.query_params.get('booking_date', None)
            availability_details = helpers.get_slot_availability(booking_date)
            return Response(availability_details)
        except Exception as err:
            return Response(f"While fetching slot availability got errors: {str(err)}")


class GetPaymentChargesInfoAPIView(APIView):
    def get(self, request):
        try:
            availability_details = helpers.get_payment_charges_info()
            return Response(availability_details)
        except Exception as err:
            return Response(f"While fetching payment info got errors: {str(err)}")
