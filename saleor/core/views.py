import urllib, json

from django.contrib import messages
from django.template.response import TemplateResponse, HttpResponse
from django.utils.translation import pgettext_lazy
from impersonate.views import impersonate as orig_impersonate
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render

from ..account.models import User
from ..dashboard.views import staff_member_required
from ..product.utils import products_for_homepage
from ..product.utils.availability import products_with_availability
from ..seo.schema.webpage import get_webpage_schema
import googlemaps
from googlemaps.places import places_autocomplete_session_token
from datetime import datetime


gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_KEY)

def home(request):
    if 'location' in request.COOKIES:
        return redirect('/stores')
    return TemplateResponse(request, 'home.html')


def sellerhome(request):
    products = products_for_homepage(
        request.user,
        request.site.settings.homepage_collection)[:8]
    products = list(products_with_availability(
        products, discounts=request.discounts, taxes=request.taxes,
        local_currency=request.currency))
    webpage_schema = get_webpage_schema(request)
    return TemplateResponse(
        request, 'seller_home.html', {
            'parent': None,
            'products': products,
            'webpage_schema': json.dumps(webpage_schema)})


def getLocations(request):
    geocode_result = gmaps.places_autocomplete_query(request.GET.get('q'))
    return JsonResponse({'results': geocode_result})


def reverse_geocode(request):
    #geocode_result = [{"address_components":[{"long_name":"277","short_name":"277","types":["street_number"]},{"long_name":"Bedford Avenue","short_name":"Bedford Ave","types":["route"]},{"long_name":"Williamsburg","short_name":"Williamsburg","types":["neighborhood","political"]},{"long_name":"Brooklyn","short_name":"Brooklyn","types":["political","sublocality","sublocality_level_1"]},{"long_name":"Kings County","short_name":"Kings County","types":["administrative_area_level_2","political"]},{"long_name":"New York","short_name":"NY","types":["administrative_area_level_1","political"]},{"long_name":"United States","short_name":"US","types":["country","political"]},{"long_name":"11211","short_name":"11211","types":["postal_code"]}],"formatted_address":"277 Bedford Ave, Brooklyn, NY 11211, USA","geometry":{"location":{"lat":40.7142205,"lng":-73.9612903},"location_type":"ROOFTOP","viewport":{"northeast":{"lat":40.71556948029149,"lng":-73.95994131970849},"southwest":{"lat":40.7128715197085,"lng":-73.9626392802915}}},"place_id":"ChIJd8BlQ2BZwokRAFUEcm_qrcA","types":["street_address"]}]
    geocode_result = gmaps.reverse_geocode((request.GET.get('latlng')))
    return JsonResponse({'results': geocode_result})


@staff_member_required
def styleguide(request):
    return TemplateResponse(request, 'styleguide.html')


def impersonate(request, uid):
    response = orig_impersonate(request, uid)
    if request.session.modified:
        msg = pgettext_lazy(
            'Impersonation message',
            'You are now logged as {}'.format(User.objects.get(pk=uid)))
        messages.success(request, msg)
    return response


def handle_404(request, exception=None):
    return TemplateResponse(request, '404.html', status=404)


def manifest(request):
    return TemplateResponse(
        request, 'manifest.json', content_type='application/json')
