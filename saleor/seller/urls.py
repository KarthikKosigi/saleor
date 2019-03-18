from django.conf.urls import url
from django.contrib.auth import views as django_views

from . import views

urlpatterns = [
    url(r'^details/$', views.details, name='details'),
    url(r'^signup/$', views.signup, name='signup')]
