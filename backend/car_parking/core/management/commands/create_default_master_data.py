from django.core.management.base import BaseCommand, CommandError
from core import default_master_data
from slots.models import SlotConfig, PaymentConfig
from users.models import User
from django.contrib.auth.management.commands import createsuperuser


class Command(BaseCommand):
    help = 'Create Default Master Data'

    def handle(self, *args, **kwargs):
        SlotConfig.objects.update_or_create(total_space=8, defaults={'booking_prior_hr': 24, 'minimum_booking_hr': 1})

        for payment in default_master_data.PAYMENT_CONFIG_DEFAULT_DATA:
            PaymentConfig.objects.update_or_create(hr_range=payment.get('hr_range'), defaults=payment)

        for user in default_master_data.DEFAULT_ADMIN_USER_DATA:
            try:
                username = user.get('username', None)
                if not username:
                    raise CommandError('username can not be none')

                User.objects.get(username=username)
            except User.DoesNotExist:
                User.objects.create_superuser(**user)

