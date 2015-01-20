from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin

from .views import OrderPaymentView


urlpatterns = patterns('',
    url(r'^order-payment/$', OrderPaymentView.as_view(), name='order_payment'),
    url(r'^admin/', include(admin.site.urls)),
)
