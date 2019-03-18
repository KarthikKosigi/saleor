from decimal import Decimal

from django.conf import settings
from django.contrib.postgres.fields import HStoreField
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.encoding import smart_text
from django.utils.text import slugify
from django.utils.translation import pgettext_lazy
from django_measurement.models import MeasurementField
from django_prices.models import MoneyField
from django_prices.templatetags import prices_i18n
from measurement.measures import Weight
from mptt.managers import TreeManager
from mptt.models import MPTTModel
from prices import TaxedMoneyRange
from text_unidecode import unidecode
from versatileimagefield.fields import PPOIField, VersatileImageField

from ..core import TaxRateType
from ..core.exceptions import InsufficientStock
from ..core.models import PublishableModel, SortableModel
from ..core.utils.taxes import DEFAULT_TAX_RATE_NAME, apply_tax_to_price
from ..core.utils.translations import TranslationProxy
from ..core.weight import WeightUnits, zero_weight
from ..discount.utils import calculate_discounted_price
from ..seo.models import SeoModel, SeoModelTranslation


class Store(SeoModel, PublishableModel):
    name = models.CharField(max_length=128)
    description = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='owner',
        on_delete=models.SET_NULL)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'store:details',
            kwargs={'slug': self.get_slug(), 'store_id': self.id})

    def get_slug(self):
        return slugify(smart_text(unidecode(self.name)))


class StoreImage(SortableModel):
    store = models.ForeignKey(
        Store, related_name='images', on_delete=models.CASCADE)
    image = VersatileImageField(
        upload_to='stores', ppoi_field='ppoi', blank=False)
    ppoi = PPOIField()
    alt = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ('sort_order', )
        app_label = 'store'

    def get_ordering_queryset(self):
        return self.store.images.all()

