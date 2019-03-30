from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.stores, name='stores'),
    url(r'^(?P<slug>[a-z0-9-_]+?)-(?P<store_id>[0-9]+)/$',
        views.store_details, name='details'),
    url(r'^(?P<slug>[a-z0-9-_]+?)-(?P<store_id>[0-9]+)/search$',
        views.store_search, name='search')]
