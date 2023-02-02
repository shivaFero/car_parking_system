from django.contrib import admin
from . import models

admin.site.register(models.SlotBooking)
admin.site.register(models.SlotConfig)
admin.site.register(models.PaymentConfig)
admin.site.register(models.BookingPayment)
