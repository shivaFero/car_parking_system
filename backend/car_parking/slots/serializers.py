from datetime import datetime, timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers

from common.constants import DateTimeFormat
from common.helpers import combine_date_time, get_duration_from_time, round_decimal_places, convert_hour_to_hr_minute
from users.models import User
from . import models, choices, constants


class SlotBookingSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    vehicle_type = serializers.ChoiceField(
        choices=choices.VEHICLE_TYPE_CHOICES,
        error_messages={'invalid_choice': f'Valid choices are: '
                                          f'{", ".join([counter[0] for counter in choices.VEHICLE_TYPE_CHOICES])}'})

    class Meta:
        model = models.SlotBooking
        fields = ("id", "user", "vehicle_no", "booking_date", "exit_date_time", "from_time", "to_time",
                  "total_booking_hrs", "booking_status", "exit_date_time", "slot_assigned", "vehicle_type",
                  "total_amount")
        extra_kwargs = {'vehicle_type': {'required': True}, }

    def validate_booking_date(self, value):
        current_date = timezone.now()
        if value < current_date.date():
            raise serializers.ValidationError('Booking date cannot be in the past.')
        return value

    @staticmethod
    def get_closet_value_from_list(value_list: list, target_value: [int, str]):
        return min([n for n in value_list if n >= target_value])  # get just largest number
        # return min(value_list, key=lambda x: abs(x-target_value))  # Get just lowest number

    def get_payment_amount_by_hour(self, from_time, to_time):
        try:
            hour = get_duration_from_time(from_time, to_time).get('hour')
            payment_list = models.PaymentConfig.objects.all()
            list_of_hrs = list(payment_list.values_list('hr_range', flat=True))
            get_hr = self.get_closet_value_from_list(list_of_hrs, hour)

            total_amount = payment_list.filter(hr_range=get_hr).last()
            return total_amount.price

        except Exception as err:
            raise serializers.ValidationError("Payment Config is not setup. Please contact to manager")

    def validate(self, attrs):
        attrs['user'] = self.context.get('request').user
        booking_date = attrs['booking_date']
        booking_slots = models.SlotBooking.objects.filter(booking_date=booking_date,
                                                          booking_status=constants.BookingStatus.IN)

        slot_config = models.SlotConfig.objects.first()

        from_time = attrs['from_time']
        to_time = attrs['to_time']

        if from_time > to_time:
            raise serializers.ValidationError("From Time can not be greater than To Time ")

        slot_time = booking_slots.filter(
            Q(from_time__lte=from_time, to_time__gt=from_time) |
            Q(from_time__lte=to_time, to_time__gt=to_time)
        )

        list_of_vehicle_no = slot_time.values_list('vehicle_no', flat=True)

        if attrs['vehicle_no'] in list_of_vehicle_no:
            raise serializers.ValidationError({
                'vehicle_no': f"This Vehicle is already booked between in this time "
                              f"{slot_time.first().from_time}: {slot_time.first().to_time} on {booking_date}"
            })

        booking_hr = combine_date_time(booking_date, from_time)
        current_time = datetime.now()
        booking_prior_hr = slot_config.booking_prior_hr
        if current_time - timedelta(hours=booking_prior_hr) <= booking_hr <= current_time + timedelta(
                hours=booking_prior_hr):
            raise serializers.ValidationError(f"Booking should be prior in {booking_prior_hr} hour")

        total_hrs = get_duration_from_time(from_time, to_time).get('hour')
        if total_hrs < slot_config.minimum_booking_hr:
            raise serializers.ValidationError(f"Booking should be at least for {slot_config.minimum_booking_hr} hr ")

        slot_count = slot_time.count() + 1  # Increment with 1 if initially have no any slot booked
        if slot_count > slot_config.total_space:
            raise serializers.ValidationError(f"No any space available on {booking_date} "
                                              f"between {from_time} to {to_time}")
        attrs['total_booking_hrs'] = round_decimal_places(total_hrs)
        attrs['exit_date_time'] = combine_date_time(booking_date, to_time)
        attrs['slot_assigned'] = slot_count

        attrs['total_amount'] = self.get_payment_amount_by_hour(from_time, to_time)
        return attrs


class SlotBookingUpdateSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.SlotBooking
        fields = ("booking_date", "from_time", "to_time")

    def validate_booking_date(self, value):
        current_date = timezone.now()
        if value < current_date.date():
            raise serializers.ValidationError('Booking date cannot be in the past.')
        return value

    def validate(self, attrs):
        from_time = attrs['from_time']
        to_time = attrs['to_time']

        if from_time > to_time:
            serializers.ValidationError("From time can not be greater than To time")


class SlotBookingListSerializers(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', default=None)
    last_name = serializers.CharField(source='user.last_name', default=None)
    username = serializers.CharField(source='user.username', default=None)
    exit_date_time = serializers.DateTimeField(format=DateTimeFormat.DATE_TIME)
    total_booking_hrs = serializers.SerializerMethodField()

    class Meta:
        model = models.SlotBooking
        fields = ("id", "vehicle_no", "username", "first_name", "last_name", "username", "booking_date", "from_time",
                  "to_time", "total_booking_hrs", "exit_date_time", "booking_status", "slot_assigned",
                   "pass_id",
                  )

    def get_total_booking_hrs(self, instance):
        return convert_hour_to_hr_minute(instance.total_booking_hrs)


class SlotBookingPaymentSerializers(serializers.ModelSerializer):
    slot = serializers.PrimaryKeyRelatedField(queryset=models.SlotBooking.objects.all(),
                                              error_messages={"does_not_exist": "Id doest not exits"})
    payment_type = serializers.ChoiceField(
        required=True, allow_null=False, allow_blank=False, choices=choices.PAYMENT_TYPE_CHOICES,
        error_messages={'invalid_choice': f'Valid choices are: '
                                          f'{", ".join([counter[0] for counter in choices.PAYMENT_TYPE_CHOICES])}'})

    class Meta:
        model = models.BookingPayment
        fields = ("slot", "payment_type", "due_amount", "amount_collected", "transaction_ref_no")
        extra_kwargs = {
            'amount_collected': {'required': True, 'min_value': 1},
            'payment_status': {'required': True},
            'transaction_ref_no': {'required': True, 'allow_null': False, "allow_blank": False}
            }

    def validate(self, attrs):
        if attrs['amount_collected'] < attrs['due_amount']:
            raise serializers.ValidationError("Amount can not be less than total amount")

        return attrs


class CancelSlotBookingSerializer(serializers.ModelSerializer):
    booking_status = serializers.ChoiceField(
        default=constants.BookingStatus.CANCEL,
        required=False,
        choices=choices.BOOKING_STATUS_CHOICES,
        error_messages={'invalid_choice': f'Valid choices are: '
                                          f'{", ".join([counter[0] for counter in choices.BOOKING_STATUS_CHOICES])}'}
    )

    class Meta:
        model = models.SlotBooking
        fields = ("booking_status", "remarks")
        extra_kwargs = {
            'remarks': {'required': True, 'allow_null': False, 'allow_blank': False}
        }

    # def validate_booking_status(self, value):
    #     if value and value == constants.BookingStatus.CANCEL:
    #         return value
    #     raise serializers.ValidationError("You Can only cancel the order, other status can not be updated")


class SlotBookingDetailsSerializers(SlotBookingListSerializers):
    payment_details = serializers.SerializerMethodField()
    total_booking_hrs = serializers.SerializerMethodField()
    booked_on = serializers.DateTimeField(source='created_on', format=DateTimeFormat.DATE_TIME)

    class Meta:
        model = models.SlotBooking

        fields = ("pass_id", "vehicle_no", "slot_assigned", "total_booking_hrs", "username", "first_name",
                  "last_name", "username", "booking_date", "from_time", "to_time",  "exit_date_time", "booked_on",
                  "booking_status", "remarks", "payment_details")

    def get_payment_details(self, instance):
        payment_info = [
            {
                "Payment Type": payment.payment_type,
                "Total Amount": payment.amount_collected,
                'Transaction Ref No': payment.transaction_ref_no,
                'Payment Status': payment.payment_status
            } for payment in instance.slot_payments.all()
        ]
        return payment_info

    def get_total_booking_hrs(self, instance):
        return convert_hour_to_hr_minute(instance.total_booking_hrs)




