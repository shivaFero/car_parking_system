from slots.filters import SlotBookingFilter
from slots.models import SlotBooking


class DashBoardFilter(SlotBookingFilter):

    class Meta:
        model = SlotBooking
        fields = ('from_time', 'to_time', 'from_date', 'to_date',)
