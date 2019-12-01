import logging

from django.utils.translation import pgettext_lazy

logger = logging.getLogger(__name__)


class AddressType:
    BILLING = 'billing'
    SHIPPING = 'shipping'

    CHOICES = [
        (BILLING, pgettext_lazy(
            'Type of address used to fulfill order',
            'Billing'
        )),
        (SHIPPING, pgettext_lazy(
            'Type of address used to fulfill order',
            'Shipping'
        ))]


class ShippingType:
    DELIVERY = 'delivery'
    PICKUP = 'pickup'
   
    CHOICES = [
        (DELIVERY, pgettext_lazy(
            'Status for a fully editable, not confirmed order created by '
            'staff users',
            'Delivery')),
        (PICKUP, pgettext_lazy(
            'Status for an order with no items marked as fulfilled',
            'Pickup'))]
        