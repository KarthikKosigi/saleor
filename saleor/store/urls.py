from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.stores, name='stores'),
    url(r'^near-by/$', views.near_by_stores, name='near-by-stores'),
    url(r'^(?P<slug>[a-z0-9-_]+?)-(?P<store_id>[0-9]+)/$',
        views.store_details, name='details'),
    url(r'^(?P<slug>[a-z0-9-_]+?)-(?P<store_id>[0-9]+)/search$',
        views.store_search, name='search'),

    # url(r'^(?P<store_pk>[0-9]+)/images/$',
    #     views.store_images, name='store-image-list'),
    url(r'^(?P<store_pk>[0-9]+)/images/(?P<img_pk>[0-9]+)/delete/$',
        views.store_image_delete, name='store-image-delete'),
    url(r'^(?P<store_pk>[0-9]+)/images/reorder/$',
        views.ajax_reorder_store_images, name='store-images-reorder'),
    url(r'^(?P<store_pk>[0-9]+)/images/upload/$',
        views.ajax_upload_image, name='store-images-upload'),]
