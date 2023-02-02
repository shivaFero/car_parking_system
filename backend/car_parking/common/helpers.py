from datetime import datetime, timedelta

from slots.models import SlotBooking
from . import constants


def combine_date_time(date=None, time=None):
    if not date:
        date = datetime.today().date()
    if not time:
        time = datetime.today().time()
    return datetime.combine(date, time)


def get_duration_from_time(from_time, to_time):
    """This function return differance of given time in form of hour, minute and second"""
    assert from_time, "From time is require"
    assert to_time, "To time is require"

    from_time = combine_date_time(time=from_time)
    to_time = combine_date_time(time=to_time)
    difference = to_time - from_time

    second = difference.seconds
    hour = second/3600
    minute = hour*60

    res = {
        'second': second,
        'minute': minute,
        'hour': hour
    }
    return res


def get_date_based_on_user_type(request, qs, lookup="user", **kwargs):
    request_method = request.method
    if request_method.lower() == constants.HTTPMethod.GET:
        user = request.user
        if user and user.is_superuser:
            return qs
        else:
            kwargs[lookup] = user
            return qs.filter(**kwargs)
    return qs


def round_decimal_places(value, round_up=2):
    if not value:
        return 0
    if not isinstance(round_up, int):
        return f'round_up expecting integer but got {type(round_up)}'
    return round(value, round_up)


def convert_minute_to_hr_minute(minute):
    return '{:02d} Hour {:02d} Minutes'.format(*divmod(minute, 60)) if minute else None


def convert_hour_to_hr_minute(hour):
    return '{:.0f} Hour {:.0f} Minutes'.format(*divmod(hour*60, 60)) if hour else None


def convert_string_date_into_date_format(string_date):
    if string_date:
        return datetime.strptime(string_date, "%Y-%m-%d")
    return None


def get_available_time_slots_from_slot_booking():
    # today = datetime.today()
    # today_bookings = SlotBooking.objects.filter(booking_date=today)
    # today_from_time_list = list(set(today_bookings.values_list('from_time__hour', flat=True)))
    # today_to_time_slot_list = list(set(today_bookings.values_list('to_time__hour', flat=True)))
    # today_time_slot_list = res = [*today_from_time_list, *today_to_time_slot_list]
    #
    # # get_from_time_avl = which is graeter less than
    # # get_to_time_avl = which is lets than
    #
    # all_time_slot = [hr for hr in range(1, 25)]
    # available_slot = check_free_time(all_time_slot, today_time_slot_list)
    available_slot = []

    return available_slot
