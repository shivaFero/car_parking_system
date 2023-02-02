from rest_framework import serializers
from slots.models import SlotBooking
from slots.constants import PaymentTypeConstant


class DashboardSerializers(serializers.ModelSerializer):
    booking_info = serializers.SerializerMethodField()
    payment_info = serializers.SerializerMethodField()

    class Meta:
        model = SlotBooking
        fields = ('booking_info', 'payment_info')

    def get_booking_info(self, instance):
        # All Data should be aggregated

        info = {
            'Per Day Booking': 0, # Total Booking divide by day/day
            'Per Day Empty Slots': 0,
            'Total Booking': 0,  # instance.count,
            'Total Users': 0,  # instance.user.count(), # only for admin
            'Total Unique Users': 0,  # instance.user.distinct().count(), # For Admin
            'Average Booking Hours Per day': 0,  # instance.total_booking_hrs/instance.count()
        }
        return info

    def get_payment_info(self, instance):
        # All Data should be aggregated
        # Get %age of each type payments
        info = {
            PaymentTypeConstant.PREPAID: 0,
            PaymentTypeConstant.UPI: 0,
            PaymentTypeConstant.CASH: 0,
            'Total Amount Per Day': 0
        }
        return info