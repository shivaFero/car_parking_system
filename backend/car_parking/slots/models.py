from django.db import models
from users.models import User


# Create your models here.

class SlotBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle_no = models.CharField(max_length=50)
    from_time = models.TimeField()
    to_time = models.TimeField()
    total_booking_hrs = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}-{self.vehicle_no}"
