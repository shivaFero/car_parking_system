from django.db import models

from users.models import User
from . import constants, choices


# Create your models here.

class SlotConfig(models.Model):
    total_space = models.PositiveIntegerField(default=8)
    booking_prior_hr = models.PositiveIntegerField(default=24, verbose_name='Booking Prior Time(in HR)')
    minimum_booking_hr = models.FloatField(default=1, verbose_name='Minimum Booking Hours')

    def __str__(self):
        return f"{self.total_space}-{self.booking_prior_hr}"


class PaymentConfig(models.Model):
    hr_range = models.PositiveIntegerField(default=0, verbose_name="Hours Up To")
    price = models.FloatField(default=0)
    remarks = models.TextField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.hr_range} - {self.price}"


class SlotBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_no = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=50, choices=choices.VEHICLE_TYPE_CHOICES,
                                    default=constants.VehicleType.FOUR_WHEELER)
    # Time Stamp
    booking_date = models.DateField(db_index=True, verbose_name='Booking Date')
    exit_date_time = models.DateTimeField(blank=True, null=True, verbose_name="Exit Date Time")
    from_time = models.TimeField()
    to_time = models.TimeField()
    total_booking_hrs = models.FloatField(default=0, verbose_name='Booking Duration')

    slot_assigned = models.PositiveIntegerField(default=0, verbose_name='Slot Assigned To Vehicle')

    booking_status = models.CharField(choices=choices.BOOKING_STATUS_CHOICES, max_length=10,
                                      default=constants.BookingStatus.IN,
                                      verbose_name='Booking Status')

    total_amount = models.FloatField(default=0, verbose_name='Total Amount/Due Amount')

    remarks = models.CharField(max_length=250, null=True, blank=True)

    # Action Performed By
    added_by = models.CharField(max_length=150, blank=True, null=True)
    updated_by = models.CharField(max_length=150, blank=True, null=True)

    # Action Performed On

    created_on = models.DateTimeField(auto_now_add=True, verbose_name='Booked On')
    updated_on = models.DateTimeField(null=True, blank=True, verbose_name='Updated On')

    def __str__(self):
        return f"{self.user.username}-{self.vehicle_no}"

    class Meta:
        ordering = ('-id', )

    @property
    def pass_id(self):
        return f'Pass-{self.id}-{self.booking_date}'


class BookingPayment(models.Model):
    slot = models.ForeignKey(SlotBooking, related_name='slot_payments', on_delete=models.RESTRICT)
    payment_type = models.CharField(choices=choices.PAYMENT_TYPE_CHOICES, max_length=50,
                                    default=constants.PaymentTypeConstant.UPI)
    due_amount = models.FloatField(default=0)
    amount_collected = models.FloatField(default=0)

    payment_status = models.CharField(max_length=50, choices=choices.PAYMENT_STATUS_CHOICES,
                                      default=constants.PaymentStatus.SUCCESS)

    transaction_ref_no = models.CharField(max_length=250, null=True, blank=True, verbose_name='Transaction Ref No')

    added_by = models.CharField(max_length=150, blank=True, null=True)
    updated_by = models.CharField(max_length=150, blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.slot}-{self.payment_type}"
