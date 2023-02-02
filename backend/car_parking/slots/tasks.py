from datetime import datetime

from car_parking.celery import app
from .constants import BookingStatus
from .models import SlotBooking


@app.task()
def update_slot_booking_status():
    today = datetime.today()
    slot = SlotBooking.objects.filter(booking_date__lte=today.date(), to_time__lte=today.time())
    if slot.exists():
        slot.update(booking_status=BookingStatus.OUT)

    return {"total_clear_slot": slot.count()}
