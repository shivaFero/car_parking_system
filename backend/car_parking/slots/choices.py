from slots.constants import PaymentTypeConstant, BookingStatus, VehicleType, PaymentStatus

PAYMENT_TYPE_CHOICES = (
    (PaymentTypeConstant.CASH, 'Cash'),
    (PaymentTypeConstant.UPI, 'UPI'),
    (PaymentTypeConstant.CARD, 'Card'),
)

PAYMENT_STATUS_CHOICES = (
    (PaymentStatus.SUCCESS, 'Success'),
    (PaymentStatus.FAILED, 'Failed'),
    (PaymentStatus.PENDING, 'Pending'),
    (PaymentStatus.DECLINED, 'Declined')
)


BOOKING_STATUS_CHOICES = (
    (BookingStatus.IN, 'In'),
    (BookingStatus.OUT, 'Out'),
    (BookingStatus.CANCEL, 'Cancel'),
)

VEHICLE_TYPE_CHOICES = (
    (VehicleType.TWO_WHEELER, 'Two Wheeler'),
    (VehicleType.THREE_WHEELER, 'Three Wheeler'),
    (VehicleType.FOUR_WHEELER, 'Four Wheeler'),
)
