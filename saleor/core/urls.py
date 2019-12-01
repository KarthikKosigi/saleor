from django.conf.urls import url
from impersonate.views import stop_impersonate

from . import views

urlpatterns = [
    url(r'^seller/$', views.sellerhome, name='seller-home'),
    url(r'^locations/$', views.getLocations, name='locations'),
    url(r'^reverse-geocode/$', views.reverse_geocode, name='reverse-geocode'),
    url(r'^$', views.home, name='home'),
    url(r'^style-guide/', views.styleguide, name='styleguide'),
    url(r'^impersonate/(?P<uid>\d+)/', views.impersonate,
        name='impersonate-start'),
    url(r'^impersonate/stop/$', stop_impersonate,
        name='impersonate-stop'),
    url(r'^404', views.handle_404, name='handle-404'),
    url(r'^manifest\.json$', views.manifest, name='manifest'),
]
