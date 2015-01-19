from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url


urlpatterns = patterns('',
    url(r'', include('order_payment.urls')),
)
