import django_filters
from . import models


class SlotBookingFilter(django_filters.FilterSet):
    from_time = django_filters.TimeFilter(field_name='from_time', lookup_expr='gte', label='From Time')
    to_time = django_filters.TimeFilter(field_name='to_time', lookup_expr='lte', label='To Time')
    from_date = django_filters.DateFilter(field_name='booking_date', lookup_expr='gte', label='From Date')
    to_date = django_filters.DateFilter(field_name='booking_date', lookup_expr='lte', label='To Date')
    vehicle_type = django_filters.CharFilter(field_name='vehicle_type', label='Vehicle Type')
    booking_status = django_filters.CharFilter(field_name='booking_status', label='Booking Status')

    ordering = django_filters.OrderingFilter(fields=['booking_date', 'exit_date_time', 'from_time', 'to_time'])

    class Meta:
        model = models.SlotBooking
        fields = ('ordering', 'from_time', 'to_time', 'from_date', 'to_date', 'booking_status')
