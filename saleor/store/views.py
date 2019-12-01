import json, googlemaps, html

from django.conf import settings
from django.core.paginator import InvalidPage, Paginator
from django.http import Http404
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.decorators import permission_required

from ..product.utils import products_with_details, products_for_homepage
from ..product.utils.availability import products_with_availability
from ..search.forms import SearchForm
from ..menu.models import Menu
from ..seo.schema.webpage import get_webpage_schema
from ..seller.models import Store
from ..product.models import Collection
from . import forms
from django.views.decorators.http import require_POST

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_KEY)


def stores(request):
    if 'location' not in request.COOKIES:
        return redirect(settings.LOGIN_REDIRECT_URL)
    if not settings.ENABLE_SEARCH:
        raise Http404("No such page!")
    form = SearchForm(data=request.GET or None)
    if form.is_valid():
        query = form.cleaned_data.get("q", "")
    else:
        query =""
    ctx = {"top_query": query}
    return render(request, 'stores/store_results.html',ctx)


def near_by_stores(request):
    ids=[]
    results = gmaps.places_nearby(location=((request.GET.get('latlng'))),radius='1000',type='grocery_or_supermarket')

    for item in results["results"]:
        ids.append(item["place_id"])

    if request.GET.get('q'):
        stores = Store.objects.filter(name__icontains=request.GET.get('q'))
    elif request.GET.get('latlng'):
        stores = Store.objects.filter(place_id__in=ids)
    else:
        stores = Store.objects.all()

    ctx = {
        'results': stores
    }
    return render(request, 'stores/partial_store_results.html', ctx)


def paginate_results(results, get_data, paginate_by=settings.PAGINATE_BY):
    paginator = Paginator(results, paginate_by)
    page_number = get_data.get('page', 1)
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        raise Http404('No such page!')
    return page


def store_details(request, slug, store_id, form=None):
    store = Store.objects.get(id=store_id)
    menu = Menu.objects.filter(store_id = store_id).first()
    collection = Collection.objects.get(pk=2)
    products = products_for_homepage(
        request.user,
        request.site.settings.homepage_collection, store_id)[:8]
    products = list(products_with_availability(
        products, discounts=request.discounts, taxes=request.taxes,
        local_currency=request.currency))
    best_sellers = products_for_homepage(
        request.user,
        collection, store_id)[:8]
    best_sellers = list(products_with_availability(
        best_sellers, discounts=request.discounts, taxes=request.taxes,
        local_currency=request.currency))
    webpage_schema = get_webpage_schema(request)
    ctx = {
        'store': store,
        'top_menu': menu,
        'parent': None,
        'products': products,
        'best_sellers': best_sellers,
        'webpage_schema': json.dumps(webpage_schema)
       }
    return TemplateResponse(request, 'stores/details.html', ctx)


def store_search(request, slug, store_id):
    if not settings.ENABLE_SEARCH:
        raise Http404('No such page!')
    form = SearchForm(data=request.GET or None)
    if form.is_valid():
        query = form.cleaned_data.get('q', '')
        results = evaluate_search_query(form, request, store_id)
    else:
        query, results = '', []
    page = paginate_results(list(results), request.GET)
    store = Store.objects.get(id=store_id)
    menu = Menu.objects.filter(store_id = store_id).first()
    ctx = {
        'query': query,
        'top_menu': menu,
        'results': page,
        'store': store,
        'query_string': '?q=%s' % query}
    return render(request, 'stores/product_results.html', ctx)


def evaluate_search_query(form, request, store_id):
    results = products_with_details(request.user).filter(store_id = store_id) & form.search()
    return products_with_availability(
        results, discounts=request.discounts, taxes=request.taxes,
        local_currency=request.currency)

@require_POST
def ajax_reorder_store_images(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)
    form = forms.ReorderProductImagesForm(request.POST, instance=store)
    status = 200
    ctx = {}
    if form.is_valid():
        form.save()
    elif form.errors:
        status = 400
        ctx = {'error': form.errors}
    return JsonResponse(ctx, status=status)

@permission_required('product.manage_products')
def store_image_delete(request, store_pk, img_pk):
    store = get_object_or_404(Store, pk=store_pk)
    image = get_object_or_404(store.images, pk=img_pk)
    if request.method == 'POST':
        image.delete()
        # msg = pgettext_lazy(
        #     'Dashboard message', 'Removed image %s') % (image.image.name,)
        # messages.success(request, msg)
        # return redirect('dashboard:product-image-list', product_pk=product.pk)
    return TemplateResponse(
        request,
        'dashboard/product/product_image/modal/confirm_delete.html',
        {'store': store, 'image': image})

@require_POST
def ajax_upload_image(request, store_pk):
    store = get_object_or_404(Store, pk=store_pk)
    form = forms.UploadImageForm(
        request.POST or None, request.FILES or None, store=store)
    ctx = {}
    status = 200
    if form.is_valid():
        image = form.save()
        ctx = {'id': image.pk, 'image': None, 'order': image.sort_order}
    elif form.errors:
        status = 400
        ctx = {'error': form.errors}
    return JsonResponse(ctx, status=status)
