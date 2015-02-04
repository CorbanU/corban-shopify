from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

from .views import OrderPaymentView


urlpatterns = patterns('',
    url(r'^order-payment/(?P<uuid>[a-z0-9-]+)/$', OrderPaymentView.as_view()),
)
