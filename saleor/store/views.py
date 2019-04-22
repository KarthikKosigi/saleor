import json

from django.conf import settings
from django.core.paginator import InvalidPage, Paginator
from django.http import Http404
from django.shortcuts import render
from django.template.response import TemplateResponse

from ..product.utils import products_with_details, products_for_homepage
from ..product.utils.availability import products_with_availability
from ..search.forms import SearchForm
from ..seller.models import Store
from ..menu.models import Menu
from ..seo.schema.webpage import get_webpage_schema


def stores(request):
    if not settings.ENABLE_SEARCH:
        raise Http404('No such page!')
    form = SearchForm(data=request.GET or None)
    if form.is_valid():
        query = form.cleaned_data.get('q', '')
        results = Store.objects.all()
    else:
        query, results = '', []
    page = paginate_results(list(results), request.GET)
    ctx = {
        'query': query,
        'results': Store.objects.all(),
        'query_string': '?q=%s' % query}
    return render(request, 'stores/store_results.html', ctx)

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
    products = products_for_homepage(
        request.user,
        request.site.settings.homepage_collection, store_id)[:8]
    products = list(products_with_availability(
        products, discounts=request.discounts, taxes=request.taxes,
        local_currency=request.currency))
    webpage_schema = get_webpage_schema(request)
    ctx = {
        'store': store,
        'top_menu': menu,
        'parent': None,
        'products': products,
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
