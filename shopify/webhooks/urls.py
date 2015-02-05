from django.conf.urls import patterns
from django.conf.urls import url

from .views import OrdersPaidView
from .views import ProductsCreateView
from .views import ProductsUpdateView


urlpatterns = patterns('',
    url(r'^orders/paid/(?P<uuid>[a-z0-9-]+)/$', OrdersPaidView.as_view()),
    url(r'^products/create/(?P<uuid>[a-z0-9-]+)/$', ProductsCreateView.as_view()),
    url(r'^products/update/(?P<uuid>[a-z0-9-]+)/$', ProductsUpdateView.as_view()),
)
