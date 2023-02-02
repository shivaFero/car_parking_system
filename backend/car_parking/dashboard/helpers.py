import datetime
from common.helpers import get_date_based_on_user_type, round_decimal_places
from slots.constants import PaymentTypeConstant
from slots.models import SlotBooking, BookingPayment
from django.db.models import Count, Sum, FloatField
from django.db.models.functions import Coalesce


def get_dashboard_based_on_given_from_to_date(request, from_date=None, to_date=None):
    if not to_date:
        to_date = datetime.date.today()
    if not from_date:
        from_date = to_date - datetime.timedelta(days=7)

    total_days = (to_date - from_date).days

    qs = SlotBooking.objects.filter(created_on__date__range=[from_date, to_date])

    slot_booking_by_login_user = get_date_based_on_user_type(request, qs)

    all_slot_payments = BookingPayment.objects.filter(slot__in=slot_booking_by_login_user)

    statics = slot_booking_by_login_user.aggregate(
        total_booking=Count('id'),
        total_users=Count('user'),
        total_booking_hours=Coalesce(Sum('total_booking_hrs'), 0, output_field=FloatField()),
        total_amount=Coalesce(Sum('total_amount'), 0, output_field=FloatField())
    )
    unique_user = len(set(slot_booking_by_login_user.values_list('user', flat=True)))

    total_payment = all_slot_payments.count()
    payment_count = {
        PaymentTypeConstant.CASH: all_slot_payments.filter(payment_type=PaymentTypeConstant.CASH).count(),
        PaymentTypeConstant.CARD: all_slot_payments.filter(payment_type=PaymentTypeConstant.CARD).count(),
        PaymentTypeConstant.UPI: all_slot_payments.filter(payment_type=PaymentTypeConstant.UPI).count(),
        'Total': total_payment
    }
    payment_info = dict()
    if total_payment:
        payment_in_percentage = {
            PaymentTypeConstant.CASH: round_decimal_places(
                (payment_count[PaymentTypeConstant.CASH]*100)/total_payment),
            PaymentTypeConstant.CARD: round_decimal_places(
                (payment_count[PaymentTypeConstant.CARD]*100)/total_payment),
            PaymentTypeConstant.UPI: round_decimal_places(
                (payment_count[PaymentTypeConstant.UPI]*100)/total_payment),
            'Total': 100,
        }
        payment_info['payment_in_percentage'] = payment_in_percentage
        payment_info['payment_count'] = payment_count

    res = {
        'total_booking_hours_per_day': round_decimal_places(statics['total_booking_hours'] / total_days),
        'per_day_booking': round_decimal_places(statics['total_booking'] / total_days),
        'unique_user': unique_user
    }
    statics['total_booking_hours'] = round_decimal_places(statics['total_booking_hours'])
    statics['payment_overview'] = payment_info
    res.update(**statics)

    return res



