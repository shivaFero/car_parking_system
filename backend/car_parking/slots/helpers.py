from datetime import datetime, timedelta
from . import models, constants


def get_slot_availability(date: None, duration=2):
    if date is None:
        date = datetime.today().date()

    slot_duration = {}
    today_slot = models.SlotBooking.objects.filter(booking_date=date, booking_status=constants.BookingStatus.IN)
    for hour in range(0, 24, duration):
        from_time = hour
        to_time = hour + 2

        today_slot_time_window = today_slot.filter(from_time__hour__gte=from_time, to_time__hour__lte=to_time)

        slot_duration[f"{from_time} to {to_time}"] = today_slot_time_window.count()

    return slot_duration


def get_payment_charges_info():
    payment_config = models.PaymentConfig.objects.all()
    current = 0
    res = {}
    for payment in payment_config:
        res[f"{current} to {payment.hr_range} Hour"] = f"{payment.price} Rs"
        current = payment.hr_range

    return res




