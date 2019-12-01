import bleach
from django import forms
from django.conf import settings
from django.db.models import Count, Q
from django.forms.models import ModelChoiceIterator
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.encoding import smart_text
from django.utils.text import slugify
from django.utils.translation import pgettext_lazy
from django_prices_vatlayer.utils import get_tax_rate_types
from mptt.forms import TreeNodeChoiceField
from ..seller.models import StoreImage
from ..product.thumbnails import create_store_thumbnails

# from ...core import TaxRateType
# from ...core.utils.taxes import DEFAULT_TAX_RATE_NAME, include_taxes_in_prices
# from ...core.weight import WeightField
# from ...product.models import (
#     Attribute, AttributeValue, Category, Collection, Product, ProductImage,
#     ProductType, ProductVariant, VariantImage)
# from ...product.tasks import update_variants_names
# from ...product.thumbnails import create_product_thumbnails
# from ...product.utils.attributes import get_name_from_attributes
# from ..forms import ModelChoiceOrCreationField, OrderedModelMultipleChoiceField
# from ..seo.fields import SeoDescriptionField, SeoTitleField
# from ..seo.utils import prepare_seo_description
# from ..widgets import RichTextEditorWidget
# from . import ProductBulkAction
# from .widgets import ImagePreviewWidget

class UploadImageForm(forms.ModelForm):
    class Meta:
        model = StoreImage
        fields = ('image',)
        labels = {
            'image': pgettext_lazy('Product image', 'Image')}

    def __init__(self, *args, **kwargs):
        store = kwargs.pop('store')
        super().__init__(*args, **kwargs)
        self.instance.store = store

    def save(self, commit=True):
        image = super().save(commit=commit)
        create_store_thumbnails.delay(image.pk)
        return image 
