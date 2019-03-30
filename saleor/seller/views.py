from django.shortcuts import render
from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth import views as django_views
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import pgettext, ugettext_lazy as _
from django.views.decorators.http import require_POST

from ..checkout.utils import find_and_assign_anonymous_cart
from ..core.utils import get_paginator_items
from ..account.models import User
from ..seller.models import Store
from .forms import (
    ChangePasswordForm, LoginForm, NameForm, PasswordResetForm, SignupForm, StoreForm,
    get_address_form, logout_on_password_change)

def get_or_process_password_form(request):
    form = ChangePasswordForm(data=request.POST or None, user=request.user)
    if form.is_valid():
        form.save()
        logout_on_password_change(request, form.user)
        messages.success(request, pgettext(
            'Storefront message', 'Password successfully changed.'))
    return form


def get_or_process_name_form(request):
    form = NameForm(data=request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, pgettext(
            'Storefront message', 'Account successfully updated.'))
    return form


def get_or_process_store_form(request):
    form = StoreForm(data=request.POST or None, instance=request.user)
    if form.is_valid():
        store = form.save(commit=False)

        store,created = Store.objects.get_or_create(owner_id=request.user.id)
        store.description = form.cleaned_data.get('description')
        store.name = form.cleaned_data.get('name')
        store.save()
        messages.success(request, pgettext(
            'Storefront message', 'Store details successfully updated.'))
    return form


@login_required
def details(request):
    password_form = get_or_process_password_form(request)
    name_form = get_or_process_name_form(request)
    store_form = get_or_process_store_form(request)
    orders = request.user.orders.confirmed().prefetch_related('lines')
    orders_paginated = get_paginator_items(
        orders, settings.PAGINATE_BY, request.GET.get('page'))
    ctx = {'addresses': request.user.addresses.all(),
           'orders': orders_paginated,
           'change_password_form': password_form,
           'store_form': store_form,
           'user_name_form': name_form}

    return TemplateResponse(request, 'seller/details.html', ctx)


def signup(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        form.save()
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = auth.authenticate(
            request=request, email=email, password=password)
        if user:
            auth.login(request, user)
        messages.success(request, _('User has been created'))
        redirect_url = request.POST.get('next', "/seller/details")
        return redirect(redirect_url)
    ctx = {'form': form}
    return TemplateResponse(request, 'seller/signup.html', ctx)

@login_required
def store_edit(request, pk):
    address = get_object_or_404(request.user.addresses, pk=pk)
    address_form, preview = get_address_form(
        request.POST or None, instance=address,
        country_code=address.country.code)
    if address_form.is_valid() and not preview:
        address_form.save()
        message = pgettext(
            'Storefront message', 'Address successfully updated.')
        messages.success(request, message)
        return HttpResponseRedirect(reverse('account:details') + '#addresses')
    return TemplateResponse(
        request, 'account/address_edit.html',
        {'address_form': address_form})

