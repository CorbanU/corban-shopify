from django.conf.urls import patterns
from django.conf.urls import url

from .views import OrderPaymentView


urlpatterns = patterns('',
    url(r'^order-payment/$', OrderPaymentView.as_view(), name='order_payment'),
)
