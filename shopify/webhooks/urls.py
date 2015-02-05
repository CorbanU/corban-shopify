from django.conf.urls import patterns
from django.conf.urls import url

from .views import OrdersPaidView


urlpatterns = patterns('',
    url(r'^orders/paid/(?P<uuid>[a-z0-9-]+)/$', OrdersPaidView.as_view()),
)
