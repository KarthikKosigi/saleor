from django.conf import settings
from ..seller.models import Store
from django.contrib.auth.decorators import login_required


def get_setting_as_dict(name, short_name=None):
    short_name = short_name or name
    try:
        return {short_name: getattr(settings, name)}
    except AttributeError:
        return {}


# request is a required parameter
# pylint: disable=W0613
def default_currency(request):
    return get_setting_as_dict('DEFAULT_CURRENCY')


def search_enabled(request):
    return {'SEARCH_IS_ENABLED': settings.ENABLE_SEARCH}


def store(request):
        if not request.user.is_anonymous:
                try:
                    store = Store.objects.get(owner=request.user)
                except Store.DoesNotExist:
                    store = None
                return {'store': store}
        else:
              return  {'store': None}
